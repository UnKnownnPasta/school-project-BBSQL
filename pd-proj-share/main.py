from tkinter import messagebox
from tkinter import *
import mysql.connector as sql
from re import findall
import ctypes, os
globpassw = 'root'
current_dir = os.path.dirname(__file__)

def create_entry(control, varx, vary, text, *args, **kwargs):
    entry = Entry(control, args,  bd=16, relief=FLAT, **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry

def create_button(control, text, varx, vary, **kwargs):
    button = Button(control, text=text, background='#6CB4EE', relief=FLAT, padx=20, pady=10, activebackground='#6CB4EE', **kwargs)
    button.place(x=varx, y=vary)
    return button


def init():
    global arrow, root, blob, topRoot, globalImg
    root = Tk()

    # Defined here since it wouldn't load otherwise
    bg_img_1 = PhotoImage(file=os.path.join(current_dir, 'bg/bg-blur-v2.png'))
    bg_img_2 = PhotoImage(file=os.path.join(current_dir, 'bg/bg-unblur.png'))
    #logo_img = Image.open('logo-v2-sh.png')
    logo_80 = PhotoImage(file=os.path.join(current_dir, 'src/logo-80.png')) #ImageTk.PhotoImage(logo_img.resize([int(0.13 * s) for s in logo_img.size]))
    logo_120 = PhotoImage(file=os.path.join(current_dir, 'src/logo-120.png')) #ImageTk.PhotoImage(logo_img.resize([int(0.25 * s) for s in logo_img.size]))
    arrow = PhotoImage(file=os.path.join(current_dir, 'src/arrow.png'))
    blob = PhotoImage(file=os.path.join(current_dir, 'src/box.png'))
    profImg = PhotoImage(file=os.path.join(current_dir, 'src/profile.png'))

    # Makes the images accessible globally -- as globalImg[n] n being item index
    globalImg = [bg_img_1, bg_img_2, logo_80, logo_120, profImg]

    ctypes.windll.gdi32.AddFontResourceA(os.path.join(current_dir, 'JosefinSans-Regular.ttf'))

    topRoot = Toplevel(root)
    topRoot.withdraw()
    topRoot.title('Profile')
    topRoot.geometry('500x400+270+200')
    topRoot.iconphoto(False, PhotoImage(file=os.path.join(current_dir, 'src/logo-nosh.png')))

    topRoot.protocol('WM_DELETE_WINDOW', DEL_EVENT)

    global con, cur
    try:
        con = sql.connect(host='localhost', user='root', password=globpassw)
        cur = con.cursor()
    except:
        messagebox.showerror('Error', 'Failed to connect to SQL')
    cur.execute('show databases;')
    res = any(db[0] == 'bloodbank' for db in cur.fetchall())
    if res == False:
        cur.execute('create database bloodbank')
    cur.execute('use bloodbank')

    try:
        cur.execute('create table if not exists Hospital (HospitalID int(4) auto_increment primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode char(6) not null)')   #.zfill
        cur.execute('create table if not exists BloodBank (BloodType char(2), Units int not null, RhFactor char(8))')
        cur.execute('create table if not exists Donor (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), foreign key (HospitalID) references Hospital(HospitalID))')
        cur.execute('create table if not exists Recipient (Name varchar(40), Age int(3), DateOfTransfer date, HospitalID int(4), BloodType char(2), foreign key (HospitalID) references Hospital(HospitalID))')
    except:
        messagebox.showerror('Error', 'Something went wrong while initializing tables.')

    con.commit()
    root.title('Blood Bank Mng')
    root.iconphoto(False, PhotoImage(file=os.path.join(current_dir, 'src/logo-nosh.png')))
    root.resizable(False, False)
    root.geometry(f"{940}x{500}+{(root.winfo_screenwidth() - 940) // 2}+{(root.winfo_screenheight() - 500) // 2}")
    Login()
    # SignUp()


def SignUp():
    global hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu, PassWord
    canvasSu = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasSu.create_image(0, 0, image=globalImg[0], anchor='nw')
    canvasSu.pack(side = "top", fill = "both", expand = True)

    sText = canvasSu.create_text(240, 180, text='Enter Details to Create A Account..', anchor=NW, font=('Josefin Sans', 17), fill='white')
    altText = canvasSu.create_text(320, 48, text='BLOOD BANK MANAGEMENT', anchor=NW, font=('Josefin Sans', 20, 'bold'), fill='white')
    canvasSu.create_image(230, 30, image=globalImg[3], anchor=NW)

    def setText(entry, defText):
        entry.delete(0, END) if entry.get().strip() == defText else None
        
    def restoreText(entry, defText):
        entry.insert(0, defText) if entry.get().strip() == "" else None

    hospName = create_entry(root, 240, 250, 'Hospital Name', width=70)
    hospName.bind('<FocusIn>', lambda event: setText(hospName, 'Hospital Name'))
    hospName.bind('<FocusOut>', lambda event: restoreText(hospName, 'Hospital Name'))

    pinCode = create_entry(root, 240, 310, 'Pin Code', width=22)
    pinCode.bind('<FocusIn>', lambda event: setText(pinCode, 'Pin Code'))
    pinCode.bind('<FocusOut>', lambda event: restoreText(pinCode, 'Pin Code'))

    Contact = create_entry(root, 420, 310, 'Contact (Phone No./email)', width=40)
    Contact.bind('<FocusIn>', lambda event: setText(Contact, 'Contact (Phone No./email)'))
    Contact.bind('<FocusOut>', lambda event: restoreText(Contact, 'Contact (Phone No./email)'))
    
    PassWord = create_entry(root, 240, 370, 'Enter a Strong Password', width=70)
    PassWord.bind('<FocusIn>', lambda event: setText(PassWord, 'Enter a Strong Password'))
    PassWord.bind('<FocusOut>', lambda event: restoreText(PassWord, 'Enter a Strong Password'))

    swchBtnSu = Button(root, command=switchS_L, image=arrow, relief=FLAT, bd=0, highlightthickness=0, activebackground='#ad1e1e')
    submBtnSu = create_button(root, 'Submit', 425, 430, command= lambda: SignSubm(pinCode.get(), Contact.get(), hospName.get(), PassWord.get()))

    swchBtnSu.place(x=770, y=30)


def Login():
    global canvasLi, userName, userPass, submBtnLi, signBtnLi
    canvasLi = Canvas(root, width='940', height='500', highlightthickness=0)
    canvasLi.create_image(0, 0, image=globalImg[1], anchor='nw')
    canvasLi.pack(side = "top", fill = "both", expand = True)

    titleLabel1 = canvasLi.create_text(355, 58, text='ADMIN', anchor='nw', font=('Franklin Gothic', 25, 'bold'), fill='white')
    titleLabel2 = canvasLi.create_text(470, 46, text='Login', anchor='nw', font=('Josefin Sans', 25), fill='white')

    sText = canvasLi.create_text(240, 180, text='Sign In', anchor='nw', font=('Franklin Gothic', 16, 'bold'), fill='white')
    altText = canvasLi.create_text(240, 200, text='Fill in details to gain access', anchor='nw', font=('Josefin Sans', 14), fill='white')

    def setText(entry, defText):
        entry.delete(0, END) if entry.get().strip() == defText else None

    def restoreText(entry, defText):
        entry.insert(0, defText) if entry.get().strip() == "" else None

    userName = create_entry(root, 240, 260, 'User Name', width=70)
    userName.bind('<FocusIn>', lambda event: setText(userName, 'User Name'))
    userName.bind('<FocusOut>', lambda event: restoreText(userName, 'User Name'))

    userPass = create_entry(root, 240, 320, 'Password', width=70)
    userPass.bind('<FocusIn>', lambda event: setText(userPass, 'Password'))
    userPass.bind('<FocusOut>', lambda event: restoreText(userPass, 'Password'))
    userPass.bind('<Return>',  lambda event: loginSubm(userName.get(), userPass.get()))

    submBtnLi = create_button(root, 'Login', 353, 380, command= lambda: loginSubm(userName.get(), userPass.get()))
    signBtnLi = create_button(root, 'Sign Up', 485, 380, command=switchL_S)
   
    orLbl = canvasLi.create_text(440, 385, text='..OR..', anchor='nw', font=('Josefin Sans', 14), fill='white')


def switchS_L(): # Signup to Login
    w = [hospName, pinCode, Contact, submBtnSu, canvasSu, swchBtnSu, PassWord]
    for i in w:
        i.destroy()
    Login()
def switchL_S(): # Login to Signup
    w = [canvasLi, userName, userPass, submBtnLi, signBtnLi]
    for i in w:
        i.destroy()
    SignUp()


def SignSubm(postCode, contact, hospName, passwrd):
    verf = pinVerify(postCode)
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
        cur.execute(query, vals)
        con.commit()
    except:
        messagebox.showerror('Error', 'Failed to signup. Try again.')
        return

    messagebox.showinfo('Success', 'Account created successfully! Login to it here')
    switchS_L()


def loginSubm(un, pw):
    for i in [un, pw]:
        if i == 'User Name' or i == 'Password' or len(i) == '' or i == ' ':
            messagebox.showerror('Error', 'Invalid login details')
            return
    query = "select * from hospital where HospitalName=%s and Password=%s"
    values = (un, pw)
    cur.execute(query, values)
    res = cur.fetchone()
    if res == None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return
    cur.execute('select HospitalID, PinCode from Hospital where HospitalName=%s', (un,))
    hId, pc = [i for i in cur.fetchall()[0]]
    program(un, pw, hId, pc)


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
        m = findall(regx, pin)
        if len(m) != 0:
            status = True
    return status


def program(u, p, i, pc):
    ww = [canvasLi, userName, userPass, submBtnLi, signBtnLi]
    for x in ww:
        x.destroy()
    global img, title_bar, scrollbar
    btnLooks = {
        "bg":"#D22B2B", "relief":"flat", "activebackground":"#D22B2B"
    }
        
    title_bar = Frame(root, bg="#D22B2B", height=30)
    title_bar.pack(fill=X)
    title_bar.place(rely=0.045, relwidth=1)
    img = [PhotoImage(file=os.path.join(current_dir, 'src/menu.png')), PhotoImage(file=os.path.join(current_dir, 'src/cog.png'))]
    # home_bar = Frame(root, bg="#D22B2B", width=100)
    # home_bar.pack(fill=Y)
    # home_bar.place(relx=0.9, relheight=1) # relwidth gives the fill to be 100%, rely keeps it 500*0.05 = 25 pixels from top

    menu_btn = Button(title_bar, image=img[0], **btnLooks, )
    menu_btn.pack(side=LEFT)
    logo_lbl = Label(title_bar, bg="#D22B2B", image=globalImg[2])
    logo_lbl.pack(side=LEFT, padx=10)

    title_label = Label(title_bar, text=u.title(), fg="white", bg="#D22B2B", font=('Josefin Sans', 17), pady=0)
    title_label.place(x=95, y=0)

    profile_btn = Button(title_bar, image=globalImg[4], command= lambda: profile(u, i, pc), **btnLooks)
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

    scrollbar = Label(root, font=("Arial", 12), anchor=NE, bg="black", fg="white", width=104)
    scrollbar.place(x=0, y=0)
    scroll_text(f'   Welcome {u.title()}!   ')
    
    # a = Button(root, text= 'a', command= lambda: scroll_text('   nyooooooooom   '))
    # a.place(x=30, y=300)
    # preview()
    # profile(u, i, pc)



def showData():
    prev1 = Label(root, image=blob)
    prev2 = Label(root, image=blob)

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
            label = Label(root, text=data, relief=GROOVE, width=12)
            label.grid(row=row, column=column)
            label.place(x=20+column*100, y=100+row*30)


def DEL_EVENT(): 
    topRoot.withdraw()
    profCanvas.destroy()

def profile(user, hid, pin):
    topRoot.deiconify()
    global profBg, profCanvas
    profBg = PhotoImage(file=os.path.join(current_dir, 'bg/profile-page.png'))

    profCanvas = Canvas(topRoot, width=500, height=400)
    profCanvas.pack(fill=BOTH)
    profCanvas.create_image(0, 0, image=profBg, anchor=NW)
    profCanvas.create_image(53, 53, image=globalImg[4], anchor=NW)

    fonval = ('Josefin Sans', 27)
    profCanvas.create_text(60, 150, text=f'Hospital: {user}', font=fonval, fill='white', anchor=NW)
    profCanvas.create_text(60, 200, text=f'Hospital ID: {hid}', font=fonval, fill='white', anchor=NW)
    profCanvas.create_text(60, 250, text=f'Pin Code: {pin}', font=fonval, fill='white', anchor=NW)

if __name__ == '__main__':
    # Start program
    init()
    # program('lions', 'root', '123', '1235')
    root.mainloop()