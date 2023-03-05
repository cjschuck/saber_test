# Define a class called NumberPrinter
class NumberPrinter:
    
    def __init__(self, start=1, end=75):
        self.start = start
        self.end = end
    
    # Define a method called print_numbers that prints numbers and messages based on requested conditions
    def print_numbers(self):
        for i in range(self.start, self.end+1):
            # If the number is divisible by 4 and 7, print "Mission Control"
            if i % 4 == 0 and i % 7 == 0:
                print("Mission Control")
            # If the number is divisible by 4, print "Mission"
            elif i % 4 == 0:
                print("Mission")
            # If the number is divisible by 5, print "Control"
            elif i % 5 == 0:
                print("Control")
            else:
                print(i)

# Create an instance of the NumberPrinter class with the default values for start and end
printer = NumberPrinter()

# Call the print_numbers method of the NumberPrinter instance to print the numbers and messages
printer.print_numbers()
