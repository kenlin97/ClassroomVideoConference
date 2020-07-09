# ClassroomVideoConference
ClassCV

This application's purpose is to add hand gesture and sleep detection functionality to classroom lectures. 
The hand gestures in this program include hand raising and thumbs up and down. This was done through creating a mask after image processing. 
For sleep detection, the program uses the DLIB library to detect the facial landmarks and uses the eye coordinates to determine whether the user is sleeping. (Reference: https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/)

To use this application, clone the entire folder and make sure all necessary modules are downloaded. I used python 3.6

The main.py is the file that should be used to run the entire program. Colorpicker.py is what I used to find the correct color values and alert.py contains the functions related to the alarm and math problem generated. 

Challenges: 
An issue that I ran into for this project was the detection of the hand color. After changing the HSV values many times, I got it to work with the current setup I had.
However, after attempting to get it working on my other laptops with varying displays, the hand detection wasn't accurate. The HSV values had to be adjust appropiately. 
Another issue I ran into was getting the application output to act as the webcam output. In the end, I figured to use OBS's virtual cam software to emulate the window as the webcam output. 

Future work: 
As this was my first project with openCV, I plan to use other methods to detect hand gestures like machine learning for better results. 
Hopefully I can get the webcam output figured out to create a fully functional program that everyone can use. 

