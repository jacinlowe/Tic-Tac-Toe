import tkinter as tk


def switch_frame():
    frame1.pack_forget()
    frame2.pack()


root = tk.Tk()
rootFrame = tk.Frame(root)
frame1 = tk.Frame(rootFrame)
frame2 = tk.Frame(rootFrame)
frame3 = tk.Frame(root, width=200, height=50)
frame4 = tk.Frame(root, width=200, height=50)

rootFrame.pack()
frame1.pack()
frame3.pack()
frame4.pack()
tk.Button(frame1, text="Switch frame", command=switch_frame).pack()
tk.Button(frame2, text="Switch frame", command=switch_frame).pack()
root.mainloop()
