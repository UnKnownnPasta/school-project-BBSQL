from tkinter import *

root = Tk()
background_image = None

def main():
    global background_image
    # Login window details
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='plus.png'))
    root.geometry('600x400')
    root.resizable(False, False)

    background_image = PhotoImage(file='bloodcells.png')
    background_label = Label(root, image=background_image, text='a')
    background_label.place(x=0, y=0, width=600, height=400)

main()
root.mainloop()