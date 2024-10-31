# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 23:46:30 2024

@author: tayta
"""

"""
The hierarchy of tkinter:
                            ROOT:
            Frame (entry_frame):   Frame ():


The steps to get frame onto the root window:
1. Make the frame
2. Run pack(can specify dimensions, but objects/frames get added sequentially; by default, it allows resizing of the window), 
    place,
    or grid (splits the root window into a grid of columns and rows)

    This is called geometry management
"""



import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import openpyxl
import os
import InventoryFunc as IF



def toggle_mode():
    if mode_switch.instate(['selected']): #selected means the switch has been pressed once. Default is unselected.
        style.theme_use('forest-light')
    else:
        style.theme_use('forest-dark')

def file_dialog():
    #filename = filedialog.askopenfilename(initialdir = os.getcwd(), 
     #                                     title = 'Select a File', 
      #                                    filetype = (("xlsx files", '*.xlsx')))
    filename = os.getcwd() + '\InventoryList.xlsx'
    
    for i in range(len(filename) - 1, 0, -1):
        if filename[i] == '/':
            data_label['text'] = '... ' + filename[i:]
            break
        else: 
            continue
    
    global file_path 
    path_label['text'] = filename
    file_path = filename
    
def load_data():
    
    file_path = path_label['text']
    try:
        doc_filename = r'{}'.format(file_path)
    
        match doc_filename[-3:]:
            case 'lsx':
                df = pd.read_excel(doc_filename)
            case 'csv':
                df = pd.read_csv(doc_filename)
            case 'pkl':
                df = pd.read_pickle(doc_filename)
    except ValueError:
        ttk.messagebox.showerror('Information:', 'The file you have selected is invalid.')
        return None
    except FileNotFoundError:
        ttk.messagebox.showerror('Information:', f'The file {file_path} cannot be found')
        return None
    clear_data()
    
    treeview['column'] = list(df.columns)
    treeview['show'] = 'headings'
    for column in treeview['columns']:
        treeview.heading(column, text = column)
    
    #will check to make sure the specified col_heads list is the same as the headers in the list_values headers
    #then adding the headers to the treeview
    
    df_rows = df.to_numpy().tolist()
    for col_heads in df_rows:
        treeview.heading(col_heads, text = col_heads)



def clear_data():
    treeview.delete(*treeview.get_children())

def insert_row():
    #retrieving data from the entry frame
    name = name_entry.get()
    brand = brand_entry.get()
    stock = stock_spinbox.get()
    unit = unit_drop.get()
    #buy = 'Buy' if a.get() else 'No'
    
    #Insert row into sheet

    row_values = [name, brand, stock, unit]
    treeview.insert('',tk.END, values = row_values)
    
    #Insert into the treeview
    
    
root = tk.Tk()

style = ttk.Style(root)

root.tk.call('source', 'forest-dark.tcl')
root.tk.call('source', 'forest-light.tcl')
style.theme_use('forest-dark')

#the list of options for the units dropdown menu
combo_list = ['Pieces','Gallons','Bags','Lbs']


frame = ttk.Frame(root) #refer to the hierarchy to see why root.
frame.pack()

#Far Left side of the window
entry_frame = ttk.LabelFrame(frame, text = 'Insert Item')
entry_frame.grid(row = 0, column = 0, padx=20, pady= 10) #pad is the space between objects. x being x-axis, y being y-axis
                                                        #in this case, these padx/y gives space between window edges and the entry_box

#Name Entry Box
name_entry = ttk.Entry(entry_frame)
#insert put text into a spot
name_entry.insert(0, 'Item Name') #(index, text in box)
#bind is putting a function to an action. FocusIn is the act of going into the textbox
name_entry.bind('<FocusIn>', lambda e: name_entry.delete('0','end'))
name_entry.bind('<FocusOut>', lambda e: name_entry.insert(0,'Item Name'))
name_entry.grid(column=0, row = 0, sticky = 'ew', padx= 5, pady= (0,5)) #sticky is the 'direction' of the entry box. ew = East to West (left to right)
                                                #the pady = (0,5) indicates no space ontop, but 5 units on bottom

#Brand Entry Box
brand_entry = ttk.Entry(entry_frame)
brand_entry.insert(0, 'Brand Name')
brand_entry.bind('<FocusIn>', lambda e: brand_entry.delete('0','end'))
brand_entry.bind('<FocusOut>', lambda e: brand_entry.insert(0,'Brand Name'))
brand_entry.grid(column = 0, row = 1, sticky= 'ew', padx= 5, pady= 5)


#Stock Spin Box
stock_spinbox = ttk.Spinbox(entry_frame, from_=1, to_= 100)
stock_spinbox.grid(column= 0, row = 2, sticky= 'ew', padx= 5, pady= 5)
stock_spinbox.insert(0, 'Stock')
stock_spinbox.bind('<FocusIn>', lambda e: stock_spinbox.delete('0','end'))
stock_spinbox.bind('<FocusOut>', lambda e: stock_spinbox.insert(0,'Stock'))

#Unit Dropdown Menu
unit_drop = ttk.Combobox(entry_frame, values= combo_list)
unit_drop.current(0) #The default option for the dropdown
""" unit_drop.insert(0,'Units')
unit_drop.bind('<FocusIn>', lambda e: unit_drop.delete('0','end'))
unit_drop.bind('<FocusOut>', lambda e: unit_drop.insert(0,'Units')) """
unit_drop.grid(row = 3, column = 0, sticky='ew', padx= 5, pady= 5)

#Buy More Check box
a = tk.BooleanVar() #True for click, False for unclicked
buy_button = ttk.Checkbutton(entry_frame, text='Buy More', variable= a)
buy_button.grid(row= 4, column = 0, sticky= 'nsew', padx= 5, pady= 5) #nsew: North South East West, makes the box

#Buttons:
ins_button = ttk.Button(entry_frame, text='Insert Item', command= insert_row())
ins_button.grid(row=5, column = 0, sticky='nsew', padx= 5, pady= 5)

#Making a frame to be used for the data browsing/loading 
data_frame = ttk.Labelframe(entry_frame,text= 'Open file')
data_frame.grid(row= 7, column = 0, padx = 20, pady = 20)

#making a button to load data
data_button = ttk.Button(data_frame, text= 'Browse Files', command = lambda: file_dialog())
data_button.grid(row= 0, column = 0, padx = (5,2), pady = 5)

load_button = ttk.Button(data_frame, text= 'Load Data', command = lambda: load_data())
load_button.grid(row=0, column = 1, padx = (3,5), pady= 5)

data_label = ttk.Label(entry_frame, text = 'No File Selected')
data_label.grid(column=0, row = 8)
path_label = ttk.Label(entry_frame, text = 'Path')

#Separator Bar
separator = ttk.Separator(entry_frame)
separator.grid(column=0, row=9, padx= (10,10), pady=10,sticky='ew')

#Dark/Light Mode Selector
mode_switch = ttk.Checkbutton(entry_frame, text= 'Mode', style= 'Switch', command= toggle_mode)
mode_switch.grid(row= 10, column=0, padx= 5, pady= 10, sticky='nsew')


#Creating a Treeview
treeFrame = ttk.Frame(frame)
treeFrame.grid(row= 0, column= 1, pady = 10)

#Creating the scroll bar for the treeview
treescroll = ttk.Scrollbar(treeFrame)
treescroll.pack(side='right',fill= 'y')

#creating the headers
col_heads = ('Name','Brand','Stock','Units')
treeview = ttk.Treeview(treeFrame, show='headings', 
                        yscrollcommand=treescroll.set, #y scolling moved based on the treescroll 
                        columns=col_heads, height= 13)

#sets the width of the headers
treeview.column('Name', width= 100)
treeview.column('Brand', width= 100)
treeview.column('Stock', width= 35)
treeview.column('Units', width= 50)

treeview.pack()

#tells the treeview to move with the scroll bar
treescroll.config(command=treeview.yview)



root.mainloop()