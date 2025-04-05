import google.generativeai as gen

gen.configure(api_key="AIzaSyDeZyH_yeLW8iDVHYVUHUkO2uvp4qWjeRA")
model = gen.GenerativeModel('gemini-1.5-flash')