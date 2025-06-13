# LSB-based-Image-Steganography-Tool
🛡️ Advanced Image Encryption and Decryption using LSB Technique
📌 Project Overview
This project is a secure steganography tool that hides secret messages inside images using Least Significant Bit (LSB) technique. It combines AES encryption for confidentiality and HMAC authentication for integrity, ensuring robust protection of hidden data. A simple Graphical User Interface (GUI) is also developed for ease of use.

🎯 Objectives
✅ Hide confidential messages inside images using LSB technique.
🔐 Encrypt messages using AES (Advanced Encryption Standard).
🧾 Generate HMAC (Hash-based Message Authentication Code) for authentication and integrity.
🖼️ Maintain the visual quality of the image with minimal distortion.
🖥️ Provide a user-friendly GUI for encoding and decoding operations.

💡 Motivation
Traditional steganography methods using LSB are vulnerable to detection and tampering. This project enhances the security by:
Encrypting the message using AES.
Verifying the authenticity using HMAC-SHA256.
Preserving image quality with minimal perceptible changes.
This makes it ideal for secure digital communication in privacy-critical applications.

🛠️ Methodology
The system is built in three main layers:
1. User Interface Layer:
Select image for hiding data.
Input secret message.
Trigger encoding/decoding.
Display status messages.

2. Core Processing Layer:
Encryption: Encrypt message using AES.
HMAC Generation: Compute HMAC for data verification.
LSB Embedding: Hide encrypted data and HMAC in the image.

3. Storage Layer:
Save encoded stego image.
Retrieve and decode the image to extract the message.

🔄 Workflow
➕ Encoding Flow:
Input plaintext message.
Encrypt using AES.
Generate HMAC from plaintext.
Embed Ciphertext + HMAC + AES Key into image using LSB.
Save the stego image.

➖ Decoding Flow:
Select encoded image.
Extract Ciphertext, HMAC, and Key.
Verify key.
Validate HMAC integrity.
If valid, decrypt and display message. If not, show error.

🧪 Results
Performance was evaluated using the following metrics:
Metric	Basic LSB	LSB + AES	LSB + AES + HMAC
MSE	0.0312	0.000	0.000
PSNR (dB)	77.76	91.75	92.06
SSIM	0.925	1.00	1.00
NCC	0.989	1.00	1.00
Entropy Diff.	0.04	0.00	0.00

🔍 Visual Quality: Preserved with negligible distortion.

🔐 Security: AES and HMAC integration improved protection.

📈 Scalability: Tested with 100 and 1000 characters, minimal image degradation.

📷 GUI Snapshots
Secure login window.
![image](https://github.com/user-attachments/assets/2d65f678-87ca-42e0-87a8-f2a473365cef)
Main dashboard (Encode / Decode).
![image](https://github.com/user-attachments/assets/f9c29c05-ac02-468a-beff-7258c112a77f)
Encoding setup (Image + Message + Keys).
![image](https://github.com/user-attachments/assets/758349e1-7ef0-478f-97e9-720274a45649)
Decoding window (Image + Keys → Revealed message).
![image](https://github.com/user-attachments/assets/86eea95e-bff7-4270-8fc2-ad4cf7d4b08f)

📚 Technologies Used
Python – Core programming language.
Tkinter – GUI development.
PIL (Pillow) – Image processing.
PyCryptodome – AES and HMAC implementation.

📖 References
Includes studies on LSB-based techniques, AES encryption, HMAC algorithms, and comparisons with modern steganographic methods.


