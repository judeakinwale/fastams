# from datetime import date, timedelta


# # some minor changes
# today = f"{date.today()}"
# tomorrow = f"{date.today() + timedelta(1)}"

# print((today, tomorrow))

# import qrcode
# img = qrcode.make('judeakinwale@gmail.com')
# type(img)  # qrcode.image.pil.PilImage
# img.save("qr_codes/some_file.png")

# import cv2
# try:
#   img = cv2.imread("qr_codes/some_file.png")
#   detect = cv2.QRCodeDetector()
#   value, points, straight_qrcode = detect.detectAndDecode(img)
#   print(value, type(value))
# except Exception() as e: print(e)

# import re
 
# # Make a regular expression
# # for validating an Email
# regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
# email = "judeakinwale.com"

# if(re.fullmatch(regex, email)):
#   print(True)
# # print(False)
  
# import os


# def send_email(reciepients, subject, message, image_path = None, cc = []):
#   import smtplib
#   from email.mime.text import MIMEText
#   from email.mime.image import MIMEImage
#   from email.mime.multipart import MIMEMultipart
  
#   email = os.environ['SMTP_EMAIL']
#   password = os.environ['SMTP_PASSWORD']
#   host = os.environ['SMTP_HOST']
#   port = os.environ['SMTP_PORT']

#   # Create a MIME multipart message
#   msg = MIMEMultipart()
#   msg['From'] = email
#   msg['To'] = ', '.join(reciepients)
#   msg['Cc'] = ', '.join(cc)
#   msg['Subject'] = subject

#   # Attach the message to the MIME message
#   msg.attach(MIMEText(message, 'plain'))

#   # Attach the image
#   if image_path:
#     with open(image_path, 'rb') as f:
#       img_data = f.read()
#       image = MIMEImage(img_data, name='image.jpg')
#       msg.attach(image)

#   # Connect to the SMTP server 
#   server = smtplib.SMTP(host, port)
#   server.starttls()

#   # Login to your account
#   server.login(email, password)

#   all_reciepients = reciepients + cc

#   # Send the email
#   server.sendmail(email, all_reciepients, msg.as_string())

#   # Close the connection
#   server.quit()



# # Provide the necessary information
# email = 'your_email@gmail.com'
# password = 'your_password'
# reciepients = ['recipient_email@example.com']
# subject = 'Hello from Python!'
# message = 'This is a test email sent using Python.'

# # Call the function to send the email
# send_email(reciepients, subject, message)
