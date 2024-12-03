import qrcode
import os

def generate_qr_code(url):
    print(f"Generating QR code for URL: {url}")  # Debugging log
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_path = 'static/images/qrcode.png'
    
    try:
        img.save(qr_code_path)
        print(f"QR code saved at: {qr_code_path}")  # Debugging log
    except Exception as e:
        print(f"Error saving QR code: {e}")  # Error logging
    
    return qr_code_path
