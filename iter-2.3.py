from tkinter import messagebox, font, ttk
from tkinter import *
import mysql.connector as sql

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()

root = Tk()

def main():
    global root, bg_img, logo_img
    bg_img = PhotoImage(file='bg-blur.png')
    logo_img = PhotoImage(file='l2.png')
    root.title('Blood Bank Mng')
    root.iconphoto(False, PhotoImage(file='logo.png'))
    root.geometry(f"{940}x{500}+{(root.winfo_screenwidth() - 940) // 2}+{(root.winfo_screenheight() - 500) // 2}")
    root.resizable(False, False)

    canvas = Canvas(root, width='940', height='500', highlightthickness=0)
    canvas.create_image(0, 0, image=bg_img, anchor='nw')
    canvas.pack(side = "top", fill = "both", expand = True)

    # buttonLooks = {
    #         'relief':FLAT, 'font':('Josefin Sans', 13),
    #         'bg':'#33363D', 'fg':'white', 'activebackground':'#33363D', 'activeforeground':'white'
    # }

    sText = canvas.create_text(250, 180, text='Welcome..', anchor='nw', font=('Josefin Sans', 36), fill='white')
    altText = canvas.create_text(320, 48, text='BLOOD BANK MANAGEMENT', anchor='nw', font=('Josefin Sans', 20, 'bold'), fill='white')
    canvas.create_image(230, 30, image=logo_img, anchor=NW)



def LoginPage() -> None:
    def on_focus_1(event): userName.delete(0, 'end') if userName.get().strip() == "User Name"  else None
    def on_focus_2(event): userPass.delete(0, 'end') if userPass.get().strip() == "Password" else None
    def off_focus_1(event): userName.insert(0, 'User Name') if userName.get().strip() == "" else None
    def off_focus_2(event): userPass.insert(0, 'Password') if userPass.get().strip() == "" else None
    userName = Entry(root, bd=16, relief=FLAT, width=70)
    userName.insert(0, 'User Name')
    userName.bind('<FocusIn>', on_focus_1)
    userName.bind('<FocusOut>', off_focus_1)

    userPass = Entry(root, bd=16, relief=FLAT, width=70)
    userPass.insert(0, 'Password')
    userPass.bind('<FocusIn>', on_focus_2)
    userPass.bind('<FocusOut>', off_focus_2)

    submBtn = Button(root, text='Submit', background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', command= lambda: program(userName.get(), userPass.get()))

    userName.place(x=300, y=250)
    userPass.place(x=300, y=310)
    submBtn.place(x=300, y=370)

def program(un, pw):
    pass

main()
root.mainloop()