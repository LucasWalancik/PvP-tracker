import cv2
#import time
#from PIL import Image
#from pytesseract import pytesseract
import matplotlib.pyplot as plt
import easyocr
reader = easyocr.Reader(['en']) 


#import IPython.display as ipd
#from tqdm import tqdm



def show_image( ROI ):
    fig, ax = plt.subplots()
    ax.imshow( ROI )
    plt.show()
    x=input()


def get_ROI( phase, image ):
    if ("Finding opponent" == phase) or ("Battle starting start" == phase) or ("Battle starting" == phase):
        ROI = image[ 990:1050, 40:382 ]
    if "Opponent info" == phase:
        ROI = image[ 830:940, 260:850 ]
    if "Opponent rank" == phase:
        ROI = image[ 805:915, 90:210 ]
    return ROI

def sanitize_text( text ):
    if 0 == len( text ):
        return ""
    text = text[ 0 ]
    text = text.strip()
    text = text.strip(". ")
    text = text.strip()
    #text.strip(".")
    return text

def get_current_second( captured_video, current_frame ):
    fps = captured_video.get(cv2.CAP_PROP_FPS)
    current_second = ( current_frame/fps )
    return round( current_second, 2 )

def setup():
    #path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #pytesseract.tesseract_cmd = path_to_tesseract
    pass

def choose_battle():
    #has to be improved
    captured_video = cv2.VideoCapture( "1.mp4" )
    return captured_video


def finding_opponent( captured_video ):
    was_frame_captured, frame = captured_video.read()
    frame_count = 0
    frames_passed = 10
    finding_opponent_start = None
    battle_starting_start = None
    red_nicknames = []
    opponent_nickname = None
    opponent_rank = None
    FRAMES_TO_SKIP = 10
    phase = "Finding opponent"
    while True == was_frame_captured:
        #in future, change the pixel values that work for GALAXY A52s 5G to proportions based on the video size
        if FRAMES_TO_SKIP == frames_passed:

            ROI = get_ROI( phase, frame )
            #show_image( ROI )
            text = reader.readtext( ROI, detail=0 )
            #text = pytesseract.image_to_string( ROI )
            text = sanitize_text( text )
            #print( f"Current phase: #{phase}# current text: {text}")

            if "Finding opponent" == phase:
                if "Finding opponent" == text:
                    finding_opponent_start = get_current_second( captured_video, frame_count )
                    print( f"Finding opponent is on the screen at { finding_opponent_start }s.")
                    phase = "Battle starting start"

            if "Battle starting start" == phase:
                if "Battle starting" == text:
                    battle_starting_start = get_current_second( captured_video, frame_count )
                    print( f"Battle starting is on the screen at { battle_starting_start }s. at {frame_count} frame")
                    phase = "Battle starting"

            if "Battle starting" == phase:
                if "Battle starting" == text:
                    pass
                else:
                    battle_starting_stop = get_current_second( captured_video, frame_count )
                    print ( f"Battle starting has stopped showing at: { battle_starting_stop } s." )
                    phase = "Opponent info"
                    ROI = get_ROI( phase, frame )
                    #text = pytesseract.image_to_string( ROI )
                    text = reader.readtext( ROI, detail=0 )
                    text = sanitize_text( text )
                    FRAMES_TO_SKIP = 1


            if "Opponent info" == phase:
                red_nicknames.append( text )
                if 5 == len( red_nicknames ):
                    unique_names = set( red_nicknames )
                    if 1 == len( unique_names ):
                        opponent_nickname = red_nicknames[ 0 ]
                        ROI = get_ROI( "Opponent rank", frame )
                        opponent_rank = reader.readtext( ROI, detail=0 )
                        #opponent_rank = pytesseract.image_to_string( ROI )
                        opponent_rank = sanitize_text( opponent_rank )
                        phase = "Final countdown"
                        FRAMES_TO_SKIP = 10
                    else:
                        red_nicknames.pop( 0 )


            if "Final countdown" == phase:
                print( f"Finding opponent start: {finding_opponent_start}s")
                print( f"Battle starting start: {battle_starting_start}s")
                print( f"Nickname: #{opponent_nickname}#" )
                print( f"Rank: #{opponent_rank}#")
                exit( 0 )
            


            # if ("Finding opponent" == text) and (None == finding_opponent_start):
            #     finding_opponent_start = get_current_second( captured_video, frame_count )
            #     print( f"Finding opponent is on the screen at { finding_opponent_start }s.")
            
            # if ("Battle starting" == text) and (None == battle_starting_start):
            #     battle_starting_start = get_current_second( captured_video, frame_count )
            #     print( f"Battle starting is on the screen at { battle_starting_start }s. at {frame_count} frame")
            #     phase = "Battle starting"
            
            # if "Opponent info" == phase:
            #     print( text )
            #     fig, ax = plt.subplots()
            #     ax.imshow( ROI )
            #     fig.show()
            #     x=input()

            frames_passed = 0

        frames_passed += 1
        was_frame_captured, frame = captured_video.read()
        frame_count += 1

def battle_starting():
    pass

def opponent_info():
    pass

def the_countdown():
    pass

def rest_of_the_game():
    pass


def main_function():
    setup()
    captured_video = choose_battle()
    finding_opponent( captured_video )
    #battle_starting()
    #opponent_info()
    #the_countdown()
    #rest_of_the_game
    pass

if __name__ == "__main__":
    main_function()