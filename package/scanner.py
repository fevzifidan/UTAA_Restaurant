import time
from cv2 import getWindowProperty, WND_PROP_VISIBLE

class Scan:

    def __init__(self, window, detector, stability, printer, capture, menu, order):
        # Here, we create the necessary objects to be used.

        self.window = window
        self.detector = detector
        self.stability = stability
        self.printer = printer
        self.cap = capture
        self.menu = menu
        self.order = order
    
    def start(self):
        """
        'last_approve_time' is used to measure the time since the last approval to show the text "Product Approved"
        for a certain period of time.
        """
        last_approve_time = 0

        # It is important to hold the data about that whether the order is completed or not (process aborted).
        order_completed = False
        while True:
            ret, frame = self.cap.read()
            
            if ret == False:
                errMsg = "We couldn't access your camera. They may an issue with permissions or you may forget to set the correct camera index."
                self.printer.print_error(errMsg)
                self.printer.print_trmnl("The program has been terminated due to an error appearing while starting scanning!")
                break
            
            # We detect the color and shape of the given input sequentially.
            color, _frame = self.detector.detect_color(frame, self.window)
            shape = self.detector.detect_shape(frame, self.menu)
            
            # To get the most stable value, we add the returning color and shape data (other than None) to the
            # corresponding stability lists.
            if color != None and shape != None:
                self.stability.color_stability_list.append(color); self.stability.shape_stability_list.append(shape)
            
            # We get the most stable value
            stable_order = self.stability.get_stable_order(shape, color)

            # When a product is approved, we show 'Product Approved' message for 2.5 seconds
            if time.time() - last_approve_time < 2.5:
                stable_order = "Not Detected!"
                detected_text = "Product Approved!"
                self.stability.reset()
            else:
                if stable_order == None:
                    stable_order = "Not Detected!"
                detected_text = stable_order
            
            rtrn_code = self.window.show(_frame, detected_text)
            
            # According to the returning 'rtrn_code' we continue the process.
            if rtrn_code == 1:
                # Attempt: Approve

                # If stable_order is 'Not Detected' then ignore
                if stable_order != "Not Detected!":
                    # Check if an order has already been placed in the current category
                    same_category, product = self.order.sameCategory(self.menu.menu[stable_order][1])
                    if same_category:
                        if stable_order != product[0]:
                            # If the current product is not the same as the previous one then
                            # give the customer a chance to change their previous order
                            question = "You cannot order more than 1 product in the same category! "\
                                    "Do you want to change your previous order to the new one?"
                            ans = self.printer.print_question_yn(f"""{question}\n{product[0]} => {stable_order}""")
                            if ans == True:
                                # If they want to change the old product with the new one
                                self.order.changeOrder(product, self.menu.menu[stable_order])
                                self.printer.print_trmnl(f"Customer changed their order '{product[0].capitalize()}' to '{stable_order.capitalize()}'.")
                        else:
                            # If the existing product has already been ordered
                            self.printer.print_warning("You have already ordered this product!")
                    else:
                        # Approve new order
                        self.printer.print_trmnl(f"Customer Ordered: {stable_order.capitalize()}")
                        self.order.addToOrder(self.menu.menu[stable_order])
                        last_approve_time = time.time()

                    self.printer.print_trmnl(f"Total Number of Products Ordered: {self.order.totalOrderedProductNumber()}")
                self.stability.reset()
            
            elif rtrn_code == -1:
                # Attempt: Complete

                ordered_main_course = self.order.orderTypeList.count("Red")
                ordered_starter = self.order.orderTypeList.count("Green")
                if self.order.totalOrderedProductNumber() == 0:
                    msg = "You have not chosen any products/meals! "\
                        "You can order some products or you can quit the program and terminate the process."
                    self.printer.print_warning(msg)
                
                # It is mandatory to order 1 main course and 1 starter to complete the order.
                elif ordered_main_course + ordered_starter != 2:
                    msg = "You have to choose at least 1 main course and 1 starter!\n"\
                        "Selected Meals:\n\t"\
                        f"Main Course: {ordered_main_course} ordered, {1 - ordered_main_course} remaining.\n\t"\
                        f"Starter: {ordered_starter} ordered, {1 - ordered_starter} remaining."
                    self.printer.print_warning(msg)
                else:
                    # If the order is eligible for confirmation
                    ans = self.printer.print_question_yn("Are you sure that you want to complete the scanning?")
                    if ans == True:
                        self.window.destroy()
                        order_completed = True
                        return order_completed
                    
            elif rtrn_code == 0:
                # Attempt: Reset Stability
                self.stability.reset()
            
            elif rtrn_code == 2:
                # Attempt: Quit
                ans = self.printer.print_question_yn("Are you sure that you want to quit/cancel the program?")
                if ans == True:
                    self.window.destroy()
                    return order_completed
            
            else:
                # Attempt: Close the window manually
                if getWindowProperty(self.window.title, WND_PROP_VISIBLE) < 1:
                    self.window.destroy()
                    # Return False to stop the program from running completely
                    return False


# END