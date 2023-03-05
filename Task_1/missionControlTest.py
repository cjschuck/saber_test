import io
import sys
import unittest

class TestNumberPrinter(unittest.TestCase):
    

    def test_print_numbers(self):        
        printer = NumberPrinter(start=1, end=15)
        captured_output = io.StringIO()
        sys.stdout = captured_output
        printer.print_numbers()
        sys.stdout = sys.__stdout__
        expected_output = "1\n2\n3\nMission\nControl\nMission\n7\nControl\nMission\n11\nMission\nControl\nMission\n15\n"
        self.assertEqual(captured_output.getvalue(), expected_output)
if __name__ == '__main__':
    unittest.main()
