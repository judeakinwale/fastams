from datetime import date, timedelta


# some minor changes
today = f"{date.today()}"
tomorrow = f"{date.today() + timedelta(1)}"

print((today, tomorrow))

import qrcode
img = qrcode.make('judeakinwale@gmail.com')
type(img)  # qrcode.image.pil.PilImage
img.save("qr_codes/some_file.png")

import cv2
try:
  img = cv2.imread("qr_codes/some_file.png")
  detect = cv2.QRCodeDetector()
  value, points, straight_qrcode = detect.detectAndDecode(img)
  print(value, type(value))
except Exception() as e: print(e)

import re
 
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
email = "judeakinwale.com"

if(re.fullmatch(regex, email)):
  print(True)
# print(False)
  