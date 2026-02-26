
from flask import Flask, render_template, request, send_file, redirect
import qrcode
import os
import uuid

app = Flask(__name__)
QR_FOLDER = "static/qr"
os.makedirs(QR_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    qr_path = None
    qr_type = None

    if request.method == "POST":
        qr_type = request.form.get("qr_type", "wifi")
        
        if qr_type == "wifi":
            ssid = request.form["ssid"]
            password = request.form.get("password", "")
            security = request.form["security"]
            hidden = request.form.get("hidden", "false")

            if security == "nopass":
                qr_string = f"WIFI:T:nopass;S:{ssid};;"
            else:
                qr_string = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden};;"
        
        elif qr_type == "url":
            url = request.form["url"]
            # Tambahkan https:// jika belum ada
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            qr_string = url

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR Code
        filename = f"{uuid.uuid4().hex}.png"
        qr_path = os.path.join(QR_FOLDER, filename)
        img.save(qr_path)

    return render_template("index.html", qr_path=qr_path, qr_type=qr_type)

@app.route("/download/<path:filename>")
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)