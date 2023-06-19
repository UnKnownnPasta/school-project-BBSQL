from tkinter import messagebox
from tkinter import *
import mysql.connector as sql
from re import findall
import os

current_dir = os.path.dirname(__file__)
import functions as f
import helper as h

def SignSubm(postCode, contact, hospName, passwrd):
    verf = h.pinVerify(postCode)
    if verf == False:
        messagebox.showerror('Failed', 'Invalid Pin Code.')
        return
    if hospName == 'Hospital Name' or len(hospName) == 0:
        messagebox.showerror('Failed', 'Invalid Hospital Name.')
        return
    if len(contact) == 0 or contact == 'Contact (Phone No./email)':
        messagebox.showerror('Failed', 'No Valid Contacts provided.')
        return
        
    try:
        vals = (hospName, passwrd, contact, postCode)
        query = "insert into Hospital (HospitalName, Password, Contact, PinCode) values (%s, %s, %s, %s)"
        f.cur.execute(query, vals)
        f.con.commit()
    except:
        messagebox.showerror('Error', 'Failed to signup. Try again.')
        return

    messagebox.showinfo('Success', 'Account created successfully! Login to it here')
    f.switchS_L()


def loginSubm(un, pw):
    for i in [un, pw]:
        if i == 'User Name' or i == 'Password' or len(i) == '' or i == ' ':
            messagebox.showerror('Error', 'Invalid login details')
            return
    query = "select * from hospital where HospitalName=%s and Password=%s"
    values = (un, pw)
    f.cur.execute(query, values)
    res = f.cur.fetchone()
    if res == None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return
    f.cur.execute('select HospitalID, PinCode from Hospital where HospitalName=%s', (un,))
    hId, pc = [i for i in f.cur.fetchall()[0]]
    program(un, pw, hId, pc)


def DEL_EVENT(): 
    f.topRoot.withdraw();
    profCanvas.destroy()


def program(u, p, i, pc):
    ww = [f.canvasLi, f.userName, f.userPass, f.submBtnLi, f.signBtnLi]
    for x in ww:
        x.destroy()
    global img, title_bar, scrollbar
    btnLooks = {
        "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B"
    }
        
    title_bar = Frame(f.root, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.045, relwidth=1)
    img = [PhotoImage(file=os.path.join(f.current_dir, 'src/menu.png')), PhotoImage(file=os.path.join(f.current_dir, 'src/cog.png'))]
    # home_bar = Frame(f.root, bg="#D22B2B", width=100)
    # home_bar.pack(fill=Y)
    # home_bar.place(relx=0.9, relheight=1) # relwidth gives the fill to be 100%, rely keeps it 500*0.05 = 25 pixels from top

    menu_btn = Button(title_bar, image=img[0], **btnLooks, )
    menu_btn.pack(side=LEFT)
    logo_lbl = Label(title_bar, bg="#D22B2B", image=f.globalImg[2])
    logo_lbl.pack(side=LEFT, padx=10)

    title_label = Label(title_bar, text=u.title(), fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
    title_label.place(x=95, y=0)

    profile_btn = Button(title_bar, image=f.globalImg[4], command= lambda: profile(u, i, pc), **btnLooks)
    profile_btn.place(x=830, y=0)
    settings_btn = Button(title_bar, image=img[1], command= lambda: profile(u, i, pc), **btnLooks)
    settings_btn.place(x=880, y=0)

    global storage
    storage = ["", 0]
    def scroll_text(txt):
        global storage
        storage[0] += txt
        scrollbar.configure(text=storage[0])

        def rotate(): # Text Capacity = 187 + word length
            text = scrollbar.cget("text")
            if len(text) >= 187+len(storage[0]):
                storage[0] = ""
            scrollbar.config(text=text + "  ")
            scrollbar.after(100, rotate)

        if not storage[1]:
            storage[1] = 1; rotate()

    scrollbar = Label(f.root, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)
    scrollbar.place(x=0, y=0)
    scroll_text(f'   Welcome {u.title()}!   ')
    
    # a = Button(f.root, text= 'a', command= lambda: scroll_text('   nyooooooooom   '))
    # a.place(x=30, y=300)
    # preview()
    # profile(u, i, pc)


def showData():
    prev1 = Label(f.root, image=blob)
    prev2 = Label(f.root, image=blob)

    prev1.place(x=20, y=200)
    prev2.place(x=350, y=200)
    table_data = [
        ['O', '12', '+'],
        ['O', '7', '-'],
        ['A', '8', '+'],
        ['A', '16', '-'],
    ]

    # Create labels for table data
    for row, data_row in enumerate(table_data, start=1):
        for column, data in enumerate(data_row):
            label = Label(f.root, text=data, relief=GROOVE, width=12)
            label.grid(row=row, column=column)
            label.place(x=20+column*100, y=100+row*30)


def profile(user, hid, pin):
    f.topRoot.deiconify()
    global profBg, profCanvas
    profBg = PhotoImage(file=os.path.join(f.current_dir, 'bg/profile-page.png'))

    profCanvas = Canvas(f.topRoot, width=500, height=400)
    profCanvas.pack(fill=BOTH,)
    profCanvas.create_image(0, 0, image=profBg, anchor=NW)
    profCanvas.create_image(53, 53, image=f.globalImg[4], anchor=NW)

    fonval = ('Josefin Sans', 27)
    Title = profCanvas.create_text(60, 90, text=f'{user.title()}', font=fonval+('bold',), fill='white', anchor=NW)
    RegID = profCanvas.create_text(60, 130, text=f'Reg. ID: {hid}', font=fonval, fill='white', anchor=NW)
    Pin = profCanvas.create_text(60, 170, text=f'Pin Code: {pin}', font=fonval, fill='white', anchor=NW)

    editBtn = h.create_button(f.topRoot, 'Edit Pin Code', 60, 300, command= lambda: editProfile())
    editBtn_leave = h.create_button(f.topRoot, 'Stop Editing', 60, 300, command= lambda: ep_1())
    editBtn_save = h.create_button(f.topRoot, 'Save Pin Code', 180, 300, command= lambda: ep_2())
    
    negCoord = {"x":-100, "y":-100} # Out of plane
    editBtn_leave.place(**negCoord)
    editBtn_save.place(**negCoord)
    global pinEntry
    pinEntry = h.create_entry(f.topRoot, -200, -180, '')

    def editProfile():
        pinEntry.place(x=200, y=180)
        editBtn.place(**negCoord)
        editBtn_leave.place(x=60, y=300)
        editBtn_save.place(x=180, y=300)

    def ep_1():
        editBtn.place(x=60, y=300)
        editBtn_leave.place(**negCoord)
        editBtn_save.place(**negCoord)
        pinEntry.place(**negCoord)

    def ep_2():
        query = "update hospital set PinCode=%s where HospitalID=%s"
        pinVal = pinEntry.get()
        if h.pinVerify(pinVal) == True:
            values = (pinVal, hid)
            f.cur.execute(query, values)
            f.con.commit()
            pin = pinVal
            profCanvas.itemconfigure(Pin, text=f'Pin Code: {pin}')
        ep_1()


if __name__ == '__main__':
    # Start program
    f.init()
    f.root.mainloop()