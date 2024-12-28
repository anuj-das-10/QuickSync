# QuickSync (QSync)
> **Version: v1.0.0** <br>
> **Author: Anuj Das (ADx)**


<br/>

### QuickSync, also known as QSync!

It allows you to share files over local or global network with ease!

- QSync enables easy file sharing by hosting a lightweight HTTP   
    server on your local machine.
    Users on the same network can access shared files using a generated URL (Local Network Mode).

- For global access, it uses Ngrok to create a secure tunnel to your local server,
    allowing peer-to-peer sharing over the internet.

- Simply generate the QR code, share it, and let others connect directly to your system!

<br/><br/>

# Getting started

```bash
sudo pip3 install -r requirements.txt
```
or

```bash
sudo apt install python3-qrcode
sudo apt install python3-pillow
```

<br/><br/>

## Setup guide to use `qsync` script globally on Ubuntu  

Follow the steps below to set up the `qsync` script globally on your Ubuntu system so it can be accessed from anywhere in the terminal without specifying its file extension.


### 1. **Save the Script in a Global Directory**  
- **Choose a Global Directory**  
   Place the script in a directory that is included in your system's `PATH`. Common directories include:  
   - `/usr/local/bin/` (preferred for custom scripts)  
   - `/usr/bin/`

- **Move the Script**  
   Assuming the script file is named `qsync.py` and is in your current directory:  
   ```bash
   sudo mv qsync.py /usr/local/bin/qsync
   ```

   Rename the script to `qsync` (without the `.py` extension) during the move.

<br/>

### 2. **Make the Script Executable**  
Grant execute permissions to the script so it can be run directly:  

```bash
sudo chmod +x /usr/local/bin/qsync
```

<br/><br/>

### 3. **Verify the setup**  
Check if the script is accessible globally by typing:  
```bash
qsync -v
```
or
```bash
qsync -h
```

If the setup is correct, you should see the help menu or version of the `qsync` script.

<br/><br/>


### 4. **Usage**  
Once set up, you can run the script from any directory in the terminal:  
- Share over Local Network:  

  ```bash
  qsync -l 8080
  ```
- Share Globally (if Ngrok is configured):
        
  ```bash
  qsync -g 8080
  ```
    - [See ngrok configuration guide](docs/ngrok_setup_guide.md)


<br/>

This setup ensures `qsync` is globally accessible and executable without needing to type its file extension or specify its full path.

<br>

---

**TIPS**: Move both file `qsync.py` & `QSync.py` to `/usr/local/bin/`, so that case sensitivity does not bother you!

---

<br/>

### Thank You & Happy Coding :-)