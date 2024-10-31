# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 22:17:59 2024

@author: tayta
"""

#Graphical packages
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd
import os

#The starting graphical object or otherwise the window itself
root = tk.Tk()

#dimensions of the window
root.geometry('500x500')

#False means the window will not shrink/largen based on the things inside the window
root.pack_propagate(False) 


#How the window will be resized. In this case, it will not be allowed
root.resizable(0,0) 

#The lable of the window and what window it is labeleing. This is teh frame for TreeView
frame1 = tk.LabelFrame(root, text = 'Excel Data')

#puts the window location
frame1.place(height= 250,width= 500)

#Frame for open file dialog
file_frame = tk.LabelFrame(root,text='Open File')

#place the window at the far left, 65% down the page. 
file_frame.place(height = 100, width = 400, rely = 0.65, relx = 0)


#Buttons
button1 = tk.Button(file_frame, text = 'Browse A File',command = lambda: file_dialog()) #will add a command to look into file system
button1.place(rely = 0.65, relx = 0.5)

button2 = tk.Button(file_frame, text= 'Load File', command = lambda: load_excel_data()) #will add a command to load the file
button2.place(rely = 0.65, relx = 0.3)

#A label within the frame that is just there
label_file = ttk.Label(file_frame, text = 'No File Selected')
label_file.place(rely = 0, relx = 0)


# TreeView Widget

tv1 = ttk.Treeview(frame1)
tv1.place(relheight = 1, relwidth = 1)

#Adds a y-axis scoller bar if there is more data than can be seen. The command is what window is being looked/scrolled
treescrolly = tk.Scrollbar(frame1, orient = 'vertical', command= tv1.yview)
treescrollx = tk.Scrollbar(frame1, orient = 'horizontal', command = tv1.xview)

#Actually puts the scroll bars onto the widget
tv1.configure(xscrollcommand = treescrollx.set, yscrollcommand = treescrolly.set)
treescrollx.pack(side = 'bottom', fill = 'x') #placing the x scroll bar
treescrolly.pack(side = 'right', fill = 'y') #placing the y scroll bar

#Creating Functions:
    
    #Opens the dialog box to get a file
def file_dialog():
    #below is the way to get a file system open to select a file
    filename = filedialog.askopenfilename(initialdir = os.getcwd(), 
                                          title = 'Select a File', 
                                          filetype = (("xlsx files", '*.xlsx'),('pickle files','*.pkl'),('All Files', '*.*')))
    label_file['text'] = filename
    return None

    #Actually loads that file in
def load_excel_data():
    file_path = label_file['text']
    try:
        
        doc_filename = r'{}'.format(file_path) #Puts the file name into the path
        
        match doc_filename[-3:]: #matches the file extension to what function it needs
            case 'lsx':
                df = pd.read_excel(doc_filename)            
            case 'csv':
                df = pd.read_csv(doc_filename)
            case 'pkl':
                df = pd.read_pickle(doc_filename)
                
    except ValueError:
        tk.messagebox.showerror('Information', 'The file you have selected is invalid.')
        return None
    except FileNotFoundError:
        tk.messagebox.showerror('Information', f'The file {file_path} cannot be found')
        return None
    
    clear_data()
    
    tv1['column'] = list(df.columns)
    tv1['show'] = 'headings'
    for column in tv1['columns']:
        tv1.heading(column, text= column)
    
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv1.insert("","end", values = row) #inserts the row into the treeview
        
    return None
def clear_data():
    tv1.delete(*tv1.get_children()) #will clear treeview
    



#the loop for the GUI looping
root.mainloop()
