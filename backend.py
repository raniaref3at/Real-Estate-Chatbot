import openai
import pandas as pd
import re

# Azure OpenAI configuration
api_key = "7uvNPwVoyFgg2xF2LqCF3CGcvEMTVEBwz0eduSlJOz7ssb7x5hMbJQQJ99AKACF24PCXJ3w3AAABACOGKpz3"
azure_endpoint = "https://assessment.openai.azure.com/"
api_version = "2024-10-21"
model = "gpt-4"

# Set up OpenAI client with Azure-specific configurations
openai.api_type = "azure"
openai.api_base = azure_endpoint
openai.api_version = api_version
openai.api_key = api_key

# Load the UAE Real Estate dataset
dataset_url = "/content/sample_data/uae_real_estate_2024.csv"
dataset = pd.read_csv(dataset_url)

# Strip spaces from column names to avoid issues
dataset.columns = dataset.columns.str.strip()

# Column mapping for attributes (adjusted to lowercase as per dataset)
column_mapping = {
    'bedrooms': 'bedrooms',
    'bathrooms': 'bathrooms',
    'displayAddress': 'displayAddress',
    'price': 'price',
    'sizeMin': 'sizeMin',
    'furnishing': 'furnishing'
}

# Function to extract attributes from the user query using regex or other NLP methods
def extract_attributes(query):
    attributes = {
        'bedrooms': None,
        'bathrooms': None,
        'displayAddress': None,
        'price_min': None,
        'price_max': None
    }

    # Extract bedrooms and bathrooms
    if re.search(r'(\d+)\s*bedroom', query, re.IGNORECASE):
        attributes['bedrooms'] = int(re.search(r'(\d+)\s*bedroom', query, re.IGNORECASE).group(1))
    if re.search(r'(\d+)\s*bathroom', query, re.IGNORECASE):
        attributes['bathrooms'] = int(re.search(r'(\d+)\s*bathroom', query, re.IGNORECASE).group(1))

    # Extract price range
    if re.search(r'under (\d+)', query, re.IGNORECASE):
        attributes['price_max'] = int(re.search(r'under (\d+)', query, re.IGNORECASE).group(1))
    elif re.search(r'(\d+)\s*(AED|dirhams)?\s*or\s*less', query, re.IGNORECASE):
        attributes['price_max'] = int(re.search(r'(\d+)\s*(AED|dirhams)?\s*or\s*less', query, re.IGNORECASE).group(1))

    # Extract city or location dynamically
    # Get the city mentioned in the query
    city_match = re.search(r'(dubai|abu dhabi|sharjah|ajman|ras al khaimah|fujairah|umm al quwain)', query, re.IGNORECASE)
    if city_match:
        attributes['displayAddress'] = city_match.group(0).capitalize()  # Get the first match and capitalize it

    return attributes


# Function to search properties in the dataset
def search_properties(attributes, dataset):
    filtered_properties = dataset
    
    # Filter by bedrooms
    if attributes['bedrooms']:
        filtered_properties = filtered_properties[
            filtered_properties['bedrooms'].astype(str).str.contains(str(attributes['bedrooms']), case=False, na=False)
        ]
    
    # Filter by bathrooms
    if attributes['bathrooms']:
        filtered_properties = filtered_properties[
            filtered_properties['bathrooms'].astype(str).str.contains(str(attributes['bathrooms']), case=False, na=False)
        ]
    
    # Filter by location (city)
    if attributes['displayAddress']:
        filtered_properties = filtered_properties[
            filtered_properties['displayAddress'].str.contains(attributes['displayAddress'], case=False, na=False)
        ]
    
    # Filter by price (if max price is specified)
    if attributes['price_max']:
        filtered_properties = filtered_properties[
            filtered_properties['price'].astype(int) <= attributes['price_max']
        ]
    
    return filtered_properties

# Format the output for a better user-friendly display
def format_properties(properties, max_results=5):
    if properties.empty:
        return "Sorry, no properties match your criteria."

    # Limit the number of results displayed
    properties = properties.head(max_results)

    # Creating a user-friendly summary for each property
    result = ""
    for index, row in properties.iterrows():
        result += f"\nProperty {index + 1}:\n"
        result += f"Location: {row['displayAddress']}\n"
        result += f"Price: {row['price']} AED\n"
        result += f"Size: {row['sizeMin']} sq ft\n"
        result += f"Bedrooms: {row['bedrooms']}\n"
        result += f"Bathrooms: {row['bathrooms']}\n"
        result += f"Furnishing: {row['furnishing']}\n"
        result += "-" * 20
    
    # Indicate if there are more results
    if len(properties) == max_results:
        result += "\n... (more results available)"
    
    return result

# Handle user input and fetch real estate info
def handle_query(query):
    user_attributes = extract_attributes(query)
    matching_properties = search_properties(user_attributes, dataset)
    
    return format_properties(matching_properties)

# Example user query (user can enter this freely)
user_query = input("Enter your query: ")
response = handle_query(user_query)
print(response)
