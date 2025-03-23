import os
import cv2
import pytesseract
import numpy as np
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import re

# Explicitly set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(img, (5, 5), 0)

    # Adaptive Thresholding for better binarization
    binary = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )

    # Morphological opening (removes small noise)
    kernel = np.ones((3, 3), np.uint8)  # Slightly larger kernel
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    # Sharpening filter to enhance text clarity
    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])  # Laplacian kernel
    sharpened = cv2.filter2D(cleaned, -1, sharpen_kernel)

    # Apply CLAHE (Histogram Equalization) for contrast improvement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(sharpened)

    return enhanced


def preprocess_with_error_margin(image_path, iteration):
    """This function applies a different preprocessing frame of error for each iteration."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Introduce variations in thresholding and denoising for each iteration
    if iteration == 0:
        _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    elif iteration == 1:
        _, binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
    elif iteration == 2:
        _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    else:
        # More aggressive thresholding or different methods
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Apply different denoising levels based on iteration
    denoised = cv2.fastNlMeansDenoising(binary, None, h=5 + iteration, templateWindowSize=7)
    
    # Enhanced contrast adjustments based on iteration
    enhanced_contrast = cv2.convertScaleAbs(denoised, alpha=1.5 + (iteration * 0.2), beta=50)

    return enhanced_contrast

def extract_expression(image_path, iterations=4):
    """Extract mathematical expression with iterations to adjust the frame of error."""
    # Preprocess the image before passing to Tesseract
    processed_img = preprocess_image(image_path)

    # Configure Tesseract for math symbols and numbers
    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=+-/=()0123456789abcdefghijklmnopqrstuvwxyz'
    
    previous_result = ""
    final_result = ""
    
    for i in range(iterations):
        # Modify processing parameters dynamically for each iteration
        processed_img = preprocess_with_error_margin(image_path, iteration=i)

        # Run Tesseract on the processed image
        text = pytesseract.image_to_string(processed_img, config=custom_config)
        
        # Clean the result (strip unwanted characters, remove newlines, etc.)
        text = text.strip().replace('\n', '')

        print(f"Iteration {i + 1}: {text}")

        # Check if the result stabilizes
        if text == previous_result:
            print("Result stable, stopping iterations.")
            break

        # Update the result for comparison in the next iteration
        previous_result = text

    final_result = text
    return final_result

def process_math_image(image_path):
    """Process image and return the extracted expression or error."""
    try:
        # Run the OCR with multiple iterations to refine the result
        expression = extract_expression(image_path)

        # Return the final result
        return {
            'expression': expression,
            'image_path': image_path.replace('static/', '')
        }
    except Exception as e:
        return {'error': str(e), 'image_path': image_path.replace('static/', '')}
    

def clean_expression(text):
    # Replace common OCR misinterpretations
    text = text.replace('x', '*')  # Convert misinterpreted 'x' to '*'
    text = re.sub(r'(?<!\d)\.(?!\d)', '', text)  # Remove isolated dots
    text = re.sub(r'\s+', '', text)  # Remove unnecessary spaces

    return text

@app.route('/', methods=['GET', 'POST'])
def index():
    """Handle the file upload and process math expressions."""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = process_math_image(filepath)
            return render_template('index.html', result=result)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)