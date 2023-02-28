
import cv2
import time
from PIL import Image
from pytesseract import pytesseract
import matplotlib.pyplot as plt


#import IPython.display as ipd
#from tqdm import tqdm


def scan_for_opponent( img ):
    ROI = img[ 990:1050, 40:382 ]
    fig, ax = plt.subplots()
    ax.imshow( ROI )
    text = pytesseract.image_to_string( ROI )
    plt.show()
    text = text.strip()
    if "Finding opponent" == text:
        return "Finding opponent"
    else:
        return None

path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract

cap = cv2.VideoCapture('1.mp4')
ret, img = cap.read()
frames = 60
seconds = 0
fps = cap.get(cv2.CAP_PROP_FPS)

finding_opponent = None
battle_starting = None
while ret:
    if frames == 60:
        if None == finding_opponent:
            finding_opponent = scan_for_opponent( img )
        

        frames = 0
    ret, img = cap.read()
    frames += 1