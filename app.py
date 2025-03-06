from flask import Flask, render_template, request, send_file
import qrcode
import os

app = Flask(__name__)

# Folder to store QR codes
QR_FOLDER = "static/qr_codes"
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code_path = None
    if request.method == "POST":
        data = request.form["qr_text"]
        if data:
            qr_filename = os.path.join(QR_FOLDER, "generated_qr.png")
            generate_qr(data, qr_filename)
            qr_code_path = qr_filename  # Path to display QR code in HTML
    
    return render_template("index.html", qr_code=qr_code_path)

def generate_qr(data, file_path):
    """Generates a QR code and saves it as an image."""
    qr = qrcode.QRCode(
        version=2, error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10, border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(file_path)

@app.route("/download")
def download_qr():
    """Allows users to download the generated QR code."""
    return send_file("static/qr_codes/generated_qr.png", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
