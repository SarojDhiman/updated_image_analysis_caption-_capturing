import pytesseract
from PIL import Image
import cv2

# Mapping of language codes to full names
LANGUAGE_NAMES = {
    'hin': 'Hindi',
    'eng': 'English',
    'asm': 'Assamese',
    'tel': 'Telugu',
    'tam': 'Tamil',
    'ben': 'Bengali',
    'guj': 'Gujarati',
    'kan': 'Kannada',
    'mal': 'Malayalam',
    'mar': 'Marathi',
    'pan': 'Punjabi',
    'urd': 'Urdu',
    'san': 'Sanskrit',
    'rom': 'Romanized Hindi'
}

def get_confidence(image, lang):
    try:
        data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['conf'] if conf != '-1']
        if confidences:
            return sum(confidences) / len(confidences)
        else:
            return 0
    except pytesseract.TesseractError as e:
        print(f"Error processing image for language '{lang}': {e}")
        return 0
    except Exception as e:
        print(f"Unexpected error processing image for language '{lang}': {e}")
        return 0

def determine_language(image):
    languages = ['hin', 'eng', 'asm', 'tel', 'tam', 'ben', 'guj', 'kan', 'mal', 'mar', 'pan', 'urd', 'san', 'rom']
    confidences = {lang: get_confidence(image, lang) for lang in languages}

    # Determine the language with the highest confidence
    detected_lang_code = max(confidences, key=confidences.get)
    detected_lang_name = LANGUAGE_NAMES.get(detected_lang_code, 'Unknown')
    return detected_lang_code, detected_lang_name, confidences[detected_lang_code]

# Path to your test image
# image_path = r"C:\Users\Saroj Dhiman\Downloads\kan1.jpeg"
# image_path = r"C:\Users\Saroj Dhiman\Downloads\Figure_1.png"
# image_path = r"C:\Users\Saroj Dhiman\Downloads\urdu2.jpg"
# image_path = r"C:\Users\Saroj Dhiman\Downloads\dd.jpg"
# image_path = r"C:\Users\Saroj Dhiman\Downloads\bengali3.jpg"
# image_path = r"C:\Users\Saroj Dhiman\Downloads\malyyyy.jpg"
image_path = r"C:\Users\Saroj Dhiman\Downloads\imagess.jpeg"

# Load the image
image = Image.open(image_path)

# Determine the language of the image
detected_lang_code, detected_language, confidence = determine_language(image)

print(f"Detected Language: {detected_language}")
print(f"Confidence: {confidence}")

# Preprocess the image using OpenCV
image_cv = cv2.imread(image_path)
gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

# Preprocessing
blur = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Remove noise using morphological operations
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Invert the image to match the text color
invert = 255 - opening

# Perform text extraction with the detected language
custom_config = '--psm 6'  # Page segmentation mode, adjust as needed
extracted_text = pytesseract.image_to_string(invert, lang=detected_lang_code, config=custom_config)

print(f"Extracted Text: {extracted_text}")
