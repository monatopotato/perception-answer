Answer.png

![answer](https://github.com/user-attachments/assets/b51126e6-7e37-4341-ae80-30dd313213ac)


Methodology:

  To get the answer, I firstly realized that the cones were all the same orange color, and I found the inRange() method from the cv2 package that will recreate a new image by filtering a specific color. Shown below, this was the new image I created to help me.

  ![detected_output](https://github.com/user-attachments/assets/9fb7bbfa-2a08-4d56-b11e-679586caa6ef)

  Once I obtained this image, I put a couple of filters on my image such as grayscale and blur to minimize the noise as there were a couple of patches of red similar to the cones. Once I cleaned the image up, I used the Canny() and findContours() method which first created edges around the cones and connected them to create an outline that represented a cone shaped object. As you can see below, the white outline represents the cone outlined from the two methods.

  ![edged](https://github.com/user-attachments/assets/6563532f-710e-4c8d-b65e-837f70b361b6)

Once I obtained this, I created a method that would calculate the mid points of each of the clusters by filtering out close points so there was only 1 point per cone. This would allow me to find a general location of where each cone is and allow me to draw a line through each of the cones once I find the midpoint of each of the cones. Once I found the midpoints of each cone I found the slope of both sides of the cones and then drew the lines accordingly.
