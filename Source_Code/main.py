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
    attributes = extract_attributes(query)
    matching_properties = search_properties(attributes, dataset)
    response = format_properties(matching_properties)
    return response
