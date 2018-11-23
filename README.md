# How to make a Robot PICKING APPLE in just one night?

This small project is made for fun (turned out not, though). I'll focus on the CV part of this project.

I took over this small project for fun about two months ago. At first, another guy in the mechanical team gave me a fruit-picking robot and want me& another hardware guy, Jessy, to automate the process of the picking. They would use this robot as the entry for another competition. The task is not difficult, all we need to do is add a camera for this little guy and instruct it moving to the target fruit with our program. I was in charge of the whole computer vision part so I only need to write the codes for object detection.

But this “just for fun” thing suddenly turned tricky ‘cause we both forgot it for the whole summer vacation until two days before the deadline of uploading the video of our robot.

So me and Jessy had to make a robot picking apple in just one night.

HOW TO DO IT?

## 0. What we need to do exactly?

### How the system works?
Me and Jessy are the teammate of an robot competition last year(Robomaster, it's pretty cool). In that competition a critical module of the robot(we call it Infantry) is "Auto-shooting" － Infantries detect the target area and turn their "barrel"(Yes they shoot plastic bullets) to it. (CV part of this project is open source right now, If you're interested, [check this](https://github.com/SEU-SuperNova-CVRA/Robomaster2018-SEU-OpenSource))

This sub-system can be simplified as **"vision detect - servo control"**. The detection program receives the image data from the camera, process it, and returns the position of target to the control program.

(fig)
And here is what the competition robot & this fruit-picking robot look like.

 (fig) 
As you can see, they share very familiar structure: chassis and a multiple-degree-of-freedom PTZ that execute the main task. So chill out, cause' it's just another simplified Infantry. Or at least we thought it was.
### Prepare everything
#### 1. Hardware
Normally, OPENCV(a powerful computer vision library) is the first thing jump out of your head. Sad story: we didn't have the TIME or MONEY to find an embedded device with the development environment we need.

Luckily I found OpenMV. This board is intergrated with a camera, and provides their own image-processing library(Check for more [details]()), maybe less powerful, but enough for this project. Anyway, this board is in charge of the image processing.

The control system runs on an ARM board. Clearly, the result of image processing should be passed to it. This is Jessy's job, but we both need to write a communication protocol, so I still need to know more about the UART module of my OpenMV.

#### 2.Software
For the vision part, all we need to do is install an IDE for the OpenMV. Have to say, their IDE is REALLY convinient for simple vision development task, ESPECIALLY for this project. You'll know the reason soon.
#### 3.Others
Obviously we don't need to let the robot pick up every fruit it meets!! We just need it succeed in picking one fake fruit. So this is the target we look for.
(fig)

## 1. Learn how to use OpenMV
