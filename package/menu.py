import cv2
import os

class Menu:
    # In this class, we create the menu by accessing the products
    # in menu_address
    def __init__(self, menu_address):
        # sample_file_name (name_category_price_shape): sutlac_green_60_square
        self.menu_path = menu_address
        self.object_list = os.listdir(self.menu_path)
        self.object_names = []
        self.__price = []
        self.__color = []
        self.shape = []
        self.images = []
        self.menu = dict()

        for item in self.object_list:
            # Get the file name without extension
            fileName, fileExtension = os.path.splitext(item)

            if fileExtension.casefold() != ".png":
                # We skip unexpected files and folders in the directory where
                # the images corresponding to the products should be located.
                continue

            # Split fileName to extract properties (name_category_price_shape)
            properties = fileName.split("_")
            if len(properties) != 4:
                # That means that the file name does not obey the naming rule
                # Ignore and continue
                pass
            else:
                self.object_names.append(properties[0])
                # categories are differentiated by colors
                self.__color.append(properties[1])
                self.__price.append(properties[2])
                self.shape.append(properties[3])

                current_image = cv2.imread(os.path.join(self.menu_path, item), 0)
                self.images.append(current_image)

        self.__create_menu()

    def __create_menu(self):
        for i in range(len(self.object_names)):
            self.menu[self.object_names[i]] = (self.object_names[i], self.__color[i], self.__price[i])

    def get_name(self, color, shape):
        # When the color and shape are given, this function returns the name of the product
        # which has these properties
        color_indexes = []
        index = 0
        try:
            for clr in self.__color:
                if clr.casefold() == color.casefold():
                    color_indexes.append(index)
                index += 1

            for index in color_indexes:
                if self.shape[index] == shape:
                    return self.object_names[index]
        except AttributeError:
            # This error can possibly occur, we return None in a controlled manner.
            return None
        return None


# END