from flask import Flask, render_template, request, redirect
import os
import pytesseract
import cv2
from pdf2image import convert_from_path
from textblob import TextBlob  # AI text analysis
from scraper import scrape_website
import logging
# Initialize Flask app
app = Flask(__name__, template_folder='templates')
# logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set path to Tesseract OCR executable (update for your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set path to Poppler bin (for PDF to image conversion)
POPPLER_PATH = r'D:\PyAutomateAI\poppler-24.08.0\Library\bin'  # Change as needed

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# AI text analysis function using TextBlob
def analyze_text(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity  # -1 (neg) to 1 (pos)

    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return "Negative"
    else:
        return "Neutral"

# Routes
@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Logging login attempts
        if username == 'juned' and password == 'junnu1729':
            logging.info(f"Login success - User: {username}")
            return redirect('/dashboard')
        else:
            logging.warning(f"Login failed - User: {username}")
            return "Invalid credentials!"
    
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    extracted_text = None
    ai_result = None

    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract text from PDF
        if file.filename.lower().endswith('.pdf'):
            pages = convert_from_path(file_path, 300, poppler_path=POPPLER_PATH)
            text_list = []
            for page in pages:
                text = pytesseract.image_to_string(page)
                text_list.append(text)
            extracted_text = "\n".join(text_list)
        else:
            # Extract text from image
            img = cv2.imread(file_path)
            if img is not None:
                extracted_text = pytesseract.image_to_string(img)
            else:
                extracted_text = "Unable to read the uploaded file."

        # Perform AI Text Classification
        if extracted_text:
            ai_result = analyze_text(extracted_text)

    return render_template('dashboard.html', result=extracted_text, ai=ai_result)


@app.route('/scrape')
def scrape():
    data = scrape_website()
    return render_template('scrape.html', data=data)
@app.route('/monitor')
def monitor():
    try:
        with open('monitor.log', 'r') as file:
            log_content = file.read()
    except FileNotFoundError:
        log_content = "No logs found."
    return render_template('monitor.html', logs=log_content)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
