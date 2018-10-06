# Untitled - By: rick - 周五 10月 5 2018

import sensor, image, time
from pyb import LED

## One time setup
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

green_led = LED(1)
blue_led = LED(2)
#broken1_led  = LED(3)
#broken2_led    = LED(4)

img = sensor.snapshot()
appleRoi = ()

#apple_th = (30, 75, 50, 70 ,0, 40)
apple_th = (30, 75, 40, 70 , 20, 60)
#apple_th = (60, 90, 20, 60, -20, 10)

#maxRatio = 1.5
#minDensity = 0.4

#maxPixelCnt =

def extendROI(Rect):
    v_x = Rect[0]
    v_y = Rect[1]
    r_width = Rect[2]
    r_height = Rect[3]

    xCenter = v_x + r_width / 2
    yCenter = v_y + r_height / 2

    r_width = r_width * 1.2
    r_height = r_height *1.2

    result = (int(xCenter - r_width / 2), int(yCenter - r_height / 2), int(r_width), int(r_height))
    return result

def areaIsGood(Rect):
    r_w = Rect[2]
    r_h = Rect[3]
    #area = r_w * r_h

    if ((r_w < 80 and r_h < 105)or(r_w < 105 and r_h < 80)):
        return False

    return True


## Main program
while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img
    print(clock.fps())

    green_led.off()
    blue_led.off()
    # inrange select the color

    # find edge
    #grayImg = img.to_grayscale()
    #edgImg = grayImg.find_edges(image.EDGE_CANNY, threshold=(0, 80))
    #grayImg.laplacian(5)
    #grayImg.binary([(2, 255)])
    #grayImg.dilate(1)
    #grayImg.midpoint(1)

# find the blobs for apple
    # make sure the roi is not empty
    if appleRoi:
        # extend the roi, or the roi is likely to shrink on every loop
        appleRoiEx = extendROI(appleRoi)
        objBoxs = img.find_blobs([apple_th], pixels_threhold = 200, roi = appleRoiEx, merge = True, margin = 0)
        print("roi found")
    else:
        objBoxs = img.find_blobs([apple_th], pixels_threhold = 200, merge = True, margin = 0)
        print("roi not founded!")

    if objBoxs:
        maxArea = 0
        mIndex = 0
        for i in range(0, len(objBoxs)):
            #img.draw_rectangle(objBoxs[i].rect())
            if objBoxs[i].area() > maxArea:
                maxArea = objBoxs[i].area()
                mIndex = i
        objBlob = objBoxs[mIndex]
        appleRoi = objBlob.rect()
        img.draw_rectangle(appleRoi, color = (255, 255, 0))
        print("obj found")

        green_led.on()

    else:
        appleRoi = ()
        print("obj not found!")

        blue_led.toggle()

        continue
    print('\n')

# get the info of density and ratio of target
    #density = objBlob.density()
    #ratio = objBlob.w() / objBlob.h()
    pixelCnt = objBlob.pixels()
    area = objBlob.area()
    #img.draw_string(appleRoi[0], appleRoi[1], str(density), color = (255, 255, 0))
    print("pix: %d,  area: %d, width: %d, height: %d"%(pixelCnt, area, objBlob.w(), objBlob.h()))

# when the target is close enough, shift into auto mode
    #if areaIsGood(objBlob.rect()):
        #unkown_led.toggle()









