import pandas as pd
import random

# Define columns and properties
columns = ["Location Id", "Location Name", "isHavingVideoVisit", "Latitude", "Longitude", "Bid", 
           "YourFlatmatesLikes", "Address", "amenities", "Area", "AverageBidValue", "BuildingGenderType", 
           "City", "CustomerReviewCount", "DepositInMonth", "IsColivePropertyOfTheMonth", "Landmark", 
           "LocationDemand", "LocationHighlights", "Location Name", "LockinPeriod", "NoticePeriod", "NPS", 
           "OperationStartDate", "Pincode", "PricePerMonth", "PropertyHighlights", "PropertyModelType", 
           "PropertyRating", "PropertyReservationAmount", "PropertyStatus", "PropertyType", "PropertyVariant", 
           "RoomType", "Sharing", "SiteMapImagePath", "State", "SubLocation", "YouTubeURL", "Review Details", 
           "tileImageUrl"]

properties = ["Colive 016 MB Paradise", "Colive 018 The Address", "Colive 052 Franny", "Colive 056 Rio Grande", 
              "Colive 055 Jordan", "Colive 068 Hackensack", "Colive 301 Sanjana Emerald", "Colive 309 Primex Verterra", 
              "Colive 158 Winster", "Colive 160 Adelaide", "Colive 161 Brisbane", "Colive 162 Canberra", 
              "Colive 163 Darwin", "Colive 165 Willis Towers", "Colive 166 Grand Central", "Colive 167 Santa Clara", 
              "Colive 169 Alpha", "Colive 172 Orange", "Colive 173 Magnum", "Colive 174 Heritage", "Colive 175 Highland", 
              "Colive 178 Kingston", "Colive 186 Liberty", "Colive 187 Glory", "Colive 189 Primus", "Colive 190 Sunrise", 
              "Colive 194 Drava", "Colive 196 Campbell", "Colive 403 Riga", "Colive 181 Sunny Vale"]

# Define query templates
query_templates = [
    "What is the {detail} of {property_name}?",
    "Can you tell me the {detail} for {property_name}?",
    "Give me the {detail} of {property_name}.",
    "I need to know the {detail} for {property_name}.",
    "Provide the {detail} for {property_name}.",
    "What are the {detail} and {detail2} of {property_name}?",
    "Can you give me the {detail}, {detail2}, and {detail3} for {property_name}?",
    "Tell me about the {detail} and {detail2} for {property_name}.",
    "What can you tell me about the {detail} and {detail2} of {property_name}?"
]

# Mapping columns to user-friendly details
detail_mapping = {
    "Location Id": ["location ID", "ID"],
    "Location Name": ["location name", "Location Name", "name of the location"],
    "isHavingVideoVisit": ["video visit availability", "video tour option", "video"],
    "Latitude": ["latitude", "latitude coordinates"],
    "Longitude": ["longitude", "longitude coordinates"],
    "Bid": ["current bid", "bid amount","offer","proposal","price","amount","advance"],
    "YourFlatmatesLikes": ["flatmates' likes", "flatmates' preferences","flatmate","behavior","flatmate requirements"],
    "Address": ["address", "location address"],
    "amenities": ["amenities", "facilities","provision","resource","advantages","service"],
    "Area": ["area","location"],
    "AverageBidValue": ["average bid value", "mean bid value","average rent","average price","mean offering"],
    "BuildingGenderType": ["building gender type", "gender specification"],
    "City": ["city", "city location"],
    "CustomerReviewCount": ["number of reviews", "review count"],
    "DepositInMonth": ["deposit period", "deposit in months","deposit amount"],
    "IsColivePropertyOfTheMonth": ["property of the month status", "highlighted property status","speciality of property","colive property of the month"],
    "Landmark": ["nearest landmark", "landmark"],
    "LocationDemand": ["location demand", "demand of the location","fast filling status","filling status"],
    "LocationHighlights": ["location highlights", "highlights of the location"],
    "LockinPeriod": ["lock-in period", "lock-in duration","lockin time"],
    "NoticePeriod": ["notice period", "notice duration"],
    "NPS": ["NPS score", "Net Promoter Score"],
    "OperationStartDate": ["operation start date", "start date","builidng origin","building creation","founding day"],
    "Pincode": ["pincode", "postal code"],
    "PricePerMonth": ["monthly rent", "rent per month","rent","payment","amount"],
    "PropertyHighlights": ["property highlights", "highlights of the property","property speciality"],
    "PropertyModelType": ["property model type", "model type"],
    "PropertyRating": ["rating", "property rating","score"],
    "PropertyReservationAmount": ["reservation amount", "reservation fee"],
    "PropertyStatus": ["status", "availability status"],
    "PropertyType": ["property type", "type"],
    "PropertyVariant": ["property variants", "variants"],
    "RoomType": ["room types", "types of rooms","available rooms"],
    "Sharing": ["sharing options", "sharing availability","sharing"],
    "SiteMapImagePath": ["site map", "site map image path"],
    "State": ["state", "state location"],
    "SubLocation": ["sub-location", "sub-area"],
    "YouTubeURL": ["YouTube link", "YouTube video URL","video","link"],
    "Review Details": ["review details", "detailed reviews","reviews","feedback","resident response","comment","reaction","critique","criticism","opinion","observation"],
    "tileImageUrl": ["image URL", "image link","image","photo","official photo"]
}

# Generate the dataset
data = []
total_rows = 6000  # Target number of rows
count = 0

while count < total_rows:
    property_name = random.choice(properties)
    detail_column = random.choice(columns)
    detail = random.choice(detail_mapping[detail_column])
    
    detail2_column = random.choice([col for col in columns if col != detail_column])
    detail2 = random.choice(detail_mapping[detail2_column])

    detail3_column = random.choice([col for col in columns if col != detail_column and col != detail2_column])
    detail3 = random.choice(detail_mapping[detail3_column])

    query_template = random.choice(query_templates)
    if "{detail2}" in query_template and "{detail3}" in query_template:
        query = query_template.format(detail=detail, detail2=detail2, detail3=detail3, property_name=property_name)
        relevant_columns = [detail_column, detail2_column, detail3_column]
    elif "{detail2}" in query_template:
        query = query_template.format(detail=detail, detail2=detail2, property_name=property_name)
        relevant_columns = [detail_column, detail2_column]
    else:
        query = query_template.format(detail=detail, property_name=property_name)
        relevant_columns = [detail_column]
    
    data.append({"User Query": query, "Relevant Columns": relevant_columns})
    count += 1

# Convert to DataFrame
df = pd.DataFrame(data)
df.to_csv('synthetic_subset_dataset.csv', index=False)
