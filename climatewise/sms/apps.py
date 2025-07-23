from django.apps import AppConfig
'''
from flask import Flask, request
import spacy
import dateparser
import sqlite3

app = Flask(__name__)
nlp = spacy.load('en_core_web_sm')

INCIDENT_KEYWORDS = ['flood','storm','drought','earthquake','fog','tornado','heatwave','erosion']
def extract_info(sms_text):
    doc = nlp(sms_text)
    locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    time_phrases = [ent.text for ent in doc.ents if ent.label_ in ['DATE', 'TIME']]
    parsed_times = [dateparser.parse(tp) for tp in time_phrases if dateparser(tp)]
    incident = next((kw for kw in INCIDENT_KEYWORDS if kw in sms_text.lower()), None)

    return {
        'locations': locations[0] if locations else None,
        'incident_type': incident,
        'time': parsed_times[0] if parsed_times else None,
    }
def store_to_db(data):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute(''/'
    CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT,
                    incident_type TEXT,
                    time TIMESTAMP,
)''/'
    c.execute('INSERT INTO reports (location, incident_type, time) VALUES (?, ?, ?)',
                (data['location'], data['incident_type'], data['time']))
@app.route('/incoming_sms',methods=['POST'])
def incoming_sms():
    sms_text = request.form.get('text')
    print(f'Received SMS:{sms_text}')
    parsed_data = extract_info(sms_text)
    store_to_db(parsed_data)
    return 'OK',200
if __name__ == '__main__':
    app.run(debug=True,port=5000)
'''

class SmsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sms'