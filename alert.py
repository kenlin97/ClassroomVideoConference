import winsound
from tkinter import *
from random import randint

#first param is the file name. search here for more info https://www.geeksforgeeks.org/python-winsound-module/

def getcorrect(userans, realans):
    print("real answer: " + str(realans))
    print("user entered: " + userans)
    if userans == str(realans):
        return True
    else:
        return False


def alertuser():

    winsound.PlaySound("Loud_Alarm_Clock_Buzzer.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

    randval1 = randint(1, 50)
    randval2 = randint(1, 50)
    mathquestion = "Solve this question this turn alarm off: " + str(randval1) + "+" + str(randval2)
    realanswer = randval1 + randval2
    # Create Tkinter POPUP gui
    root = Tk()
    root.overrideredirect(True)
    label = Label(root, text= mathquestion).pack()
    e = Entry(root, text="Type here")
    e.pack()

    initial = False

    def submit(answer, init):

        correct = getcorrect(e.get(), answer)
        print(correct)
        if correct:
            wronglabel = Label(root, text = "Correct").pack()
            root.destroy()
            winsound.PlaySound(None, winsound.SND_PURGE)

        elif correct == False:
            wronglabel = Label(root, text = "Incorrect").pack()
        else:
            return

    submitbtn = Button(root, text="Submit Answer", command= lambda: submit(realanswer, initial))
    submitbtn.pack()

    root.mainloop()

######################################################



