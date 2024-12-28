#!/usr/bin/env python3

import sys
import time
import signal
import socket
import qrcode
import argparse
import requests
import threading
import subprocess
import tkinter as tk
from PIL import ImageTk

# SCRIPT VERSION & Author: Anuj Das (ADx)
SCRIPT_VERSION = "v1.1.0"



# Globals to store subprocesses
ngrok_process, http_server_process = None, None



# It checks whether the given port is already in use or not!
def is_port_in_use(port):
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0



# It is used to get the local IP of the machine
def get_local_ip():
    """Get the local IP address of the machine."""
    result = subprocess.run(
        "hostname -I", shell=True, capture_output=True, text=True
    )
    return result.stdout.strip().split()[0]  # Get the first IP address



# It starts local HTTP server on specified port number if port is not in use.
def start_local_server(port):
    """Start a local HTTP server."""
    global http_server_process
    if is_port_in_use(port):
        print(f"Error: Port {port} is already in use. Please specify a different port.")
        return
    print(f"Starting local HTTP server on port {port}...")
    http_server_process = subprocess.Popen(["python3", "-m", "http.server", str(port)],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)



# It starts ngrok HTTP server on specified port number and provides a
# public URL when it is ready, which can be used to access server outside the LAN.
def start_ngrok(port):
    """Start Ngrok and return when the public URL is ready."""
    global ngrok_process
    print(f"Starting Ngrok for port {port}...")

    try:
        # Start Ngrok in a subprocess
        ngrok_process = subprocess.Popen(["ngrok", "http", str(port)],
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)
        time.sleep(2)   # Allow time for Ngrok to initialize

        # Fetch the public URL from Ngrok's API
        while True:
            try:
                response = requests.get("http://localhost:4040/api/tunnels")
                response_data = response.json()
                for tunnel in response_data.get("tunnels", []):
                    if tunnel.get("proto") == "https":
                        return tunnel.get("public_url")
            except requests.exceptions.ConnectionError:
                time.sleep(1)   # Wait for the API to become available

    except Exception as e:
        print(f"Error starting Ngrok: {e}")
        return None



# This function is used to display QR Code for the generated Local/Global URL
def displayQR(address, title=f"QSync: {SCRIPT_VERSION}"):
    """Generate and display a QR code using Tkinter in a separate thread."""
    def run_tkinter():
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=12,
            border=4,
        )
        qr.add_data(address)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Display QR code using Tkinter
        root = tk.Tk()
        root.title(title)
        qr_image = ImageTk.PhotoImage(img)
        label = tk.Label(root, image=qr_image)
        label.pack()

        # Keep the tkinter window open but doesn't block the main process
        root.mainloop()

    # Start Tkinter event loop in a separate thread
    threading.Thread(target=run_tkinter, daemon=True).start()



# It is used to release all the allocated resources like port, etc.
def cleanup():
    """Clean up resources before exiting."""
    global http_server_process, ngrok_process
    print("\nDisposing running resources...")
    if http_server_process:
        print("Terminating local HTTP server...")
        http_server_process.terminate()
        http_server_process.wait()
    if ngrok_process:
        print("Terminating Ngrok process...")
        ngrok_process.terminate()
        ngrok_process.wait()

    # Ensuring that the ports are free after cleanup
    print(f"\nPort disposed successfully!")



# It handles termination of running script.
def signal_handler(sig, frame):
    """Handle termination signals (Ctrl+C or SIGTERM)."""
    cleanup()
    sys.exit(0)



# This is the main method which handles command line arguments and parses it.
def main():
    # Set up signal handlers for graceful termination
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
         description=(
            "QSync, also known as QuickSync!\n"
            "This script is developed by: Anuj Das (ADx)\n\n"
            "QSync allows you to share files over local or global network with ease!\n\n"

            "[+] QSync enables easy file sharing by hosting a lightweight HTTP server on your local machine.\n" 
            "    Users on the same network can access shared files using a generated URL (Local Network Mode).\n\n"
            "[+] For global access, it uses Ngrok to create a secure tunnel to your local server,\n"
            "    allowing peer-to-peer sharing over the internet.\n\n"
            "[+] Simply generate the QR code, share it, and let others connect directly to your system!\n\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-v", "--version", action="version", version=f"QSync: {SCRIPT_VERSION}", help="show current script's version number and exit")
    parser.add_argument("-l", metavar="PORT", type=int, help="share over local network")
    parser.add_argument("-g", metavar="PORT", type=int, help="share globally using ngrok")
    args = parser.parse_args()

    if args.l:
        port = args.l
        if is_port_in_use(port):
            print(f"Error: Port {port} is already in use. Please specify a different port.")
            return
        # Start the local server in a separate thread
        threading.Thread(target=start_local_server, args=(port,), daemon=True).start()
        local_ip = get_local_ip()
        local_url = f"http://{local_ip}:{port}"
        print(f"Local URL: {local_url}")
        displayQR(local_url, title=f"QSync: {SCRIPT_VERSION} - Sharing Locally") 

    elif args.g:
        port = args.g
        if is_port_in_use(port):
            print(f"Error: Port {port} is already in use. Please specify a different port.")
            return
        # Start the local server in a separate thread
        threading.Thread(target=start_local_server, args=(port,), daemon=True).start()

        # Start Ngrok and fetch the public URL
        print("Waiting for Ngrok URL...")
        ngrok_url = start_ngrok(port)

        if ngrok_url:
            print(f"Global URL: {ngrok_url}")
            displayQR(ngrok_url, title=f"QSync: {SCRIPT_VERSION} - Sharing Globally")
        else:
            print("Failed to get Ngrok URL. Make sure Ngrok is installed and running.")

    else:
        print("Please specify either -l or -g with a port number.")
        parser.print_help()

    # Keep the script running
    print("\nPress Ctrl + C to terminate the script!")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
