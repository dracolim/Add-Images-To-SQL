# Add Images to SQL Database
**Method used: <em>Base64</em> conversion**

Steps to Add images into SQL DB:
[in skills.sql]
1. Create a `image` column under the skill table in the sql file 
2. Insert values into skills table including image with Base64 
- To get Base64 images, you can use any available conversion website online to convert images to Base64
- https://codebeautify.org/image-to-base64-converter

[in app.py]
1. In create_skill function, include "image" into the data.keys()
<img width="435" alt="Screenshot 2022-10-15 at 11 23 30 PM" src="https://user-images.githubusercontent.com/85498185/195994463-01fc30dc-f27d-47ef-b101-0026f921154f.png">

[in skills.html]
1. under the  <!-- CREATE SKILL POP UP -->, include input type = file and v-on:change = `onChangeFile` to call the onChangefile whenever the user uploads an image
2. in the `onChangeFile` function, it calls the `createImage` function which will load and read the image as Base64 , and assigns it to the image variable
3. When showing the images, make sure to include "data:image/png;base64," in the img tag to convert Base64 to an image

That's All :)
