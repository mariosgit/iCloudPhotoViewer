from pyicloud import PyiCloudService
from sys import exit
from os import environ, system
from random import choice
from time import sleep
from getpass import getpass

username = environ['USERNAME']
# password = environ['PASSWORD']
password = getpass("Enter iCloud Password for %s: "%username)


api = PyiCloudService(username, password)

if api.requires_2sa:
    print "Two-step authentication required. Your trusted devices are:"
    devices = api.trusted_devices
    #print devices
    for i, device in enumerate(devices):
        print "  %s: %s" % (i, device.get('deviceName', "SMS to %s" % device.get('phoneNumber')))
    device = devices[0]
    print device
    if not api.send_verification_code(device):
        print "Failed to send verification code"
        exit(1)
    code = raw_input("Enter Verification Code: ")
    print code
    if not api.validate_verification_code(device, code):
        print "Failed to verify verification code"
        exit(1)

print "Auth OK !"
# print api.iphone.play_sound()
# print api.iphone.location()

for album in api.photos.albums:
    print "Album", album.title()

photos = api.photos.albums['2017 Segeln']
print type(photos)
photolist = []
for photo in photos:
    photolist.append(photo)
#for photo in photolist:
#    print photo, photo.filename

print "Fotos in list:", len(photolist)

filename = "photo.jpg"
while(1):
    photo = choice(photolist)
    print photo.filename, photo.size, photo.dimensions
    if photo.dimensions[0] * photo.dimensions[1] < 15000000:
        download = photo.download('medium')
        with open(filename, 'wb') as opened_file:
            opened_file.write(download.raw.read())
            opened_file.close()

        system("sudo killall fbi")
        system("sudo fbi -T 2 -d /dev/fb0 -a --noverbose %s"%(filename))

        sleep(30)
    else:
        print "skipping large photo"

