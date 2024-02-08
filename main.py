import cv2
import pytesseract
from PIL import Image
import google.generativeai as genai
from configparser import ConfigParser


#scan image
cv2.namedWindow("Scan Image")
cam = cv2.VideoCapture(0)
while cam.isOpened():
    _, image = cam.read() 
    cv2.putText(image, "Press 's' to scan", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Scaner', image)
    if cv2.waitKey(25) & 0xFF == ord('s'):
        cv2.imwrite('imge.jpg',image)
        break
    
cam.release()
cv2.destroyAllWindows()


# image to text
image_path = 'imge.jpg'

with Image.open(image_path) as img:
    # Use Tesseract to do OCR on the image
    extracted_text = pytesseract.image_to_string(img)

print(extracted_text)

# text to gemini
prompt = f"find the output for this code:{extracted_text}"
config = ConfigParser()
config.read('F:/1.Project/_0Restapi/credentials.ini')
api_key = config['GOOGLE_API_KEY']['google_api_key']
genai.configure(api_key=api_key)
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k":1,
    "max_output_tokens":2048,
}
safety_settings = [
{
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
{
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
},
]

model = genai.GenerativeModel(model_name="gemini-pro",
                            generation_config=generation_config,
                            safety_settings=safety_settings)

convo = model.start_chat(history=[
])

convo.send_message(prompt)

response = convo.last.text
print(response)

