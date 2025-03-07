import os
import numpy as np
from flask import Flask, request, render_template
from PIL import Image, ImageEnhance

app = Flask(__name__)

UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ASCII_CHARS = "@#$%?*+;:,.!"

def image_to_ascii(image_path, width=100, contrast_factor=1.5):
    img = Image.open(image_path)
    aspect_ratio = img.height / img.width
    # Multiplying by 0.55 to correct distortion
    new_height = int(width * aspect_ratio * 0.55)
    
    # Resize image while keeping aspect ratio
    img = img.resize((width, new_height))
    img = img.convert("L")  # "L" mode converts the image to grayscale
    
    # Fix: Corrected "enchance" to "enhance"
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_factor)

    pixels = np.array(img)
    normalized_pixels = (pixels / 255) * (len(ASCII_CHARS) - 1)

    ascii_str = "\n".join(
        "".join(ASCII_CHARS[int(pixel)] for pixel in row) 
        for row in normalized_pixels
    )

    return ascii_str

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "image" not in request.files:
            return "no file part", 400
        file = request.files["image"]
        
        if file.filename == "":
            return "no selected file", 400
        
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, "uploaded_image.png")
            file.save(file_path)
            print(f"File saved: {file_path}")

            ascii_str = image_to_ascii(file_path)
            print(f"Generated ASCII Preview:\n{ascii_str[:300]}")

            # Fix: Changed "ascii_art" to "ascii_str"
            return render_template("index.html", ascii_str=ascii_str)
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
