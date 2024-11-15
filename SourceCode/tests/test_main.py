import unittest
from unittest.mock import patch, Mock
import pandas as pd
from main import query_properties_with_openai, format_openai_query, format_properties_for_openai

class TestRealEstateChatbot(unittest.TestCase):
    @patch('main.openai.ChatCompletion.create')
    def test_query_properties_with_openai(self, mock_openai_create):
        # Sample dataset
        dataset = pd.DataFrame({
            'displayAddress': ['Location 1', 'Location 2'],
            'price': [500000, 750000],
            'sizeMin': [1200, 1500],
            'bedrooms': [2, 3],
            'bathrooms': [1, 2],
            'furnishing': ['Furnished', 'Unfurnished']
        })
        
        # Mocked attributes and results
        query = "2-bedroom furnished apartment"
        
        # Mock the OpenAI API response
        mock_openai_create.return_value = {
            'choices': [
                {'message': {'content': 'Here is a summary of matching properties'}}
            ]
        }
        
        # Run the function
        response = query_properties_with_openai(query, dataset)
        
        # Assertions
        self.assertIn('Here is a summary', response)
        mock_openai_create.assert_called_once()

    def test_format_openai_query(self):
        # Test data
        query = "Looking for a 2-bedroom apartment"
        top_results = "Property 1: Location, Price, etc."
        
        # Run the function
        messages = format_openai_query(query, top_results)
        
        # Assertions
        self.assertEqual(len(messages), 4)
        self.assertEqual(messages[0]["role"], "system")
        self.assertIn("User query:", messages[1]["content"])
    
    def test_format_properties_for_openai(self):
        # Sample data
        dataset = pd.DataFrame({
            'displayAddress': ['Location A', 'Location B'],
            'price': [500000, 700000],
            'sizeMin': [1000, 1200],
            'bedrooms': [2, 3],
            'bathrooms': [2, 3],
            'furnishing': ['Furnished', 'Unfurnished']
        })
        
        # Run the function
        formatted_text = format_properties_for_openai(dataset, max_results=2)
        
        # Assertions
        self.assertIn("Property 1: Location: Location A", formatted_text)
        self.assertIn("Property 2: Location: Location B", formatted_text)

if __name__ == '__main__':
    unittest.main()
