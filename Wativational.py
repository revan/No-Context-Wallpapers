#!/bin/python
import praw
from PIL import Image, ImageFont, ImageDraw
import pyimgur
from random import choice
from urlparse import urlparse
import textwrap
from secrets import IMGUR_ID, IMGUR_SECRET

def standardizeImgur(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == 'imgur.com':
        #is album or framed page
        if parsed_url.path.split('/')[1]=='a':
            #is album, skip
            raise Exception()
        else:
            return parsed_url.geturl()+'.jpg'
    elif parsed_url.netloc == 'i.imgur.com':
        #is image file
        return  parsed_url.geturl()
    raise Exception()

#font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', 20)

r = praw.Reddit(user_agent='Wativational')
submissions = r.get_subreddit('nocontext').get_hot(limit=20)
titles = [vars(x)['title'] for x in submissions]

submissions = r.get_subreddit('wallpapers').get_hot(limit=20)
images = [vars(x)['url'] for x in submissions]

im = pyimgur.Imgur(IMGUR_ID)

title = choice(titles)
url = ''
image = ''
for attempt_number in range(50):
    try:
        url = standardizeImgur(choice(images))
    except:
        continue
    url = url.rsplit('/',1)[1].split('.')[0]
    print(url) 
    image = im.get_image(url)
    break

print(title)
print(image)

Image.open(image.download('/tmp/', overwrite=True))
