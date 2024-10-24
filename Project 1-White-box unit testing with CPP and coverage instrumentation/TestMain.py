# TestMain.py

import unittest
from TestAll import AllTest  # Import the StudentTest class from student_test.py
if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(AllTest)
    # Create a test runner
    runner = unittest.TextTestRunner()
    # Run the tests
    result = runner.run(suite)
    # Check if the tests were successful
    if result.wasSuccessful():
        print("All tests passed!")
        exit_code = 0
    else:
        print("Some tests failed.")
        exit_code = 1
    exit(exit_code)
