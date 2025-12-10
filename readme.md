# Local Document Analyzer

## Overview

Local Document Analyzer is a Streamlit application leveraging OpenAI's Vision and parsing capabilities to process and analyze local document files such as invoices and receipts. The tool is designed to perform OCR (Optical Character Recognition) on PDFs or image files and extract structured data using OpenAI models.

## Features

- **File Uploads:** Upload images or PDFs.
- **PDF to Image Conversion:** Convert uploaded PDFs into images for processing.
- **OCR Extraction:** Extract text from images using OpenAI Vision API.
- **Invoice Parsing:** Parse structured data from extracted text.
- **Results Display:** Show structured results and summary analytics.
- **Download Data:** Download extracted data as CSV or Excel files.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Chandrakanth-Zen-Python/local_document_analyzer
   cd local-document-analyzer
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. **Install Dependencies**

   Make sure you have Python 3.x installed, then run:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Obtain an OpenAI API Key**

   - You will need an OpenAI API key to use the OCR and parsing services. Visit [OpenAI](https://openai.com/) to obtain the key.

2. **Run the Application**

   Start the Streamlit application using:

   ```bash
   streamlit run app.py
   ```

3. **Upload Files and Process**

   - Upload your PDF or image files in the Streamlit app.
   - Enter your OpenAI API key in the settings panel.
   - Click "Process Documents" to begin analyzing.

4. **View and Download Results**

   - View extracted data in the app.
   - Download the parsed results as CSV or Excel files.

## Dependencies

This project relies on the following main Python packages:

- **streamlit:** For building the interactive UI.
- **pandas:** Used for data manipulation and exporting results.
- **openai:** To interact with OpenAI's API for OCR and parsing.
- **pillow (PIL):** For image processing.
- **pdf2image:** To convert PDF files into images.
- **openpyxl:** For exporting results to Excel format.

## Contributing

Contributions to improve functionalities or fix issues are welcome. Feel free to submit a pull request or report any issues in the repository.

## License

This project is licensed under the MIT License.

## Acknowledgments

Special thanks to OpenAI for providing robust models that enable efficient OCR and text parsing capabilities.

---

Customize this `README.md` as needed to suit your specific project requirements and preferences.
