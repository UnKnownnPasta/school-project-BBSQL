from __main__ import app, globalImages
from tkinter import *
from tkinter import messagebox
from helper import *

root, con, cur = app.root, app.connection, app.cursor

class SelectAuthType:
    def __init__(self):
        self.auth_canvas = Canvas(
            root, width='940', height='500', highlightthickness=0
        )
        self.auth_canvas.create_image(0, 0, image=globalImages[1], anchor='nw')
        self.auth_canvas.pack(side = "top", fill = "both", expand = True)

        standard_look = {"anchor": "nw", "fill":"white"}
        self.login_choice = create_button(root, 'Login to Account', 100, 100, comman=app.doLogin)
        self.signup_choice = create_button(root, 'Create A Account', 100, 100, comman=app.doLogin)


class Login:
    def __init__(self):
        self.login_canvas = Canvas(
            root, width='940', height='500', highlightthickness=0
        )
        self.login_canvas.create_image(0, 0, image=globalImages[1], anchor='nw')
        self.login_canvas.pack(side = "top", fill = "both", expand = True)

        standard_look = {"anchor": "nw", "fill":"white"}
        titleLabel1 = self.login_canvas.create_text(
            355, 58, text='ADMIN', font=('Franklin Gothic', 25, 'bold'), **standard_look
        )
        titleLabel2 = self.login_canvas.create_text(
            470, 46, text='Login', font=('Josefin Sans', 25), **standard_look
        )

        topText = self.login_canvas.create_text(
            240, 180, text='Sign In', font=('Franklin Gothic', 16, 'bold'), **standard_look
        )
        altText = self.login_canvas.create_text(
            240, 200, text='Fill in details to gain access', font=('Josefin Sans', 14), **standard_look
        )

        def setText(entry, defaultText):
            entry.delete(0, END) if entry.get().strip() == defaultText else None

        def restoreText(entry, defaultText):
            entry.insert(0, defaultText) if entry.get().strip() == "" else None

        self.user_name = create_entry(root, 240, 260, 'User Name', width=70)
        self.user_name.bind('<FocusIn>', 
            lambda event: setText(user_name, 'User Name')
            )
        self.user_name.bind('<FocusOut>', 
            lambda event: restoreText(user_name, 'User Name')
        )

        self.user_pass = create_entry(root, 240, 320, 'Password', width=70)
        self.user_pass.bind('<FocusIn>', 
            lambda event: setText(user_pass, 'self.Password')
        )
        self.user_pass.bind('<FocusOut>', 
            lambda event: restoreText(user_pass, 'self.Password')
        )
        self.user_pass.bind('<Return>',  
            lambda event: m.loginSubm(user_name.get(), user_pass.get())
        )

        self.submit_button = create_button(
            root, 'Login', 320, 380, command= lambda: m.loginSubm(user_name.get(), user_pass.get())
        )
        self.signin_button = create_button(root, 'Sign Up', 460, 380, command=switchL_S)


class SignUp:
    def __init__(self):
        self.signup_canvas  = Canvas(
            root, width='940', height='500', highlightthickness=0
        )
        self.signup_canvas .create_image(0, 0, image=globalImages[0], anchor='nw')
        self.signup_canvas .pack(side = "top", fill = "both", expand = True)

        titleText = self.signup_canvas .create_text(
            240, 180, text='Enter Details to Create A Account..', anchor=NW, font=('Josefin Sans', 17), fill='white'
        )
        altText = self.signup_canvas .create_text(
            320, 48, text='BLOOD BANK MANAGEMENT', anchor=NW, font=('Josefin Sans', 20, 'bold'), fill='white'
        )
        self.signup_canvas .create_image(230, 30, image=globalImages[3], anchor=NW)

        def setText(entry, defText):
            entry.delete(0, END) if entry.get().strip() == defText else None
            
        def restoreText(entry, defText):
            entry.insert(0, defText) if entry.get().strip() == "" else None

        self.hospName = create_entry(root, 240, 250, 'Hospital Name', width=70)
        self.hospName.bind('<FocusIn>', lambda event: setText(self.hospName, 'Hospital Name'))
        self.hospName.bind('<FocusOut>', lambda event: restoreText(self.hospName, 'Hospital Name'))

        self.pinCode = create_entry(root, 240, 310, 'Pin Code', width=22)
        self.pinCode.bind('<FocusIn>', lambda event: setText(self.pinCode, 'Pin Code'))
        self.pinCode.bind('<FocusOut>', lambda event: restoreText(self.pinCode, 'Pin Code'))

        self.Contact = create_entry(
            root, 420, 310, 'Contact (Phone No./email)', width=40
        )
        self.Contact.bind('<FocusIn>', 
            lambda event: setText(self.Contact, 'self.Contact (Phone No./email)')
        )
        self.Contact.bind('<FocusOut>',
            lambda event: restoreText(self.Contact, 'self.Contact (Phone No./email)')
        )
        
        self.PassWord = create_entry(root, 240, 370, 'Enter a Strong Password', width=70)
        self.PassWord.bind('<FocusIn>', 
            lambda event: setText(self.PassWord, 'Enter a Strong self.Password')
        )
        self.PassWord.bind('<FocusOut>', 
            lambda event: restoreText(self.PassWord, 'Enter a Strong self.Password')
        )

        self.switchBtn = Button(root, command=switchS_L, image=globalImages[5], relief=FLAT, bd=0, highlightthickness=0, activebackground='#ad1e1e')
        self.submitBtn = create_button(root, 'Submit', 390, 430, command= lambda: m.SignSubm(self.pinCode.get(), self.Contact.get(), self.hospName.get(), self.PassWord.get()))

        self.switchBtn.place(x=770, y=30)