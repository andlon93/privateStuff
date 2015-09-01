from Tkinter import *

board = [[0 for x in range(5)] for x in range(5)] 
board[0][0] = 1
board[4][0] = 5

root = Tk()

w = Label(root, text="red", bg="red", fg="white")
w.pack(padx=5, pady=10, side=LEFT)

w = Label(root, text="green", bg="green", fg="black")
w.pack(padx=5, pady=20, side=LEFT)

w = Label(root, text="blue", bg="blue", fg="white")
w.pack(padx=5, pady=20, side=LEFT)

mainloop()