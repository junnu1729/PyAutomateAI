from flask import Flask, render_template, request, redirect
import os
import pytesseract
import cv2
from pdf2image import convert_from_path

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Configuration
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set path to Tesseract OCR executable (change this for production)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Set path to Poppler bin (for PDF to image conversion)
POPPLER_PATH = r'C:\Users\USER\Downloads\poppler-windows-24.08.0-0'  # Change for production

# Create uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Set up routes
@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'juned' and request.form['password'] == 'junnu1729':
            return redirect('/dashboard')
        return "Invalid credentials!"
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    extracted_text = None
    if request.method == 'POST':
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        if file.filename.lower().endswith('.pdf'):
            # Convert PDF pages to images
            pages = convert_from_path(file_path, 300, poppler_path=POPPLER_PATH)
            text_list = []
            for page in pages:
                text = pytesseract.image_to_string(page)
                text_list.append(text)
            extracted_text = "\n".join(text_list)
        else:
            # Assume it's an image
            img = cv2.imread(file_path)
            if img is not None:
                extracted_text = pytesseract.image_to_string(img)
            else:
                extracted_text = "Unable to read the uploaded file."

    return render_template('dashboard.html', result=extracted_text)

# Run the app only when executed directly
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Set the port for deployment
    app.run(host='0.0.0.0', port=port, debug=True)
