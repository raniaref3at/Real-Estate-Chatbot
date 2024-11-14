import streamlit as st
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
dataset_url = "uae_real_estate_2024.csv"
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

    # Extract location similar to other entities
    location_match = re.search(r'\b(?:in|at|near)\s+(\w+(?:\s+\w+)*)', query, re.IGNORECASE)
    if location_match:
        attributes['displayAddress'] = location_match.group(1).strip()

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

# Format the output for a more organized display with numbered listings
def format_properties(properties, max_results=5):
    if properties.empty:
        return "Sorry, no properties match your criteria."
    
    response = ""
    
    # Limit the number of results displayed
    properties = properties.head(max_results)

    # Create a more organized and readable output
    for idx, row in properties.iterrows():
        response += f"Location: {row['displayAddress']}\n"
        response += f"Price: {row['price']} AED\n"
        response += f"Size: {row['sizeMin']} sq ft\n"  # Correct the size unit
        response += f"Bedrooms: {row['bedrooms']}\n"
        response += f"Bathrooms: {row['bathrooms']}\n"
        response += f"Furnishing: {row['furnishing']}\n\n"
    
    return response





# Function to handle chat history
def handle_query(query, chat_history):
    user_attributes = extract_attributes(query)
    matching_properties = search_properties(user_attributes, dataset)
    response = format_properties(matching_properties)

    chat_history.append(f"You: {query}")
    chat_history.append(f"Bot: {response}")
    return chat_history

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS to fix the text box and send button at the bottom
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 90vh;
            padding-bottom: 60px;  /* space for the fixed input and button */
        }
        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
        }
        .user-message {
            background-color: #FFFFFF;
            color: black;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 10px;
            font-size: 14px;
        }
        .bot-message {
            background-color: #D3D3D3;
            color: black;
            padding: 10px;
            margin-bottom: 5px;
            border-radius: 10px;
            font-size: 14px;
        }
        .input-container {
            display: flex;
            position: fixed;
            bottom: 10px;
            left: 10px;
            right: 10px;
            background-color: white;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        .input-box {
            flex-grow: 1;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #ddd;
        }
        .send-button {
            margin-left: 10px;
            padding: 10px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# Display chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

for message in st.session_state.chat_history:
    if message.startswith("You:"):
        st.markdown(f'<div class="user-message">{message[4:]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">{message[4:]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Display input field and send button
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Enter your message:", key="user_input_field", label_visibility="collapsed")
    submit_button = st.form_submit_button("Send", type="primary")

    if submit_button and user_input:
        st.session_state.chat_history = handle_query(user_input, st.session_state.chat_history)

st.markdown('</div>', unsafe_allow_html=True)
