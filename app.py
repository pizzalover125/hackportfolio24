import os
from flask import Flask, render_template, request
import PyPDF2
import google.generativeai as genai

app = Flask(__name__)

# Configure generative AI and create the model instance
genai.configure(api_key="AIzaSyCpFAJhHWgOlx5zsbb_5B7KHMFAzNyxp-w")
model = genai.GenerativeModel('gemini-1.0-pro-latest')

# Function to interact with generative AI model
def askGemini(text):
    response = model.generate_content(text)
    return response.text

# Function to extract text content from PDF
def pdf_content(filepath):
    try:
        with open(filepath, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()

            return text
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        file.save(file.filename)
        pdfCont = pdf_content(file.filename)
        response = askGemini(f"You are a resume coach. You want to be very strict and subjective. Give the person a score from 1 to 100. Tell them what to improve. Be concise. Don't use any markdown. Don't comment on anything related to formatting. Resume: {pdfCont}")


        return render_template("index.html", response=response)
    else:
        # Clean up previously uploaded PDFs
        for filename in os.listdir('.'):
            if filename.lower().endswith(".pdf"):
                file_path = os.path.join('.', filename)
                os.remove(file_path)
                print(f"Deleted PDF: {filename}")

        return render_template("index.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
