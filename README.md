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

### Attach Serial Device
In PowerShell (Admin):
```
usbipd wsl list
usbipd wsl attach --busid <BUSID (EX: 3-1)>
```

### Detach Serial Device (if still connected to WSL)
In PowerShell (Admin):
```
usbipd wsl list
usbipd wsl detach --busid <BUSID (EX: 3-1)>
```

In some sitations when `usbipd bind --force` has been used (which is sometimes the default) an extra step is required:
```
usbipd unbind --busid <BUSID (EX: 3-1)>
```

### Reset Serial Device
Once attached to WSL press the reset switch.

Serial write does not work until the STM32 is reset, reading still works however.

Resetting the STM32 while the application is running will break the sync mechanism.

## Useage
```
python3 main.py -h
```
