import os
api_key = os.getenv("AZURE_OPENAI_API_KEY")
#api_key=<"7uvNPwVoyFgg2xF2LqCF3CGcvEMTVEBwz0eduSlJOz7ssb7x5hMbJQQJ99AKACF24PCXJ3w3AAABACOGKpz3">
azure_endpoint="https://assessment.openai.azure.com/"
api_version="2024-10-21"
model="gpt-4" 
dataset_url = "uae_real_estate_2024.csv"

column_mapping = {
    'bedrooms': 'bedrooms',
    'bathrooms': 'bathrooms',
    'displayAddress': 'displayAddress',
    'price': 'price',
    'sizeMin': 'sizeMin',
    'furnishing': 'furnishing'
}