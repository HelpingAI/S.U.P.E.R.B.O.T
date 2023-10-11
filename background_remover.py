# importing all necessary libraries
import tkinter as tk
from rembg import remove
from PIL import Image
from tkinter import filedialog
from PIL import Image
import os
from tkinter import messagebox
import os

# defining tkinter window
top = tk.Tk()
top.geometry("400x400")
top.title('S.U.P.E.R.B.O.T.')

filename = ''

# function to select file from system
def upload_file():
    global filename
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    if len(filename) > 0:
        b1.config(state='disabled')

# function to remove backgroung of an image and then show message
def Convert(image_name):
    current_working_directory = os.getcwd()
    input_path = filename
    output_path = f'{current_working_directory}\{image_name}.png'
    image_input = Image.open(input_path)
    output = remove(image_input)
    output.save(output_path)
    messagebox.showinfo('Success', 'Image background successfully removed')
    top.destroy()


my_font1 = ('times', 18, 'bold')

# defining tkinter widgets and placing then on tkinter window GUI
l1 = tk.Label(top, text='Background Removal App', width=30, font=my_font1)
l1.grid(row=1, column=1)

b1 = tk.Button(top, text='Select here', height=2, font=('Arial', 20), bg='green', fg='white', command=lambda: upload_file())
b1.grid(row=2, column=1, pady=20)

image_name = tk.StringVar(top)
image_name.set('enter file name')

e1 = tk.Entry(top, textvariable=image_name)
e1.grid(row=3, column=1, pady=20)

b2 = tk.Button(top, text='Convert now', height=2, font=('Arial', 20), bg='green', fg='white', command=lambda: Convert(image_name.get()))
b2.grid(row=4, column=1, pady=20)

top.mainloop()

