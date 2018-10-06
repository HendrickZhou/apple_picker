# Untitled - By: rick - 周五 10月 5 2018

import sensor, image, time
from pyb import LED

## One time setup
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()
img = sensor.snapshot()
SIZE = (img.width(), img.height())
CENTER = (img.width() / 2, img.height() / 2)
AREA = img.size()

green_led = LED(1)
blue_led = LED(2)
#broken1_led  = LED(3)
#broken2_led    = LED(4)

appleRoi = ()

#apple_th = (30, 75, 50, 70 ,0, 40)
apple_th = (30, 75, 40, 70 , 20, 60)
#apple_th = (60, 90, 20, 60, -20, 10)

#maxRatio = 1.5
#minDensity = 0.4

#maxPixelCnt =

def extendRoiWithBias(Rect, last_flag):
    v_x = Rect[0]
    v_y = Rect[1]
    r_width = Rect[2]
    r_height = Rect[3]

    xCenter = v_x + r_width / 2
    yCenter = v_y + r_height / 2

    # extend the area
    r_width = r_width * 1.2
    r_height = r_height *1.2

    # add the bias
    if last_flag[0] == 0:
        x_b = 0
    elif last_flag[0] == 1:
        x_b = -10 # targe on right, roi turn left
    else:
        x_b = 10

    if last_flag[1] == 0:
        y_b = 0
    elif last_flag[1] == 1:
        y_b = -10 # target down, roi turn upwards
    else:
        y_b = 10

    result = (int(xCenter - r_width/2 + x_b/2), int(yCenter - r_height/2 + y_b/2), int(r_width), int(r_height))
    return result

def areaIsGood(Rect):
    r_w = Rect[2]
    r_h = Rect[3]
    #area = r_w * r_h
    if ((r_w < 80 and r_h < 105)or(r_w < 105 and r_h < 80)):
        return False
    return True

def judgeDirection(Blob):
    size = Blob.area()
    min_b_x = 10 * (1 + size/AREA)
    min_b_y = 10 * (1 + size/AREA)
    obj_center_x = Blob.cx()
    obj_center_y = Blob.cy()
    bias_x = obj_center_x - CENTER[0]
    bias_y = obj_center_y - CENTER[1]

    if abs(bias_x) < min_b_x:
        x_flag = 0 # still
    elif bias_x > 0:
        x_flag = 1 # target is on the right
    else:
        x_flag = 2 # target is on the left

    if abs(bias_y) < min_b_y:
        y_flag = 0 # still
    elif bias_y > 0:
        y_flag = 1 # target is down
    else:
        y_flag = 2 # target is up
    return [x_flag, y_flag]

last_flag = [0, 0] # 0 for x, 1 for y

## Main program
while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img
    print(clock.fps())




    green_led.off()
    blue_led.off()

# find the blobs for apple
    # make sure the roi is not empty
    if appleRoi:
        # extend the roi, or the roi is likely to shrink on every loop
        appleRoiEx = extendRoiWithBias(appleRoi, last_flag)
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
        last_flag = judgeDirection(objBlob)

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
