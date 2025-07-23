import spacy
import os
from climatewise.climatewise.settings import GOOGLE_AI_API,MONGO_CLIENT
from pymongo import MongoClient
from geopy.geocoders import Nominatim, GoogleV3
import google.generativeai as genai
model = genai.GenerativeModel("gemini-2.5-flash")
genai.configure(os.getenv(GOOGLE_AI_API))


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
    client = MongoClient(os.getenv(MONGO_CLIENT))
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
       