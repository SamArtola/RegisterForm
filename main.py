import base64
import streamlit as st
import requests
import os

st.title("WiTCON 2024 Registration")
st.image("media/WiTCONLogo.png")
st.header("Registration Form")

AIRTABLE_PERSONAL_TOKEN = st.secrets["AIRTABLE_PERSONAL_TOKEN"]
AIRTABLE_BASE_ID = st.secrets["AIRTABLE_PERSONAL_TOKEN"]
AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_PERSONAL_TOKEN"]
AIRTABLE_API_URL = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'

headers = {
    'Authorization': f'Bearer {AIRTABLE_PERSONAL_TOKEN}',
    'Content-Type': 'application/json',
}

firstName = st.text_input("Enter your first name:")
lastName = st.text_input("Enter your last name:")
email = st.text_input("Enter your university email:")
phone = st.text_input("Enter your phone number:")
resume = st.file_uploader("Upload your Resume here (PDF only!)", type="pdf")
pantherID = st.text_input("Enter Panther ID If Applicable:")
github = st.text_input("Please provide a link to your Github:")
linkedIn = st.text_input("Please provide the link to your LinkedIn:")

academicStanding = st.selectbox("What is your academic standing?",
                                    index=None,
                                    options=["Freshman", "Sophomore", "Junior", "Senior", "Graduate"])

majorOptions = ["Computer Science BA", "Computer Science BS", "Computer Science MS", "Computer Science PhD",
                    "Cybersecurity BA", "Cybersecurity BS", "IoT", "Computer Engineering", "Electrical Engineering",
                    "Management Information Systems", "Information Technology BA", "Information Technology BS",
                    "Information Technology MS", "Information Technology PhD", "Data Science",
                    "Interdisciplinary Engineering", "Mechanical Engineering", "Biomedical Engineering",
                    "Civil Engineering", "Other"]
major = st.selectbox("What is your Major?",
                         options=majorOptions,
                         placeholder="Select Major",
                         index=None)
if major == "Other":
    major = st.text_input("Please enter your major:")

hispanic = st.checkbox("Do you identify as latino/latina/latinx?")

ethnicities = ["African American/Black",
                   "Caucasian/White",
                   "Hispanic/Latino",
                   "Asian",
                   "Native American/Alaska Native",
                   "Pacific Islander",
                   "Middle Eastern/North African",
                   "Biracial/Multiracial",
                   "Other (please specify)",
                   "Prefer not to say"]

ethnicity = st.selectbox("What is your ethnicity?",
                             options=ethnicities,
                             placeholder="Select Ethnicity",
                             index=None)

shirt = st.selectbox("What is your shirt size?",
                         options=["S", "M", "L", "XL", "XXL"], index=None)

diet = st.multiselect("Any dietary restrictions?",
                          options=["No", "Vegan", "Vegetarian", "Gluten Allergy", "Lactose Intolerance"])
st.text(diet)
consent = st.checkbox("I consent to the use of my likeness in media publications, for WiTCON and third parties, "
                          "on print and social media for the purpose of promotion and awareness."
                          )

pasta = st.text_input("What's your favorite pasta shape?")
st.image("https://sancarlo.co.uk/app/uploads/2019/12/pasta.jpg")
submitted = st.button("Submit")

if submitted:
        st.write("Thank you for registering for WiTCON")
        form_entry = {
            'fields': {
                'Name': firstName + " " + lastName,
                'Email': email,
                'LinkedIn': linkedIn,
                'Major': major,
                'Phone': phone,
                'PantherID': pantherID,
                'Github': github,
                'Academic Standing': academicStanding,
                'Shirt': shirt,
                'pasta': pasta,
                'consent': consent
            }
        }

        temp = ""
        for i in diet:
            temp += i
        form_entry['fields']['Diet'] = diet
        if resume is not None:
            file_content = resume.read()
            file_content_base64 = base64.b64encode(file_content).decode('utf-8')

            attachment = {
                'filename': resume.name,
                'url': f'data:application/pdf;base64,{file_content_base64}'
            }

            form_entry['fields']['Resume'] = [attachment]

        response = requests.post(AIRTABLE_API_URL, json=form_entry, headers=headers)

        if response.status_code == 200:
            st.success("Form submitted successfully!")
        else:
            st.error(f"Error submitting form: {response.text}")

response = requests.get(AIRTABLE_API_URL, headers=headers)
data = response.json()
