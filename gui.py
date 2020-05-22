import tkinter as tk
from tkinter import *
window = tk.Tk()
window.minsize(600,600)
frm_canvas = tk.Frame(master=window, width=400, height=400, bg="red")

canvas = tk.Canvas(master = frm_canvas,scrollregion=(0,0,1000,1000))
hbar=tk.Scrollbar(frm_canvas,orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM,fill=tk.X)
hbar.config(command=canvas.xview)
vbar=tk.Scrollbar(frm_canvas,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
canvas.create_line(0,0,2000,2000,50,100,200,300)
canvas.pack()
frm_parameters = tk.Frame(master=window, width=400,height=200, bg="pink")
# frm_parameters.grid(row=0,column = 1,sticky = "ES")
frm_canvas.pack(anchor = "nw",side=tk.TOP,expand=True,fill=tk.BOTH)
frm_parameters.pack(anchor = "ne",side = tk.BOTTOM,expand = False,fill=tk.BOTH)





window.mainloop()

