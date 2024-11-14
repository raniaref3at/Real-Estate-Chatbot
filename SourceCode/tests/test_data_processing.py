import unittest
from Source_Code.backend.data_processing import load_dataset

class TestDataProcessing(unittest.TestCase):
    def test_load_dataset(self):
        dataset = load_dataset()
        self.assertIsNotNone(dataset)  # Check if dataset is loaded
        self.assertIn('displayAddress', dataset.columns)  # Check if expected column is present

if __name__ == "__main__":
    unittest.main()
