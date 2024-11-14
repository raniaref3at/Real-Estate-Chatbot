import re

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
