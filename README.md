# Servo Drive Application

## Installation
```
python3 -m venv venv
source venv
pip install --upgrade pip
pip install -r requirements.txt
```

## Attaching STM32 Serial Port to WSL2

### Start udev Service
In WSL:
```
sudo vim /etc/wsl.conf
```

Add the following:
```
[boot]
command="service udev start"
```

Exit and restart WSL.

### Attach Serial Device (Repeat when device is reset)
In PowerShell (Admin):
```
usbipd wsl list
usbipd wsl attach --busid <BUSID (EX: 3-1)>
```

## Useage
```
python3 main.py -h
```