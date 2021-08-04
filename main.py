import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import imutils
import time

#canba
#Declare screen width and screen height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 550

#Initialie tkinter window
window = tkinter.Tk()
window.title("Third Umpire Review System by Sayantan")

#Initialize a canvas for displayimg background image
canvas = tkinter.Canvas(window, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)

img = cv2.cvtColor(cv2.imread("welcome.jpg"), cv2.COLOR_BGR2RGB)
img = imutils.resize(img, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
canvas.image = img
canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
canvas.pack()

stream = cv2.VideoCapture("run_out.mp4")

def play(speed):
    print(f"click {speed}")
    #Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    frame = imutils.resize(frame, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def pending(decision):
    #Display decision pending image
    img = cv2.cvtColor(cv2.imread("pending.jpg"), cv2.COLOR_BGR2RGB)
    img = imutils.resize(img, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
    img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    canvas.image = img
    canvas.create_image(0, 0, image=img, anchor=tkinter.NW)

    #wait for 2 second
    time.sleep(2)
    
    #Display out/not out image
    if decision == "out":
        img = cv2.cvtColor(cv2.imread("out.png"), cv2.COLOR_BGR2RGB)
        img = imutils.resize(img, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
        img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
        canvas.image = img
        canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
    else:
        img = cv2.cvtColor(cv2.imread("not_out.png"), cv2.COLOR_BGR2RGB)
        img = imutils.resize(img, width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
        img = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
        canvas.image = img
        canvas.create_image(0, 0, image=img, anchor=tkinter.NW)
       
def out():
    thread = threading.Thread(target=pending, args = ("out",))
    thread.daemon = 1
    thread.start()
    print("out")

def not_out():
    thread = threading.Thread(target=pending, args = ("not out",))
    thread.daemon = 1
    thread.start()
    print("not out")

#Introduce buttons
button = tkinter.Button(window, text = "<< Previous(fast)", width = 50, command = partial(play, -4))
button.pack()

button = tkinter.Button(window, text = "<< Previous(slow)", width = 50, command = partial(play, -2))
button.pack()

button = tkinter.Button(window, text = "Next(fast) >>", width = 50, command = partial(play, 4))
button.pack()

#use of partial keyword -> actual syntax command = play. But this does not accept any argument inside play().
#so, use partial(play, 20). This will make compiler think that command = play is written but still internally play() will accept arguments.
button = tkinter.Button(window, text = "Next(slow) >>", width = 50, command = partial(play, 2))
button.pack()

button = tkinter.Button(window, text = "Give OUT", width = 50, command = out)
button.pack()

button = tkinter.Button(window, text = "Give NOT OUT", width = 50, command = not_out)
button.pack()

window.mainloop()
#mainloop() should always run otherwise GUI will hang. So, use thread, which will have responsibility of changing images when final decision will be out/not out

