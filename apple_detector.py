# Untitled - By: rick - 周五 10月 5 2018

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)

clock = time.clock()

img = sensor.snapshot()
appleRoi = ()
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

while(True):
    clock.tick()
    img = sensor.snapshot()
    img = img
    print(clock.fps())

    # inrange select the color

    # find edge
    #grayImg = img.to_grayscale()
    #edgImg = grayImg.find_edges(image.EDGE_CANNY, threshold=(0, 80))
    #grayImg.laplacian(5)
    #grayImg.binary([(2, 255)])
    #grayImg.dilate(1)
    #grayImg.midpoint(1)

# find the blobs for apple
    #apple_th = (30, 75, 50, 70 ,0, 40)
    apple_th = (30, 75, 40, 70 , 20, 60)
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
        appleRoi = objBoxs[mIndex].rect()
        img.draw_rectangle(appleRoi)
        print("obj found")
    else:
        appleRoi = []
        print("obj not found!")
    print('\n')

# choose the max area for
