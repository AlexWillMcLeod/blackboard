from tkinter import*
import turtle, subprocess, os



def CreateDrawingBox():

    global DrawingBoard

    DrawingBoard = Canvas(master = root, width = 1700, height = 1080, bg=DefBG, bd=0, highlightthickness=0)
    DrawingBoard.place(x=768, y=540, anchor = CENTER)

    DrawingBoard.bind("<Leave>", Left)
    DrawingBoard.bind("<Enter>", Entered)

def Left(event):

    root.unbind("<B1-Motion>")

def Entered(event):

    root.bind("<B1-Motion>", Draw)



def CreateSideButtons():

    global ResetAll

    Eraser = Button(root, text="Eraser", bg=SecFG, font=(DefFont, 30), relief='raised', bd=0, activebackground=SecFG, activeforeground=SecBG, fg=SecBG, command = ActivateEraser, width = 10, takefocus=False)
    Eraser.place(x=1630, y = 100, anchor = W)

    for x in range(4):
        CreateColourButton(x)

    for i in range(4):
        CreateThicknessButton(i)

    Calculator = Button(root, text="Calculator", bg=SecBG, font=(DefFont, 30), relief='raised', bd=0, activebackground=SecBG, activeforeground="Orange", fg="Orange", command = ActivateCalculator, width = 10, takefocus=False)
    Calculator.place(x=1630, y = 400, anchor = W)


    ResetAll = Button(root, text="Clear", bg=DefRed, font=(DefFont, 30), relief='raised', bd=0, activebackground=DefRed, activeforeground=DefFG, fg=DefFG, command = AskToReset, width = 10, takefocus=False)
    ResetAll.place(x=1630, y = 800, anchor = W)

def CreateThicknessButton(i):

        x_coords = [1630, 1691, 1753, 1814]

        globals()["Thickness" + str(i + 1)] = Button(root, text=str(i + 1), bg=SecBG, font=(DefFont, 30), relief='raised', bd=0, activebackground=SecBG, activeforeground=DefFG, fg=DefFG, command = lambda: ChangeThickness(i + 1), width = 2, takefocus=False)
        globals()["Thickness" + str(i + 1)].place(x=x_coords[i], y = 300, anchor = W)
        
def CreateColourButton(i):
    
        text_colours = ["R","G","B","W"]
        colours = [DefRed, DefGreen, DefBlue, DefFG]
        x_coords = [1630, 1691, 1753, 1814]

        globals()["Colour" + str(i)] = Button(root, text=str(text_colours[i]), bg=SecBG, font=(DefFont, 30), relief='raised', bd=0, activebackground=SecBG, activeforeground=colours[i], fg=colours[i], command = lambda: ChangeColour(colours[i]), width = 2, takefocus=False)
        globals()["Colour" + str(i)].place(x=x_coords[i], y = 200, anchor = W)
        

def ActivateCalculator():

    if process_exists("Calculator.exe") == True:
        os.system("TASKKILL /F /IM Calculator.exe")

    subprocess.Popen('C:\\Windows\\System32\\calc.exe')

def ChangeThickness(Width):

    global Thickness
    global Eraser

    try:
        for i in range(4):
            globals()["Thickness" + str(i + 1)].config(bg=SecBG, fg=DefFG, activeforeground = DefFG, activebackground=SecBG)
    except:
        pass

    Thickness = (int(Width) * 0.8) - 0.5
    
    try:
        globals()["Thickness" + str(Width)].config(bg=DefFG, fg=SecBG, activeforeground = SecBG, activebackground=DefFG)
    except:
        pass
        
    Eraser = False

def ChangeColour(NewColour):

    global Colour
    global Thickness
    global Eraser

    Eraser = False

    Cancel()

    Colour = NewColour

def ActivateEraser():
    global Colour
    global Thickness
    global Eraser

    Eraser = True


def Cancel():

    global Confirm
    global ResetAll

    try:
        ResetAll.config(text="Clear", command = AskToReset)
    except:
        pass

    try:
        Confirm.destroy()
    except:
        pass


def AskToReset():

    global Confirm

    Confirm = Button(root, text="Confirm", bg=SecBG, font=(DefFont, 30), relief='raised', bd=0, activebackground=SecBG, activeforeground=DefGreen, fg=DefGreen, command = Reset, width = 10, takefocus=False)
    Confirm.place(x=1630, y = 900, anchor = W)

    ResetAll.config(text="Cancel", command = Cancel)

def Reset():
    
    Cancel()

    DrawingBoard.destroy()
    CreateDrawingBox()



def Release(event):

    global old_x
    global old_y

    old_x, old_y = None, None


def Draw(event):

    global old_x
    global old_y
    global Eraser

    root.unbind("<B1-Motion>")

    if Eraser == True:
        NewThickness = 45
        NewColour = DefBG
    else:
        NewThickness = Thickness
        NewColour = Colour

    try:
        DrawingBoard.create_line(old_x, old_y, event.x, event.y, width = NewThickness, fill=NewColour, smooth = TRUE, splinesteps = 1000, capstyle=ROUND)
    except:
        pass

    old_x = event.x
    old_y = event.y

    root.bind("<B1-Motion>", Draw)

def process_exists(process_name):
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())









def Init():

    global root
    global DefFont
    global DefBG
    global DefFG
    global SecBG
    global SecFG
    global Thickness
    global Colour
    global DefRed
    global DefGreen
    global DefBlue
    global Eraser

    DefBG = 'gray13'
    DefFG = 'gray87'
    SecBG = 'gray19'
    SecFG = 'gray77'
    DefFont = 'Product Sans'
    DefRed = 'orangered1'
    DefGreen = 'forest green'
    DefBlue = 'steel blue'

    
    ChangeColour(DefFG)

    Eraser = False

    root = Tk()
    root.state('zoomed')
    root.title('Blackboard')
    root.config(bg=DefBG)

    CreateDrawingBox()
    
    CreateSideButtons()
    
    root.bind("<ButtonRelease-1>", Release)
    root.bind("<B1-Motion>", Draw)

    ChangeThickness(3)

    root.mainloop()




Init()
