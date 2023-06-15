from tkinter import messagebox, font, ttk
from tkinter import *
import mysql.connector as sql
import time, re
from PIL import Image, ImageTk

global con, cur
con = sql.connect(host='localhost', user='root', password='root')
cur = con.cursor()
cur.execute('use bloodbank')


global root, bg_img, logo_img, arrow
root = Tk()
bg_img_1 = PhotoImage(file='bg-blur-v2.png')
bg_img_2 = PhotoImage(file='bg-unblur.png')
logo_img = PhotoImage(file='l3-2.png')
logo_img2 = PhotoImage(file='l2-2.png')
arrow = PhotoImage(file='skills-3.png')
root.title('Blood Bank Mng')
root.iconphoto(False, PhotoImage(file='logo.png'))
root.geometry(f"{940}x{500}+{(root.winfo_screenwidth() - 940) // 2}+{(root.winfo_screenheight() - 500) // 2}")
root.resizable(False, False)


def SignUp():
    global hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu
    canvasSu = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasSu.create_image(0, 0, image=bg_img_1, anchor='nw')
    canvasSu.pack(side = "top", fill = "both", expand = True)

    sText = canvasSu.create_text(240, 180, text='Enter Details to Create A Account..', anchor=NW, font=('Josefin Sans', 17), fill='white')
    altText = canvasSu.create_text(320, 48, text='BLOOD BANK MANAGEMENT', anchor=NW, font=('Josefin Sans', 20, 'bold'), fill='white')
    canvasSu.create_image(230, 30, image=logo_img2, anchor=NW)

    def setText(entry, defText):
        entry.delete(0, END) if entry.get().strip() == defText else None
        
    def restoreText(entry, defText):
        entry.insert(0, defText) if entry.get().strip() == "" else None

    hospName = Entry(root, bd=16, relief=FLAT, width=70)
    hospName.insert(0, 'Hospital Name')
    hospName.bind('<FocusIn>', lambda event: setText(hospName, 'Hospital Name'))
    hospName.bind('<FocusOut>', lambda event: restoreText(hospName, 'Hospital Name'))

    pinCode = Entry(root, bd=16, relief=FLAT, width=22)
    pinCode.insert(0, 'Pin Code')
    pinCode.bind('<FocusIn>', lambda event: setText(pinCode, 'Pin Code'))
    pinCode.bind('<FocusOut>', lambda event: restoreText(pinCode, 'Pin Code'))

    Contact = Entry(root, bd=16, relief=FLAT, width=40)
    Contact.insert(0, 'Contact (Phone No./email)')
    Contact.bind('<FocusIn>', lambda event: setText(Contact, 'Contact (Phone No./email)'))
    Contact.bind('<FocusOut>', lambda event: restoreText(Contact, 'Contact (Phone No./email)'))
    
    PassWord = Entry(root, bd=16, relief=FLAT, width=70)
    PassWord.insert(0, 'Enter a Strong Password')
    PassWord.bind('<FocusIn>', lambda event: setText(PassWord, 'Enter a Strong Password'))
    PassWord.bind('<FocusOut>', lambda event: restoreText(PassWord, 'Enter a Strong Password'))


    swchBtnSu = Button(root, command=switchS_L, image=arrow, relief=FLAT, bd=0, highlightthickness=0, activebackground='#ad1e1e')
    submBtnSu = Button(root, text='Submit', background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', command= lambda: SignSubm(pinCode.get(), Contact.get(), hospName.get(), PassWord.get()))

    hospName.place(x=240, y=250)
    pinCode.place(x=240, y=310)
    Contact.place(x=420, y=310)
    PassWord.place(x=240, y=370)
    submBtnSu.place(x=425, y=430)
    swchBtnSu.place(x=770, y=30)


def Login():
    global canvasLi, userName, userPass, submBtnLi, signBtnLi
    canvasLi = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasLi.create_image(0, 0, image=bg_img_2, anchor='nw')
    canvasLi.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvasLi.create_text(355, 58, text='ADMIN', anchor='nw', font=('Franklin Gothic', 25, 'bold'), fill='white')
    titleLabel2 = canvasLi.create_text(470, 46, text='Login', anchor='nw', font=('Josefin Sans', 25), fill='white')

    sText = canvasLi.create_text(240, 180, text='Sign In', anchor='nw', font=('Franklin Gothic', 16, 'bold'), fill='white')
    altText = canvasLi.create_text(240, 200, text='Fill in details to gain access', anchor='nw', font=('Josefin Sans', 14), fill='white')

    def setText(entry, defText):
        entry.delete(0, END) if entry.get().strip() == defText else None

    def restoreText(entry, defText):
        entry.insert(0, defText) if entry.get().strip() == "" else None

    userName = Entry(root, bd=16, relief=FLAT, width=70)
    userName.insert(0, 'User Name')
    userName.bind('<FocusIn>', lambda event: setText(userName, 'User Name'))
    userName.bind('<FocusOut>', lambda event: restoreText(userName, 'User Name'))

    userPass = Entry(root, bd=16, relief=FLAT, width=70)
    userPass.insert(0, 'Password')
    userPass.bind('<FocusIn>', lambda event: setText(userPass, 'Password'))
    userPass.bind('<FocusOut>', lambda event: restoreText(userPass, 'Password'))

    submBtnLi = Button(root, text='Login', background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', command= lambda: program(userName.get(), userPass.get()))
    signBtnLi = Button(root, text='Sign Up', background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', command=switchL_S)

    userName.place(x=240, y=260)
    userPass.place(x=240, y=320)
    submBtnLi.place(x=370, y=380)
    signBtnLi.place(x=460, y=380)


def switchS_L(): # Signup to Login
    w = [hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu]
    for i in w:
        i.destroy()
    Login()
def switchL_S(): # Login to Signup
    w = [canvasLi, userName, userPass, submBtnLi, signBtnLi]
    for i in w:
        i.destroy()
    SignUp()


def SignSubm(pstCde, cntct, hospNme, paswrd):
    verf = pinVerify(pstCde)
    if verf == False:
        messagebox.showerror('Failed', 'Invalid Pin Code.')
        return
    if hospNme == 'Hospital Name' or len(hospNme) == 0:
        messagebox.showerror('Failed', 'Invalid Hospital Name.')
        return
    if len(cntct) == 0 or cntct == 'Contact (Phone No./email)':
        messagebox.showerror('Failed', 'No Valid Contacts provided.')
        return
        
    messagebox.showinfo('Success', 'Account created successfully! Login to it here')
    switchS_L()


def pinVerify(pin) -> True:
    if not pin.isdigit() or pin[0] == '0' or len(pin) != 6:
        return False
    invalid = [29, 35, 54, 55, 65, 66]
    if pin[:2] in invalid:
        return False
    reg = open('validrange.txt')
    status = False
    for i in range(8):
        regx = reg.readline().strip().replace('/', '')
        m = re.findall(regx, pin)
        if len(m) != 0:
            status = True
    return status


def program(un, pw):
    w_super = [canvasLi, userName, userPass, submBtnLi, signBtnLi]
    for i in w_super:
        i.destroy()
    
    title_bar = Frame(root, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.05, relwidth=1) # relwidth gives the fill to be 100%, rely keeps it 500*0.05 = 25 pixels from top

    image_label = Label(title_bar, bg="#D22B2B", image=logo_img)
    image_label.pack(side=LEFT)

    title_label = Label(root, text="Blood Bank Management", fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
    title_label.place(x=50, y=25)

    global stg
    stg = ["", 0]
    def scroll_text(txt):
        global stg
        if stg[0] != txt:
            stg[0] += txt
            label.configure(text=" " + stg[0])

        def rotate():
            text = label.cget("text")
            rotated_text = text[1:] + text[0]
            if rotated_text == text:
                rotated_text = text
            label.config(text=" " + rotated_text + "  ")
            label.after(300, rotate)

        if not stg[1]:
            stg[1] = 1; rotate()

    label = Label(root, font=("Arial", 12), anchor=NE, bg="black", bd=2, fg="white", width=104, highlightcolor='blue', highlightthickness=1)
    label.place(x=-1, y=0)
    scroll_text('   This is some text   ')
    a = Button(root, text= 'a', command= lambda: scroll_text('   nyooooooooom   '))
    a.place(x=30, y=300)
    
SignUp()
root.mainloop()
