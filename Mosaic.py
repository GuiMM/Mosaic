from PIL import Image
import os
mosaicDirectoryBricks = 'sourceImages'
sourceFile = 'gui.jpg'
mosaicFile = 'sou.png'
dimensionPixelBricks = 100

def avg_rgb(img):
    rgb_im = img.convert('RGB')
    media = [0,0,0]
    x,y = img.size
    for line in range(0,x):
        for col in range(0,y):
            r, g, b = rgb_im.getpixel((line, col))
            media[0] += r
            media[1] += g
            media[2] += b

    pixels = x*y
    media[0] /= pixels
    media[1] /= pixels
    media[2] /= pixels
    return media

def calculate_avg_imgs():
    aux = 0
    dict = {}
    for filename in os.listdir(mosaicDirectoryBricks):
        if (filename.endswith(".jpg") | filename.endswith(".gif") | filename.endswith(".png")):
            f = Image.open(mosaicDirectoryBricks+'/'+filename)
            media = avg_rgb(f)
            dict[aux] = mosaicDirectoryBricks+'/'+filename, media
            aux += 1
    return dict

def choose_better_image(pixel,dict):
    chosed = 0
    minDistance = 10000
    for i in range(0, len(dict)):
        distance = ((pixel[0]-dict[i][1][0])**2 + (pixel[1]-dict[i][1][1])**2 + (pixel[2]-dict[i][1][2])**2)**(0.5)
        if(distance < minDistance):
            minDistance = distance
            chosed = i
    print "chosed: " + str(i) + "distance: " + str(minDistance)
    return dict[chosed][0]


im = Image.open(sourceFile) # Can be many different formats.
pix = im.load()
print im.size  # Get the width and hight of the image for iterating over
w,h = im.size

#creating the blank mosaic image file
newImage = Image.new('RGB', (w*100, h*100), (0,0,0))
#preparing the avg pixel of all images
dict = calculate_avg_imgs()
#main loop to build the mosaic
for x in range(0,w):
    for y in range(0,h):
        rgb_im = im.convert('RGB')
        pixel = rgb_im.getpixel((x, y))
        substImg = choose_better_image(pixel, dict)
        pixelImg = Image.open(substImg)
        #pasting the mosaic parts and positioning after the pixel size of bricks(dimensionPixelBricks)
        newImage.paste(pixelImg, (x*dimensionPixelBricks, y*dimensionPixelBricks))


newImage.save(mosaicFile)

