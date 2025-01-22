import cv2
import json

class Detector:

    def __init__(self, color_address):
        self.color_address = color_address
        try:
            with open(color_address, "r") as colorFile:
                self.colors = json.load(colorFile)
        except Exception as e:
            errMsg = "We encountered a problem while trying to open/read the color_address!\n"\
                    f"color_address = {color_address} | {type(color_address)}\n"\
                    f"Error Message: {e}"
            raise Exception(errMsg)

    def detect_color(self, frame, window):
        # We will use HSV color spaces for color detection,
        # that's why we perform a transition from BGR to HSV.
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # We calculate the center coordinates
        height, width, _ = frame.shape
        cx = int(width/2)
        cy = int(height/2)

        # We place the focus point in the center of the screen
        _frame = window._place_focus_point(frame, (cx,cy), 5, (234,255,0), 3)

        # We get the color from a single point, that is, from the center.
        pixel_center = hsv_frame[cy, cx]
        hue_value = pixel_center[0]
        saturation = pixel_center[1]
        value = pixel_center[2]

        color = None

        # Get the colors read from .json file (color_address)

        black = self.colors["Black"]
        white = self.colors["White"]
        red_1 = self.colors["Red_1"]
        red_2 = self.colors["Red_2"]
        orange = self.colors["Orange"]
        yellow = self.colors["Yellow"]
        green = self.colors["Green"]
        blue = self.colors["Blue"]
        purple = self.colors["Purple"]
        pink = self.colors["Pink"]

        """
        For black, 'value' is enough; for white, 'saturation' is enough;
        and for the other colors, we just consider the 'hue value's.
        This conclusion was obtained by examining a graph containing hsv color spaces.
        """

        # Compare hue - saturation - value with color ranges

        if black["lowerLimit"] < value < black["upperLimit"]: color = "Black"
        elif white["lowerLimit"] < saturation < white["upperLimit"]: color = "White"
        elif red_1["lowerLimit"] < hue_value < red_1["upperLimit"]: color = "Red"
        elif red_2["lowerLimit"] < hue_value < red_2["upperLimit"]: color = "Red"
        elif orange["lowerLimit"] < hue_value < orange["upperLimit"]: color = "Orange"
        elif yellow["lowerLimit"] <= hue_value < yellow["upperLimit"]: color = "Yellow"
        elif green["lowerLimit"] <= hue_value < green["upperLimit"]: color = "Green"
        elif blue["lowerLimit"] <= hue_value < blue["upperLimit"]: color = "Blue"
        elif purple["lowerLimit"] <= hue_value < purple["upperLimit"]: color = "Purple"
        elif pink["lowerLimit"] <= hue_value < pink["upperLimit"]: color = "Pink"
        else: color = None

        # We return both color and the frame where the focus point is shown in the center of the frame.
        return color, _frame

    def detect_shape(self, frame, menu):
        # We convert the frame to the suitable format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Initiate ORB (Oriented FAST and Rotated BRIEF) detector
        orb = cv2.ORB.create(nfeatures=1000)

        def findDescriptor(images):
            # We find the descriptor of each given image and store them in a list.
            descriptorList=[]
            for img in images:
                # Find the keypoints and descriptors with ORB
                kp, des = orb.detectAndCompute(img, None)
                descriptorList.append(des)
            return descriptorList

        def findID(img, descriptorList, thres=15):
            kp2, des2 = orb.detectAndCompute(img, None)
            # BFMatcher (Brute-Force Matcher) with default params
            bf = cv2.BFMatcher()
            matchList = []
            finalVal = None
            try:
                for descripter in descriptorList:
                    # Find 2 nearest neighbour and get the matches
                    matches = bf.knnMatch(descripter, des2, k=2)
                    # Apply ratio test
                    good = []
                    for m,n in matches:
                        if m.distance < 0.75 * n.distance:
                            good.append([m])
                    matchList.append(len(good))
            except:
                """
                The error that might occur here is most likely caused
                by the function bf.knnMatch(). Most likely, the error
                occurred because of a possible incompatibility in instant
                parameters assigned to the function during the loop. We
                pass and continue to scan assuming that the error is
                instant and temporary.
                """
                pass

            if len(matchList)!=0:
                if max(matchList) > thres:
                    finalVal = matchList.index(max(matchList))
            return finalVal
        
        descriptorList = findDescriptor(menu.images)
        id = findID(frame, descriptorList, thres=10)
        
        if id != None: return menu.shape[id]
        else: return None


# END