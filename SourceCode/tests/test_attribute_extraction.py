import unittest
from SourceCode.attribute_extraction import extract_attributes

class TestAttributeExtraction(unittest.TestCase):
    def test_extract_bed_bath(self):
        query = "3 bedroom and 2 bathroom in Dubai"
        attributes = extract_attributes(query)
        self.assertEqual(attributes['bedrooms'], 3)
        self.assertEqual(attributes['bathrooms'], 2)

    def test_extract_price_range(self):
        query = "apartments under 5000 AED"
        attributes = extract_attributes(query)
        self.assertEqual(attributes['price_max'], 5000)

    def test_extract_location(self):
        query = "villa in Abu Dhabi"
        attributes = extract_attributes(query)
        self.assertEqual(attributes['displayAddress'], "Abu Dhabi")

if __name__ == "__main__":
    unittest.main()
