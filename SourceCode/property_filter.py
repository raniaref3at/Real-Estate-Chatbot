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
