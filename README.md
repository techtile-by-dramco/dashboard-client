# RPI TechtileDashboard-client Firmware
### 0️⃣ Update the System and install required packages
- On the raspberry pi
  ```
  sudo apt update
  sudo apt upgrade -y
	```
  ```
  sudo apt install git -y
  sudo apt install git openssh-client -y
  sudo apt install python3 python3-pip python3-venv -y
  ```

### 1️⃣ Create SSH Key to clone this repository
Generate SSH Key on the Pi
```
ssh-keygen -t ed25519 -C "your_email@example.com"
```
Copy the public Key
```
cat ~/.ssh/id_ed25519.pub
```
- ENTER 3x
- Go to **this** Github account [online]
- Add this public Key: settings --> SSH and GPG Keys
- New SSH Key
- Paste this Key

Test SSH Connection, in the RPI terminal

```
ssh -T git@github.com
```

### 2️⃣ Clone this repo via SSH
```
git@github.com:techtile-by-dramco/dashboard-client.git
cd dashboard-client
```

### 3️⃣ Test Python scripts manually (important)
Run each script once to confirm it works before making services

```
cd ~/dashboard-client
./venv/bin/python Test_RPI.py
```

Stop it with Ctrl+C, then:

```
RPI_control.py
```
And make sure that all necessary libraries are installed before proceeding!


### 4️⃣ Create the two systemd services

4.1 Test_RPI.service
```
sudo nano /etc/systemd/system/Test_RPI.service
# Copy past content form the Test_RPI.service file on Github
# Save and exit .service file
sudo systemctl daemon-reload
sudo systemctl enable Test_RPI.service
sudo systemctl start Test_RPI.service
systemctl status Test_RPI.service
```
  
4.2 rpi-control.service
```
sudo nano /etc/systemd/system/rpi-control.service
# Copy past content form the rpi-control.service file on Github
# Save and exit .service file
sudo systemctl daemon-reload
sudo systemctl enable rpi-control.service
sudo systemctl start rpi-control.service
systemctl status rpi-control.service
```

4.3 Troubleshooting (if necessary)
- View logs:
```
sudo journalctl -u Test_RPI.service -f
sudo journalctl -u rpi-control.service -f
```

- Restart after changes:

```
sudo systemctl restart Test_RPI.service
sudo systemctl restart rpi-control.service 
```

- Verify start after reboot (if service is enabled)
```sudo reboot```
