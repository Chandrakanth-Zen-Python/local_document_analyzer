# app.py
"""
Local Document Analyzer (OpenAI Vision OCR + OpenAI Invoice Parsing)
"""

import streamlit as st
import io
import re
import os
import json
import base64
import tempfile
import pandas as pd
from datetime import datetime
from PIL import Image
from openai import OpenAI
import fitz  # NEW: PyMuPDF replaces pdf2image

st.set_page_config(page_title="Document Analyzer (OpenAI OCR)", layout="wide")

# ----------------- UTILITIES -----------------

def pdf_to_images(pdf_bytes):
    """Convert PDF to list of PIL images using PyMuPDF (no poppler needed)."""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    images = []

    for page in doc:
        pix = page.get_pixmap(dpi=200)
        img_bytes = pix.tobytes("png")
        images.append(Image.open(io.BytesIO(img_bytes)))

    return images

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode()

def openai_ocr(image_bytes, api_key, model="gpt-4o-mini"):
    client = OpenAI(api_key=api_key)
    img_b64 = base64.b64encode(image_bytes).decode()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Extract ONLY raw text from this image. No commentary."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all text from the document."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                    }
                ]
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


def openai_parse_invoice(ocr_text, api_key, model="gpt-4o-mini"):
    client = OpenAI(api_key=api_key)

    system_prompt = """
    You are an invoice parser. Return ONLY valid JSON:

    {
      "vendor": string | null,
      "invoice_number": string | null,
      "date": string | null,
      "currency": string | null,
      "subtotal": number | null,
      "tax": number | null,
      "total": number | null,
      "line_items": [
        {
          "description": string | null,
          "qty": number | null,
          "unit_price": number | null,
          "amount": number | null
        }
      ]
    }
    """

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": ocr_text}
        ],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "")
    return json.loads(raw)

def safe_float(x):
    try:
        if x is None: return None
        return float(str(x).replace(",", "").replace("₹","").replace("$",""))
    except:
        return None


# ----------------- STREAMLIT UI -----------------

st.title("📄 Local Document Analyzer — OpenAI OCR + OpenAI Parsing")
st.write("Upload invoices/receipts and extract structured data locally.")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("OpenAI API Key", type="password")
    ocr_model = st.text_input("OCR Model", value="gpt-4o-mini")
    parse_model = st.text_input("Parser Model", value="gpt-4o-mini")

files = st.file_uploader("Upload images or PDFs", accept_multiple_files=True,
                         type=["jpg","jpeg","png","pdf"])

if st.button("Process Documents"):

    if not api_key:
        st.error("Enter OpenAI API key.")
        st.stop()

    if not files:
        st.error("Upload at least one file.")
        st.stop()

    parsed_records = []

    for file in files:
        st.subheader(f"📄 Processing {file.name}")

        # ===== PDF OR IMAGE =====
        if file.name.lower().endswith(".pdf"):
            pdf_bytes = file.read()
            images = pdf_to_images(pdf_bytes)   # NEW: use PyMuPDF
            st.info(f"PDF contains {len(images)} page(s).")
        else:
            images = [Image.open(file)]

        full_ocr_text = ""

        # ===== OCR each page =====
        for idx, img in enumerate(images):
            st.write(f"OCR Page {idx+1} ...")
            buf = io.BytesIO()
            img.save(buf, format="PNG")

            ocr_text = openai_ocr(buf.getvalue(), api_key, model=ocr_model)
            st.text_area(f"OCR Output Page {idx+1}", ocr_text, height=200)

            full_ocr_text += "\n" + ocr_text

        # ===== Parse invoice =====
        st.write("🔍 Parsing invoice data...")
        parsed = openai_parse_invoice(full_ocr_text, api_key, model=parse_model)

        parsed["subtotal"] = safe_float(parsed.get("subtotal"))
        parsed["tax"] = safe_float(parsed.get("tax"))
        parsed["total"] = safe_float(parsed.get("total"))

        parsed_records.append(parsed)

        st.success("Parsed successfully!")
        st.json(parsed)

    # ===== DataFrame =====
    df = pd.DataFrame(parsed_records)

    st.header("📊 Extracted Data")
    st.dataframe(df)

    # ===== Download CSV =====
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "invoices.csv", "text/csv")

    # ===== Download Excel =====
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        df.to_excel(tmp.name, index=False)
        excel_bytes = open(tmp.name, "rb").read()
        st.download_button(
            "Download Excel", 
            excel_bytes, 
            "invoices.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
