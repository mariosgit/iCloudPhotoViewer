import pygame
import Image, ImageDraw, ImageFont
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudAPIResponseError
from sys import exit
from os import environ, system
from random import choice
from time import sleep
from getpass import getpass

# globals
#  select an album, otherwise a random one is taken
albumName = '2017 Segeln'


username = environ['USERNAME']
password = environ['PASSWORD']
# password = getpass("Enter iCloud Password for %s: "%username)

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
    # print code
    if not api.validate_verification_code(device, code):
        print "Failed to verify verification code"
        exit(1)

print "iCloud Authentication OK !"


# Open a window on the screen
screen = screen=pygame.display.set_mode() # [0,0], pygame.OPENGL)
pygame.mouse.set_visible(0)
print pygame.display.get_driver()
print pygame.display.Info()
myfont = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 25)

albums = []
for album in api.photos.albums:
    #  print "Album", album.title()
    albums.append(album.title())
# print albums 

if albumName not in albums:
    albumName = choice(albums)
photos = api.photos.albums[albumName]
# print type(photos) # pyicloud.services.photos.PhotoAlbum
photolist = []
for photo in photos:
    photolist.append(photo)

print "# Fotos in album \"%s\": %d" % (albumName,len(photolist))

filename = "photo.jpg"
while(1):
    photo = choice(photolist)
    if photo and photo.dimensions[0] * photo.dimensions[1] < 15000000:
        print photo.filename, photo.size, photo.dimensions
        try:
            download = photo.download('medium')
            if download:
                with open(filename, 'wb') as opened_file:
                    opened_file.write(download.raw.read())
                    opened_file.close()

            # load, resize image
            img = Image.open(filename)
            img.thumbnail(screen.get_size())
            draw = ImageDraw.Draw(img)
            draw.text([19,19], albumName, fill=(000,000,000), font=myfont)
            draw.text([21,19], albumName, fill=(000,000,000), font=myfont)
            draw.text([21,21], albumName, fill=(000,000,000), font=myfont)
            draw.text([19,21], albumName, fill=(000,000,000), font=myfont)
            draw.text([20,20], albumName, fill=(255,222,000), font=myfont)

            # convert to pygame image
            image = pygame.image.fromstring(img.tostring(), img.size, img.mode)
            image = image.convert()

            # center and draw
            ssize = img.size
            tsize = screen.get_size()
            screen.fill([0,0,0])
            screen.blit(image, [(tsize[0]-ssize[0])/2,(tsize[1]-ssize[1])/2])
            pygame.display.flip() # display update

            sleep(10)
        except IOError, err:
            print err
        except PyiCloudAPIResponseError, err:
            print err
        except KeyboardInterrupt:
            print "Bye!"
            exit(0)
    else:
        print "skipping large photo"

