import unittest
from Source_Code.backend.main import query_properties

class TestMain(unittest.TestCase):
    def test_query_properties(self):
        query = "Find a 2-bedroom apartment in Dubai under 5000 AED"
        response = query_properties(query)
        self.assertIn("Dubai", response)
        self.assertIn("5000 AED", response)

if __name__ == "__main__":
    unittest.main()
