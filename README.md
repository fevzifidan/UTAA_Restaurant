# $${\color{#4cc9f0}UTAA \space Restaurant}$$
It is a real-time ordering application for a restaurant based on shape and color detection with OpenCV.

It allows you to order with lego shapes with various color and shape combinations. The lego shape shown to the camera is compared with the predefined lego shapes in the Menu directory. If the lego shown to the camera is available in the menu, the corresponding product can be added to the order list.

As stated in the program's project requirements, in order for the order to be completed, it is mandatory to select 1 product from the starter and 1 product from the main course category. In addition, it allows for at most one product to be selected from each category, again depending on the project requirements.

## Programming Languages and Modules Used
The project has been developed in Python and mainly uses OpenCV.

## Supported Languages
- English

## Customization
To remove the current limitations of the program and customize the way it works, you can update the **Main** and **Scan** classes according to your own needs.

In addition, to add new products to the menu or to change the legos of already added products, all you need to do is to add the .png images of your own lego designs to the **Menu** directory.

>[!Important]
>The lego shape corresponding to a product must have only one color, i.e. the shape must not consist of lego pieces with different colors.
>You can check the Menu directory for the naming of the files and examples.

## Screenshots
![Sample Screenshot 1](https://github.com/fevzifidan/UTAA_Restaurant/blob/main/Screenshots/utaa_restaurant_ss_1.png)

> [!Note]
> The live camera image (including the focus point) is intentionally censored, the actual image (including the focus point) is visible during program execution.

## Development Purpose and Use
This project was developed for educational purposes only and does not have any commercial purpose.

## About the Developer
- Fevzi FİDAN
