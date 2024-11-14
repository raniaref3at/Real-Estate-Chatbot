def format_properties(properties, max_results=5):
    if properties.empty:
        return "Sorry, no properties match your criteria."
    
    response = "Based on your criteria, these are the properties that best match you: \n"
    properties = properties.head(max_results)

    for index, (_, row) in enumerate(properties.iterrows(), start=1):
        response += f"\n{index}_Location: {row['displayAddress']} "
        response += f"Price: {row['price']} AED "
        response += f"\nSize: {row['sizeMin']} sq ft\n"
        response += f"Bedrooms: {row['bedrooms']}\n"
        response += f"Bathrooms: {row['bathrooms']}\n"
        response += f"Furnishing: {row['furnishing']}\n\n"
    
    return response
