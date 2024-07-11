from datetime import datetime, timedelta

def etime(time, ltime, etime, n):
    if n == 0:
        etimec = time
        etimec = etimec - timedelta(minutes=5)
        ltimec = etimec + timedelta(minutes=5)
    else:
        etimec = ltime
        ltimec = etimec + timedelta(minutes=5)
    
    return etimec, ltimec




import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from your_module import etime  # Replace 'your_module' with the actual module name

class TestEtimeFunction(unittest.TestCase):

    @patch('your_module.timedelta', wraps=timedelta)  # Mocking timedelta
    def test_etime(self, mock_timedelta):
        # Test case for n == 0
        time = datetime(2023, 7, 11, 12, 0, 0)
        ltime = datetime(2023, 7, 11, 12, 10, 0)
        etime_val = datetime(2023, 7, 11, 12, 20, 0)
        n = 0
        
        etimec, ltimec = etime(time, ltime, etime_val, n)
        
        # Validate the results for n == 0
        self.assertEqual(etimec, time - timedelta(minutes=5))
        self.assertEqual(ltimec, time)
        
        # Ensure timedelta is called correctly
        mock_timedelta.assert_any_call(minutes=5)
        
        # Test case for n != 0
        n = 1
        
        etimec, ltimec = etime(time, ltime, etime_val, n)
        
        # Validate the results for n != 0
        self.assertEqual(etimec, ltime)
        self.assertEqual(ltimec, ltime + timedelta(minutes=5))
        
        # Ensure timedelta is called correctly again
        self.assertEqual(mock_timedelta.call_count, 4)

if __name__ == "__main__":
    unittest.main()
  
