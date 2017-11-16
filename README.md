iCloudPhotoViewer is a small python app, that shows your iCloud photos on a RaspberryPi with TFT screen.
It uses the framebuffer devices /dev/fb0 as graphical output, so no X is required, thus it saves resources on your Pi.

Tested with RetroPie distribution, it does not install X and emulation station can be turned off easily.
To turn off Emulation station at startup, start the config tool
```
sudo ./RetroPie-Setup/retropie_setup.sh
```
Go to "C"-Configuration/Tools / autostart, Choose "Boot to text console (auto login as pi).

# Requirements:

* iCloud Access module https://github.com/picklepete/pyicloud
* pygame
* PIL

# Usage

```
export SDL_FBDEV=/dev/fb0
export SDL_VIDEODRIVER=fbcon
sudo USERNAME="YOURAPPLEID" PASSWORD="YOURPW" python iCloudPhotoViewer.py 
```

PS: This is not the savest way to store the password !
