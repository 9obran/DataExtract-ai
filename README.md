# DataExtract AI

**Live Demo:** [dataextract-ai.streamlit.app](https://dataextract-ai.streamlit.app/)

A production-ready Streamlit application that uses Google's Gemini 2.5 Flash to extract structured business data from PDF documents and export it directly to Excel. Built to eliminate manual data entry from invoices, receipts, purchase orders, and other standard business paperwork.

---

## Overview

Upload any business PDF and the app automatically identifies and extracts key fields — vendor name, invoice number, dates, line items, totals, customer details, and addresses. The extracted data is displayed as structured JSON and can be downloaded instantly as a formatted Excel file.

This project demonstrates practical integration of LLMs into document processing pipelines, with careful attention to API reliability, structured output handling, and clean data transformation.

## Features

- **Drag-and-drop PDF upload** with immediate processing feedback
- **AI-powered field extraction** using Gemini 2.5 Flash with enforced JSON output via `response_mime_type`
- **Structured data preview** in the browser before download
- **One-click Excel export** using Pandas and openpyxl
- **Secure API key management** through Streamlit secrets

## Tech Stack

- **Frontend:** Streamlit
- **LLM:** Google Gemini 2.5 Flash via the `google-genai` SDK
- **PDF Parsing:** PyMuPDF (fitz)
- **Data Processing:** Pandas
- **Excel Generation:** openpyxl

## Architecture & Key Decisions

**Text truncation to 3,000 characters:** The app sends only the first 3,000 characters of the PDF to the LLM. This keeps API calls fast and cost-efficient while capturing the header and summary sections where the most critical business fields typically appear.

**Enforced JSON output:** The API call uses `config={"response_mime_type": "application/json"}` to guarantee valid JSON from Gemini, eliminating fragile regex parsing or output cleaning.

**In-memory processing:** PDFs are read directly from the Streamlit file buffer without writing to disk, keeping the deployment stateless and suitable for containerized environments.

## Local Setup

**Prerequisites:** Python 3.9+ and a [Google AI Studio API key](https://aistudio.google.com/app/apikey)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/dataextract-ai.git
cd dataextract-ai

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
mkdir -p .streamlit
echo 'GEMINI_API_KEY = "your-api-key-here"' > .streamlit/secrets.toml

# 5. Run the app
streamlit run app.py
```

The app will be available at `http://localhost:8501`.

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── .streamlit/
    └── secrets.toml    # API configuration (gitignored)
```

## Deployment

The live instance runs on **Streamlit Community Cloud**. To deploy your own:

1. Push the repository to GitHub
2. Connect the repo at [share.streamlit.io](https://share.streamlit.io)
3. Add `GEMINI_API_KEY` under **App Settings → Secrets**
4. Deploy

## Requirements

```
streamlit>=1.30.0
google-genai>=1.0.0
PyMuPDF>=1.23.0
pandas>=2.0.0
openpyxl>=3.1.0
```

## Limitations & Considerations

- **Character limit:** Only the first 3,000 characters of each PDF are processed. Multi-page documents with critical data spread throughout may require pre-processing or pagination logic.
- **Document types:** Optimized for standard business documents. Highly complex tables, scanned images without OCR text layers, or unconventional layouts may reduce extraction accuracy.
- **API dependency:** Requires an active internet connection and valid Gemini API key.

## License

MIT
