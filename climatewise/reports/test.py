import google.generativeai as genai

genai.configure(api_key="AIzaSyAsR2JOO3qPTFHVpKUxY-aPWDF2rJ92z-s")
model = genai.GenerativeModel("gemini-2.5-flash")
prompt =  f"Given the text: 'ana ruwa sosai a nan yakawada', translate in it to english and return it as a python string"
response = model.generate_content(prompt)
getback = response.text
print(getback)

