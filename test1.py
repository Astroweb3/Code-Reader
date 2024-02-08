import cv2
import pytesseract 
from PIL import Image
from bs4 import BeautifulSoup

cv2.namedWindow("Scan Image")
cam = cv2.VideoCapture(0)
while cam.isOpened():
    _,image = cam.read()
    cv2.putText(image,"Press 's' key to Scan",(20,20),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255,0),2)
    cv2.imshow('Scanner',image)
    if cv2.waitKey(25) & 0xFF==ord('s'):
        cv2.imwrite('image.jpg',image)
        break
cam.release()
cv2.destroyAllWindows()
image_path = 'image.jpg'

with Image.open(image_path) as img:
    text = pytesseract.image_to_string(img)
    
print(text)

soup = BeautifulSoup(text,'html.parser')
ouput = soup.get_text()
print(ouput)

