from tkinter import *
import ctypes
import random
import tkinter
import os

ctypes.windll.shcore.SetProcessDpiAwareness(1)

# Setup
storage = Tk()
storage.title('S.U.P.E.R.B.O.T.- Typing Speed Test')

storage.geometry('1400x700')

storage.option_add("*Label.Font", "consolas 30")
storage.option_add("*Button.Font", "consolas 30")

def handlingLabels():
    # Text List
    random_selection = [
        'A random statement can inspire authors and help them start writing. It challenges the author to use their imagination because the sentences subject is utterly ambiguous. The random sentence may be creatively used in a variety of ways by writers. The statement is most frequently used to start a tale. Another choice is to include it into the narrative. The issue of using it to conclude a tale is far more challenging. In all of these scenarios, the writer is compelled to use their imagination because they have no idea what words will come out of the tool.',
        'Python Code aims to teach beginning and intermediate programmers Python through tutorials, recipes, articles, and problem-solving techniques while also disseminating information globally. Everyone in the globe will be able to learn how to code for free thanks to Python Code. Python is a general-purpose, high-level, interpreted programming language. Code readability is prioritised in its design philosophy, which makes heavy use of indentation. Python uses garbage collection and has dynamic typing. It supports a variety of programming paradigms, including procedural, object-oriented, and functional programming as well as structured programming (especially this). Due to its extensive standard library, it is frequently referred to as a "batteries included" language.',
        'We begin with the imports as usual. We must import tkinter since we utilise it to create the user interface. In order to subsequently modify the typefaces on our components, we additionally import the font module from tkinter. The partial function is obtained from functools and is a brilliant function that accepts another function as a first argument, along with certain args and kwargs, and returns a reference to this function with those arguments. When we wish to add one of our functions to a command argument of a button or key binding, this is extremely helpful.',
        'A computer programmer is a person who writes computer programmes, frequently for bigger pieces of software. They are also known as software developers, software engineers, programmers, or coders. A programmer is a person who uses a particular programming language to construct or write computer software or applications. The majority of programmers have substantial computer and coding expertise across a wide range of platforms and programming languages, including SQL, Perl, XML, PHP, HTML, C, C++, and Java. The terms "programmer" and "software engineer" may be used to describe the same position at various businesses because there is no industry-wide vocabulary standard. Usually, a "programmer" or "software developer" will concentrate on translating a precise specification into computer code.'
    ]
    # Chosing one of the texts randomly with the choice function
    text = random.choice(random_selection).lower()

    splitPoint = 0

    global nameLabelLeft
    nameLabelLeft = Label(storage, text=text[0:splitPoint], fg='green')
    nameLabelLeft.place(relx=0.5, rely=0.5, anchor=E)

    global nameLabelRight
    nameLabelRight = Label(storage, text=text[splitPoint:])
    nameLabelRight.place(relx=0.5, rely=0.5, anchor=W)

    global currentAlphabetLabel
    currentAlphabetLabel = Label(storage, text=text[splitPoint], fg='grey')
    currentAlphabetLabel.place(relx=0.5, rely=0.6, anchor=N)

    global secondsLeft
    headingLabel = Label(storage, text=f'Vortex - Typing Speed Test', fg='blue')
    headingLabel.place(relx=0.5, rely=0.2, anchor=S)
    secondsLeft = Label(storage, text=f'0 Seconds', fg='red')
    secondsLeft.place(relx=0.5, rely=0.4, anchor=S)

    global writeAble
    writeAble = True
    storage.bind('<Key>', handlekeyPress)

    global secondsPassed
    secondsPassed = 0

    storage.after(60000, stopGame)
    storage.after(1000, timeAddition)


def stopGame():
    global writeAble
    writeAble = False

    # Calculating the amount of words
    amountWords = len(nameLabelLeft.cget('text').split(' '))

    secondsLeft.destroy()
    currentAlphabetLabel.destroy()
    nameLabelRight.destroy()
    nameLabelLeft.destroy()

    global labelOfResult
    labelOfResult = Label(storage, text=f'Words per Minute (WPM): {amountWords}', fg='black')
    labelOfResult.place(relx=0.5, rely=0.4, anchor=CENTER)

    # Display a button to restartGame the game
    global showcaseResults
    showcaseResults = Button(storage, text=f'Retry', command=restartGame)
    showcaseResults.place(relx=0.5, rely=0.6, anchor=CENTER)

def restartGame():
    # Destry result widgets
    labelOfResult.destroy()
    showcaseResults.destroy()
    handlingLabels()


    

def timeAddition():
    global secondsPassed
    secondsPassed += 1
    secondsLeft.configure(text=f'{secondsPassed} Seconds')

    if writeAble:
        storage.after(1000, timeAddition)

def handlekeyPress(event=None):
    try:
        if event.char.lower() == nameLabelRight.cget('text')[0].lower():
            nameLabelRight.configure(text=nameLabelRight.cget('text')[1:])
            nameLabelLeft.configure(text=nameLabelLeft.cget('text') + event.char.lower())
            currentAlphabetLabel.configure(text=nameLabelRight.cget('text')[0])
    except tkinter.TclError:
        pass

handlingLabels()

storage.mainloop()
os.system('python SUPERBOT.py')