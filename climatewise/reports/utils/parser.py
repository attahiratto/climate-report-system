import spacy
import dateparser
from pymongo import MongoClient
from geopy.geocoders import Nominatim, GoogleV3
import google.generativeai as genai
model = genai.GenerativeModel("gemini-2.5-flash")
genai.configure(api_key="AIzaSyAsR2JOO3qPTFHVpKUxY-aPWDF2rJ92z-s")


def run_parser():
    nlp = spacy.load('en_core_web_sm')
    geolocator = Nominatim(user_agent="climate_reporter")
    
    def extract_info(location):
        doc = nlp(location)
        locations = [ent.text for ent in doc.ents if ent.label_ in ['FAC','GPE']] #Geopolitical Entity
        #times = [dateparser.parse(ent.text) for ent in doc.ents if ent.label_ in ['DATE', 'TIME']]
        #incident = next((kw for kw in INCIDENT_KEYWORDS if kw in text.lower()), None)
        if locations:
            location = ",".join(locations)
        else:
            pass
        lat,lon = None,None
        try:
            loc = geolocator.geocode(f"{location},Nigeria")
            if loc:
                lat,lon = loc.latitude , loc.longitude
        except:
            pass
        return lat,lon,location
    client = MongoClient("mongodb+srv://abdoulbin38:w0bsa0IXB7mk2xcH@cluster0.5n02s7c.mongodb.net/climateReportSystemdb?retryWrites=true&w=majority&authSource=admin")
    db = client["climateReportSystem"]
    collection = db["Incoming Messages"]
    #collection_2 = db["Processed Messages"]
    #Process and Update DB
    for doc in collection.find({"latitude": {"$exists": False}}):
        doc_location = doc["location"]
        #text = doc.get("text")
        #prompt = f"Convert this location:'{doc_location}' in Nigeria, into a format that is usable by Nomatim's geocoder, and return the answer in python string format "  #f"Translate the following text:'{text}' to english and return only the translated text in a python string format, exactly like this:'translated text' "
        #response = model.generate_content(prompt)
        #doc_location = response.text
        lat,lon,location = extract_info(doc_location)
        
        collection.update_one(
            {"_id":doc["_id"]},
            {"$set":
            {"location": location,
            "latitude":lat,
            "longitude":lon}
            }
        )
       