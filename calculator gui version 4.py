import math
import tkinter as tk
from tkinter import messagebox
from tkinter import *
import os

def  screen():
    global main_screen
    global no,o,op

    main_screen= Tk ()
    main_screen.geometry("300x250")
    main_screen.title("Graphical Calculator")
    main_screen['bg']='green'

    no = IntVar()
    o = IntVar()

    op=StringVar()
    d=DoubleVar()
    
    
    Label(main_screen,text="enter first no.", bg="blue", width="300", height="2", font=("Calibri", 24)).pack()
    first_entry = Entry(main_screen,font=('calibri',24),bg="maroon" , textvariable=no).pack()
    Label(main_screen,text="enter second no.", bg="blue", width="300", height="2", font=("Calibri",24)).pack()

    second_entry = Entry(main_screen,font=('calibri',24),bg="maroon" ,textvariable=o).pack()
    Label(main_screen,text="enter operator", bg="blue", width="300", height="2", font=("Calibri",24)).pack()
    opt = Entry(main_screen,font=('calibri',24),bg="maroon", textvariable=op).pack()
    Button(main_screen,text="calculate", height="2",bg="aqua",width="30",font=("calibri",24), command = calculation ).pack()
    Button(main_screen,text="exit the pages", height="2",bg="aqua",width="30",font=("calibri",24), command =ExitApplication1 ).pack()

    
    Label(main_screen,text="", bg="red", width="300", height="2", font=("Calibri", 24)).pack()
    Label(main_screen,text="", bg="red", width="300", height="2", font=("Calibri", 24)).pack()
    Label(main_screen,text="", bg="red", width="300", height="2", font=("Calibri", 24)).pack()
    
    main_screen.mainloop()

def calcu(a,b,opt):
    
    if opt=="*" :
        d=a*b
    elif opt == "/":
        d=a/b
    elif opt == "+":
        d=a+b
    
    elif opt == "-":
        d=a-b
    elif opt == 'square of a':
        d=a*a   
    elif opt == 'square of b':
        d=b*b
    elif opt == 'cube of a':
        d=a*a*a
    
    elif opt == 'cube of b':
        d=b*b*b
    elif opt == 'a sq - b sq':
        d=(a*a)-(b*b)
    elif opt == '(a+b)sq':
        d=(a+b)*(a+b)
    elif opt == '(a+b)sq':
        d=(a-b)*(a-b)
    
    elif opt == 'a sq + b sq':
        d=(a*a)+(b*b)
    elif opt == 'a cube - b cube':
        d=(a*a*a)-(b*b*b)
    elif opt == 'a cube + b cube':
        d=(a*a*a)+(b*b*b)
    elif opt == '(a+b) cube':
        d=(a+b)*(a+b)*(a+b)
    
    elif opt == '(a-b) cube':
        d=(a-b)*(a-b)*(a-b)
    elif opt == 'sq rt of a':
        d=math.sqrt(a)
    elif opt == 'sq rt of b':
        d=math.sqrt(b)
    elif opt == 'cube rt of a':
        d=a**(1/3)
    
    elif opt == 'cube rt of b':
        d=b**(1/3)
    elif opt=='check remainder of a/b' or 'mod of a/b' or 'mod a/b' :
        d=a % b
    elif opt=='check remainder of b/a' or 'mod of b/a' or 'mod b/a' :
        d=b % a 
    return d


def ExitApplication1():
    MsgBox = tk.messagebox.askquestion ('Exit Application','Are you sure you want to exit the application',icon = 'warning')
    
    if MsgBox == 'yes':
       
       exit()

    else:
        tk.messagebox.showinfo('Return','You will now return to the application screen')
    

def calculation():

    no1=(no.get())
    no2=(o.get())
    oprt=op.get()
    
    global d
    d=calcu(no1,no2,oprt)
   
    
    global calculator
    calculator = Toplevel (main_screen)
    calculator.geometry("300x250")
    calculator.title("result")
    calculator['bg']='red'
    
    Label(calculator,text=('result page'), bg="Green", width="300", height="1", font=("Calibri", 36)).pack()
    Label(calculator,text="", bg="red", width="300", height="1", font=("Calibri",24)).pack()
    Label(calculator,text='The result is', bg="blue", width="300", height="1", font=("Calibri", 36)).pack()
    
    Label(calculator,text="", bg="red", width="300", height="1", font=("Calibri", 24)).pack()   
    Label(calculator,text=d, bg="blue", width="300", height="1", font=("Calibri", 24)).pack()   
    Button(calculator,text="exit the pages", height="2",bg="aqua",width="30",font=("calibri",24), command =ExitApplication1).pack()

if __name__ == "__main__":
    screen()