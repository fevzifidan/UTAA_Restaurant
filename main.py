r"""
This project has been developed and tested for
'SENG 211 - Object Oriented Programming' course.
"""

try:
    import cv2
    import time
    from os import path
    from package.detector import Detector
    from package.menu import Menu
    from package.order import Order
    from package.printer import Printer
    from package.scanner import Scan
    from package.stability import Stability
    from package.window import Window
except Exception as e:
    errMsg = "One or more crucial modules for this program to run could not be imported!\n"\
        f"Error Message: {e}"
    raise ImportError(errMsg)

class Main:
    def __init__(self, menu_address, color_address, cameraIndex = 0, tk_messages = True, restaurant_name = "UTAA Restaurant"):
        self.menu_address = menu_address
        self.color_address = color_address
        self.cameraIndex = cameraIndex
        self.tk_messages = tk_messages
        self.restaurant_name = restaurant_name
    
    def initialize(self):
        # We start the whole process here, and we end it here.

        menu = Menu(self.menu_address)
        order = Order()
        window = Window(self.restaurant_name)
        detector = Detector(self.color_address)
        stability = Stability(menu)
        printer = Printer(self.tk_messages)

        printer.print_trmnl(f"Welcome to {self.restaurant_name}")

        cap = cv2.VideoCapture(self.cameraIndex)
        scan = Scan(window, detector, stability, printer, cap, menu, order)

        # We catch the value corresponding to the data which states whether the order is
        # completed or not.
        order_completed = scan.start()

        cap.release()

        if order_completed:
            # Show orders and their prices
            printer.print_trmnl("Here are your orders:")
            for product in order.showOrder():
                printer.print_trmnl(f"\t{product[0].capitalize()} -> {product[2]} TL")
            
            # Show total order cost
            printer.print_trmnl(f"Your Fee: {order.calculateOrderFee()} TL")

            while True:
                ans = input("Do you confirm your order? Yes (y) or No (n): ")
                if ans.casefold() == "y":
                    # Here, time.sleep(2) provides a demonstration by creating a
                    # 2-second delay between sequential processes
                    printer.print_trmnl("Payment confirmed!")
                    time.sleep(2)

                    # Get the list of the ordered products
                    products = order.showOrder()

                    # Loop through the products and show a preparation message for each of them
                    for product in products:
                        printer.print_trmnl(f"Your {product[0].capitalize()} is being prepared...")
                        time.sleep(2)

                    printer.print_trmnl("Your meals are being served!")
                    time.sleep(2)

                    printer.print_trmnl("\nProcess completed!\nThank you for choosing us!")
                    break
                
                elif ans.casefold() == "n":
                    printer.print_trmnl("Sorry, the order has been cancelled! :(")
                    break
                else:
                    printer.print_trmnl("Please give a valid answer! (y, Y, n, N)")
        else:
            """
            We assume that the failure to complete the order which can handle to reach this stage can
            only occur when the customer terminates the program, otherwise another error is thrown before
            reaching this stage.
            """
            pass

if __name__ == "__main__":
    menu_address = path.join(path.dirname(__file__), "Menu")
    color_address = path.join(path.dirname(__file__), "colors.json")
    main = Main(menu_address=menu_address, color_address = color_address, cameraIndex = 0, tk_messages = True)
    main.initialize()


# END
