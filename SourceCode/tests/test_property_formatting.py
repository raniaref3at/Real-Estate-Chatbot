import unittest
import pandas as pd
from Source_Code.backend.property_formatting import format_properties

class TestPropertyFormatting(unittest.TestCase):
    def test_format_properties(self):
        properties = pd.DataFrame({
            'displayAddress': ["Dubai"],
            'price': [5000],
            'sizeMin': [800],
            'bedrooms': [2],
            'bathrooms': [2],
            'furnishing': ["Furnished"]
        })
        response = format_properties(properties)
        self.assertIn("Location: Dubai", response)
        self.assertIn("Price: 5000 AED", response)

if __name__ == "__main__":
    unittest.main()
