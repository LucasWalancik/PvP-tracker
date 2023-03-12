from pytesseract import pytesseract
import cv2
import matplotlib.pyplot as plt



captured_video = cv2.VideoCapture( "2.mp4" )
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.tesseract_cmd = path_to_tesseract
truth, frame = captured_video.read()
should_we_end = False

current_frame = 0

while not should_we_end:
    frames_to_skip = input( f"How many frames to skip? Currently at: {current_frame}" )
    frames_to_skip = int( frames_to_skip )
    if 0 == frames_to_skip:
        exit()

    for i in range( frames_to_skip ):
        truth, frame = captured_video.read()
        current_frame+=1
    if truth:
        fig, ax = plt.subplots()
        ax.imshow( frame )
        fig.show()
    else:
        print( "That's all folks" )
        exit()