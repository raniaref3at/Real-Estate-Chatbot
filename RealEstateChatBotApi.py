import openai
import pandas as pd
import re

api_key = "7uvNPwVoyFgg2xF2LqCF3CGcvEMTVEBwz0eduSlJOz7ssb7x5hMbJQQJ99AKACF24PCXJ3w3AAABACOGKpz3"
azure_endpoint = "https://assessment.openai.azure.com/"
api_version = "2024-10-21"
model = "gpt-4"

openai.api_type = "azure"
openai.api_base = azure_endpoint
openai.api_version = api_version
openai.api_key = api_key

dataset_url = "uae_real_estate_2024.csv"
dataset = pd.read_csv(dataset_url)

dataset.columns = dataset.columns.str.strip()

column_mapping = {
    'bedrooms': 'bedrooms',
    'bathrooms': 'bathrooms',
    'displayAddress': 'displayAddress',
    'price': 'price',
    'sizeMin': 'sizeMin',
    'furnishing': 'furnishing'
}

def extract_attributes(query):
    attributes = {
        'bedrooms': None,
        'bathrooms': None,
        'displayAddress': None,
        'price_min': None,
        'price_max': None
    }

    attributes = extract_bed_bath(query, attributes)

    attributes = extract_price_range(query, attributes)

    attributes = extract_location(query, attributes)

    return attributes

def extract_bed_bath(query, attributes):
    if re.search(r'(\d+)\s*bedroom', query, re.IGNORECASE):
        attributes['bedrooms'] = int(re.search(r'(\d+)\s*bedroom', query, re.IGNORECASE).group(1))
    if re.search(r'(\d+)\s*bathroom', query, re.IGNORECASE):
        attributes['bathrooms'] = int(re.search(r'(\d+)\s*bathroom', query, re.IGNORECASE).group(1))
    return attributes

def extract_price_range(query, attributes):
    if re.search(r'under (\d+)', query, re.IGNORECASE):
        attributes['price_max'] = int(re.search(r'under (\d+)', query, re.IGNORECASE).group(1))
    elif re.search(r'(\d+)\s*(AED|dirhams)?\s*or\s*less', query, re.IGNORECASE):
        attributes['price_max'] = int(re.search(r'(\d+)\s*(AED|dirhams)?\s*or\s*less', query, re.IGNORECASE).group(1))
    return attributes

def extract_location(query, attributes):
    location_match = re.search(r'\b(?:in|at|near)\s+(\w+(?:\s+\w+)*)', query, re.IGNORECASE)
    if location_match:
        attributes['displayAddress'] = location_match.group(1).strip()
    return attributes

def search_properties(attributes, dataset):
    filtered_properties = dataset

    filtered_properties = filter_by_attributes(filtered_properties, attributes)

    return filtered_properties

def filter_by_attributes(filtered_properties, attributes):
    if attributes['bedrooms']:
        filtered_properties = filtered_properties[filtered_properties['bedrooms'].astype(str).str.contains(str(attributes['bedrooms']), case=False, na=False)]

    if attributes['bathrooms']:
        filtered_properties = filtered_properties[filtered_properties['bathrooms'].astype(str).str.contains(str(attributes['bathrooms']), case=False, na=False)]

    if attributes['displayAddress']:
        filtered_properties = filtered_properties[filtered_properties['displayAddress'].str.contains(attributes['displayAddress'], case=False, na=False)]

    if attributes['price_max']:
        filtered_properties = filtered_properties[filtered_properties['price'].astype(int) <= attributes['price_max']]

    return filtered_properties

def format_properties(properties, max_results=5):
    if properties.empty:
        return "Sorry, no properties match your criteria."
    
    response = "Based on your criteria, these are the properties that best match you : \n"
    properties = properties.head(max_results)

    for index, (_, row) in enumerate(properties.iterrows(), start=1):
        response += f"\n{index}_Location: {row['displayAddress']}\n"
        response += f"\nPrice: {row['price']} AED\n"
        response += f"\nSize: {row['sizeMin']} sq ft\n"
        response += f"\nBedrooms: {row['bedrooms']}\n"
        response += f"\nBathrooms: {row['bathrooms']}\n"
        response += f"\nFurnishing: {row['furnishing']}\n\n"
    
    return response