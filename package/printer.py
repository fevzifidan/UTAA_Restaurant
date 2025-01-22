from tkinter import messagebox

class Printer:
    # To effectively interact with the customer, or the user of the program, we
    # use both terminal and message boxes.

    def __init__(self, tk_messages):
        # We determine whether message boxes will be used or not according to
        # the tk_messages value.
        self.tk_messages = tk_messages

    # Following functions provide several types of demonstrations of messages.

    def print_info(self, message):
        # Show information/informative message
        print(f"Info: {message}")
        if self.tk_messages: return messagebox.showinfo("Information", message)
    
    def print_warning(self, message):
        # Show warning message
        print(f"Warning: {message}")
        if self.tk_messages: return messagebox.showwarning("Warning", message)

    def print_error(self, message):
        # Show error message
        print(f"Error: {message}")
        if self.tk_messages: return messagebox.showerror("Error", message)

    def print_trmnl(self, message):
        # Just print message to terminal
        print(f"Message: {message}")

    def print_question_yn(self, message):
        # Ask a Yes/No question
        if self.tk_messages: return messagebox.askyesno("Question", message)
        ans = input(f"{message}: ")
        if ans.casefold() == "y": return True
        else: return False
    
    def print_question_oc(self, message):
        # Ask an Ok/Cancel question
        return messagebox.askokcancel("Question", message)


# END