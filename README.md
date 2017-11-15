iCloudPhotoViewer is a small python app, that shows your iCloud photos on a RaspberryPi with TFT screen.
It uses the framebuffer devices /dev/fb0 as graphical output, so no X is required, thus it saves resources on your Pi.

Tested with RetroPie distribution, it does not install X and emulation station can be turned off easily.

# Requirements:

* iCloud Access module https://github.com/picklepete/pyicloud
* fbi needs to be installed.

# Usage

export USERNAME='YOURAPPLEID'
python iCloudPhotoViewer

At the moment the "fbi" app is used to show the image, it will be startet with sudo to get access to /dev/fb0, normaly this works on the pi without password prompt. If not you can change the access right to the /dev/fb0 device.
