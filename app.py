from flask import Flask, render_template, request, jsonify
from googletrans import Translator
import pytesseract
from PIL import Image
import whisper
import os

app = Flask(__name__)

# Supported languages and their codes
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Odia": "or",
    "Urdu": "ur",
}

# Function to validate target language
def validate_language(language):
    if language in SUPPORTED_LANGUAGES:
        return SUPPORTED_LANGUAGES[language]
    else:
        raise ValueError(f"Unsupported language: {language}")

# Function to translate text
def translate_text(text, target_language):
    try:
        target_code = validate_language(target_language)
        translator = Translator()
        translated = translator.translate(text, dest=target_code)
        return translated.text
    except Exception as e:
        return f"Translation error: {str(e)}"

# Function to convert audio to text
def audio_to_text(audio_file):
    try:
        model = whisper.load_model("base")  # Load Whisper model
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        return f"Audio-to-text error: {str(e)}"

# Function to extract text from an image
def image_to_text(image_path):
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        return f"Image-to-text error: {str(e)}"

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/translate", methods=["POST"])
def translate():
    try:
        input_type = request.form.get("input_type")
        target_language = request.form.get("target_language")

        if input_type == "text":
            text = request.form.get("text")
            translated_text = translate_text(text, target_language)
            return jsonify({"original_text": text, "translated_text": translated_text})

        elif input_type == "audio":
            audio_file = request.files.get("audio_file")
            if audio_file:
                audio_path = "temp_audio.wav"
                audio_file.save(audio_path)
                text = audio_to_text(audio_path)
                translated_text = translate_text(text, target_language)
                return jsonify({"original_text": text, "translated_text": translated_text})
            else:
                return jsonify({"error": "No audio file uploaded"})

        elif input_type == "image":
            image_file = request.files.get("image_file")
            if image_file:
                image_path = "temp_image.png"
                image_file.save(image_path)
                text = image_to_text(image_path)
                translated_text = translate_text(text, target_language)
                return jsonify({"original_text": text, "translated_text": translated_text})
            else:
                return jsonify({"error": "No image file uploaded"})

        return jsonify({"error": "Invalid input type"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)