# Setup Ngrok on Ubuntu

<br/>

## Step 1: Download Ngrok
1. Open a terminal on your Ubuntu system.
2. Download the latest version of ngrok using the following command:

   ```bash
   wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
   ```

<br/>

## Step 2: Extract the Ngrok Package
1. Extract the downloaded tarball:

   ```bash
   tar -xvzf ngrok-v3-stable-linux-amd64.tgz
   ```

<br/>

## Step 3: Move the Ngrok Binary to a System Directory
1. Move the `ngrok` binary to a directory in your system's `PATH`, such as `/usr/local/bin/`:

   ```bash
   sudo mv ngrok /usr/local/bin/
   ```

<br/>

## Step 4: Verify Installation
1. Check if ngrok is installed correctly by running:

   ```bash
   ngrok version
   ```
   This should display the installed version of ngrok.

<br/>

## Step 5: Authenticate Ngrok (Optional)
1. Go to the [ngrok dashboard](https://dashboard.ngrok.com) and sign up or log in.
2. Copy your **Auth Token** from the dashboard.
3. Authenticate ngrok by running:

   ```bash
   ngrok config add-authtoken $YOUR_AUTHTOKEN
   ```

<br/>

## Step 6: Start Using Ngrok
1. To expose a local web server running on port 8080, use:

   ```bash
   ngrok http 8080
   ```
2. Ngrok will provide a public URL for your local server, which you can share or use for testing.

<br/>
<br/>

---

### Notes:
- Ngrok free plan provides random subdomains that change each time you restart ngrok.
- For permanent subdomains or additional features, consider upgrading to a paid plan.

---

Enjoy using Ngrok on your Ubuntu system!
