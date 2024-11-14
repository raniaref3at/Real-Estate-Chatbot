import unittest
import pandas as pd
from SourceCode.property_filter import search_properties

class TestPropertyFilter(unittest.TestCase):
    def setUp(self):
        self.dataset = pd.DataFrame({
            'bedrooms': [2, 3, 1],
            'bathrooms': [1, 2, 1],
            'displayAddress': ["Dubai", "Abu Dhabi", "Sharjah"],
            'price': [4500, 6000, 3000]
        })

    def test_search_properties(self):
        attributes = {'bedrooms': 3, 'price_max': 6000}
        result = search_properties(attributes, self.dataset)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['displayAddress'], "Abu Dhabi")

if __name__ == "__main__":
    unittest.main()
