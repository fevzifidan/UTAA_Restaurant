import cv2
import numpy as np

class Window:
    def __init__(self, restaurant_name):
        self.title = restaurant_name

        # We determine the keys to be captured during the process.
        self.complete_key = [27] # ESC
        self.approve_key = [32] # Space
        self.rst_stability = [114, 82] # r - R
        self.quit_key = [81, 113] # Q or q

    def show(self, frame, detected_text):
        height, width, channels = frame.shape

        # We determine some necessary properties of the subframe to be created.
        subframe_height = int(height*0.07)
        subframe_width = width

        # We determine 2 different colors for 2 kind of texts.
        if detected_text == "Product Approved!": dt_color = (0,255,0)
        else: dt_color = (0,0,255)

        # We create the subframe
        subframe = np.zeros((subframe_height, subframe_width, 3), dtype=np.uint8)

        # We place the necessary texts to the subframe
        cv2.putText(subframe, 'ESC: Complete -- Q: Quit/Cancel -- r: Reset Stability -- SPACE: Approve',
                    (10, subframe_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        cv2.putText(subframe, detected_text, (subframe_width - 120, subframe_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, dt_color, 1)

        # We combine frames (the original frame and subframe)
        frame = np.vstack((frame, subframe))

        # We show the frame
        cv2.imshow(self.title, frame)
        
        # We capture the returning key value
        key = cv2.waitKey(1)
        if key in self.complete_key:
            return -1
        elif key in self.approve_key:
            return 1
        elif key in self.rst_stability:
            return 0
        elif key in self.quit_key:
            return 2
        else:
            # We do not consider invalid keys
            pass

    def destroy(self):
        cv2.destroyAllWindows()

    def _place_focus_point(self, frame, center_coordinates, radius, color, thickness):
        """
        When capturing live images from the camera, we use a focus point to prevent the
        colors of irrelevant objects seen from the camera from being confused with the
        color of the main object. The scanned object is aligned on the focus point and
        the color is captured with this focus point.
        """
        # In this function, we place the focus point to be used during color detection.
        cv2.circle(frame, center_coordinates, radius, color, thickness)
        return frame


# END