## Real Estate Chatbot 
# Overview
This chatbot provides users with a quick, AI-powered search experience for real estate properties. It processes natural language queries (e.g., "2-bedroom in Dubai Marina under 500,000 AED") and retrieves relevant property data based on user criteria such as location, price, bedroom/bathroom count, and furnishing options.

# Setup
Prerequisites

Python 3.x
Required packages: pandas, openai
OpenAI Azure API key and endpoint
Configuration

Place api_key, azure_endpoint, api_version, and model information in a configuration file or modify them directly in the script.
Set the dataset_url to the path of the CSV file containing real estate data.
Installation

Install required packages:

`pip install pandas openai`
# Data File
Ensure that the dataset CSV (uae_real_estate_2024.csv) follows this structure:

Columns: displayAddress, price, sizeMin, bedrooms, bathrooms, furnishing
Place the dataset file in the root directory or specify the correct path in dataset_url.
Usage
# Initializing Chatbot

Load the dataset using `load_dataset()` to make property data available for queries.
Querying Properties

Use `query_properties(query)` with a natural language string like:

query_properties("Looking for a furnished 2-bedroom apartment in Dubai Marina under 700,000 AED.")
Example Workflow


dataset = load_dataset()  
result = query_properties("3-bedroom in Downtown Dubai under 1,000,000 AED")
print(result)
# Functionality
Natural Language Processing `(extract_attributes)`: Extracts user-requested attributes like bedrooms, price, and location using regex patterns.

Property Filtering `(search_properties)`: Filters dataset by attributes such as price range, bedroom/bathroom count, and location.

Output Formatting `(format_properties_for_openai)`: Formats properties into a user-friendly text, listing details for each matching property.

OpenAI API Call `(query_properties_with_openai)`: Sends the formatted message to OpenAI's GPT model to generate a response that summarizes search results in conversational language.

# Run the Code
Set the Azure OpenAI API Key: Open a terminal and set your Azure OpenAI API key as an environment variable. Use the following command (replace the example key with your actual API key):


`export AZURE_OPENAI_API_KEY="your_actual_api_key"`
To confirm that the key is set correctly, you can run:


`echo $AZURE_OPENAI_API_KEY`
Navigate to the Project Directory: Change your working directory to the folder containing the code files:


`cd /path/to/your/Real-Estate-Chatbot/SourceCode`
Run the Application: Use `Streamlit to run the frontend`


streamlit run frontend.py
Access the Application: Once Streamlit starts the server, it will display a URL in the terminal. Open the URL in a web browser to use the chatbot.

# Key Functions
`extract_attributes(query)` : Parses user’s query to extract search criteria.
`search_properties(attributes, dataset)` : Filters the dataset based on extracted attributes.
`format_openai_query(query, top_results)`: Structures messages for the OpenAI chat completion.
`query_properties_with_openai(query, dataset)`: Combines all steps, sending results to OpenAI to generate the final user-facing response.
Example Output
If a user asks for a “furnished 2-bedroom apartment in Dubai Marina under 500,000 AED,” the chatbot might respond:

“Here are some matching properties in Dubai Marina:
Property 1: Location: Dubai Marina, Price: 450,000 AED, Size: 1200 sq ft, Bedrooms: 2, Bathrooms: 1, Furnishing: Furnished.”

# Troubleshooting
API Errors: Ensure correct API key and endpoint.
Dataset Errors: Confirm CSV formatting and column names.
Regex Matching Issues: Customize regex patterns in attribute extraction functions if certain query formats are not recognized.
This documentation should guide you in using, modifying, and troubleshooting the real estate chatbot effectively.
