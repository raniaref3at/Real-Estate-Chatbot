import openai
from settings import api_key, azure_endpoint, api_version, model
from data_processing import load_dataset
from attribute_extraction import extract_attributes
from property_filter import search_properties
from property_formatting import format_properties

openai.api_type = "azure"
openai.api_base = azure_endpoint
openai.api_version = api_version
openai.api_key = api_key

dataset = load_dataset()

def query_properties(query):
    return query_properties_with_openai(query, dataset)

def query_properties_with_openai(query, dataset):
    attributes = extract_attributes(query)
    matching_properties = search_properties(attributes, dataset)

    top_results = format_properties_for_openai(matching_properties)

    messages = [
        {"role": "system", "content": "You are a helpful real estate assistant."},
        {"role": "user", "content": f"User query: '{query}'"},
        {"role": "assistant", "content": f"Matching properties:\n{top_results}"},
        {"role": "user", "content": "Generate a user-friendly response summarizing these results."}
    ]

    response = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        max_tokens=150,
        temperature=0.5
    )

    return response['choices'][0]['message']['content'].strip()

def format_properties_for_openai(properties, max_results=5):
    properties = properties.head(max_results)
    formatted_text = ""

    for index, (_, row) in enumerate(properties.iterrows(), start=1):
        formatted_text += (
            f"Property {index}: Location: {row['displayAddress']}, "
            f"Price: {row['price']} AED, Size: {row['sizeMin']} sq ft, "
            f"Bedrooms: {row['bedrooms']}, Bathrooms: {row['bathrooms']}, "
            f"Furnishing: {row['furnishing']}.\n"
        )

    return formatted_text