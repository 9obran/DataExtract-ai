import streamlit as st
from google import genai
import fitz  # PyMuPDF
import json
import pandas as pd
from io import BytesIO

# 1. Initialize the Client with API key
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

def extract_text_from_pdf(uploaded_file) -> str: # returns a string
    # Open document from the uploaded Streamlit file buffer
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf") # open the file
    return "\n".join(page.get_text() for page in doc) # return the text

def extract_fields_with_llm(text: str) -> dict: # returns a dict
    # 2. Define the prompt
    prompt = f"""
    Extract all key business fields from this document.
    Return ONLY a flat, valid JSON object. No explanation.
    Fields to extract (if present): vendor name, invoice number, 
    date, due date, total amount, line items, customer name, address.
    
    Document:
    {text[:3000]} 
    """ # Limit to first 3000 characters

    # 3. Call the API using the correct new syntax!
    # Notice it is client.models.generate_content
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    # 4. Parse the guaranteed JSON response
    return json.loads(response.text)

def dict_to_excel(data: dict) -> BytesIO:
    rows = [(k, v) for k, v in data.items()]
    df = pd.DataFrame(rows, columns=["Field", "Value"])
    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer

# --- UI ---
st.title("DataExtract AI")
st.caption("Upload any business document → get structured Excel output instantly.")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded:
    with st.spinner("Extracting..."):
        text = extract_text_from_pdf(uploaded)
        data = extract_fields_with_llm(text)
    
    st.success("Extraction complete")
    st.json(data)
    
    excel = dict_to_excel(data)
    st.download_button(
        label="Download Excel",
        data=excel,
        file_name="extracted_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )