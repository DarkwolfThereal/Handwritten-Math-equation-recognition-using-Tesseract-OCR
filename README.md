# Handwritten Math Equation Recognition using Tesseract OCR

## Overview
This project is a Flask-based web application that recognizes handwritten mathematical equations from images using **Tesseract OCR**. Users can upload images containing math expressions, and the application extracts and processes the equations for further evaluation.

## Features
- 📷 **Image Upload:** Users can upload images of handwritten mathematical equations.
- 🧠 **OCR Processing:** Uses **Tesseract OCR** to extract text from images.
- 🛠️ **Preprocessing Pipeline:** Includes denoising, adaptive thresholding, and contrast enhancement for better recognition.
- 🔄 **Multiple Iterations for Accuracy:** Runs multiple iterations with different preprocessing settings to improve OCR accuracy.
- 📈 **Expression Cleaning:** Corrects common OCR misinterpretations like 'x' misread as '*' and removes unnecessary spaces.
- 🌐 **Web-Based Interface:** Simple UI to upload images and display extracted equations.

## Technologies Used
- **Python** (Backend logic)
- **Flask** (Web framework)
- **OpenCV** (Image preprocessing)
- **Tesseract OCR** (Text recognition)
- **HTML, CSS, JavaScript** (Frontend UI)

## Installation & Setup
### Prerequisites
Ensure you have the following installed:
- **Python 3.x**
- **Tesseract OCR** (Download from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract))
- **pip** (Python package manager)

### Steps to Run Locally
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/DarkwolfThereal/Handwritten-Math-equation-recognition-using-Tesseract-OCR.git
   cd Handwritten-Math-equation-recognition-using-Tesseract-OCR
   ```
2. **Set Up Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set the Path for Tesseract OCR in `app.py` (If Needed):**
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```
5. **Run the Flask Application:**
   ```bash
   python app.py
   ```
6. **Open the App in Your Browser:**
   - Go to `http://127.0.0.1:5000/`
   - Upload an image and view the extracted math expression.

## Accuracy Warning ⚠️
This project relies on **Tesseract OCR**, which is not optimized for recognizing handwritten mathematical expressions. As a result, the accuracy of extracted equations may be low, especially for complex symbols and notations. Consider using deep learning-based OCR models for improved performance.

## Usage
- Upload an image containing a handwritten mathematical expression.
- The system processes the image and extracts the equation.
- The extracted equation is displayed on the webpage.

## Future Improvements
- 🖊️ **Handwriting Recognition Model:** Improve accuracy with a custom-trained deep learning model.
- ✏️ **Equation Solver:** Add LaTeX rendering and equation solving functionality.
- 📡 **API Support:** Expose an API for integration with other applications.

## Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the **MIT License**.

## Author
Developed by [DarkwolfThereal](https://github.com/DarkwolfThereal).


