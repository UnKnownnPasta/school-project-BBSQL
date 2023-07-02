from __main__ import app
from tkinter import Entry, Button, Label, messagebox

def pinVerify(pin) -> True:
    if not pin.isdigit() or pin[0] == '0' or len(pin) != 6:
        return False
    invalid = [29, 35, 54, 55, 65, 66]
    if pin[:2] in invalid:
        return False
    return status


# -------------------------------- Switch between Login and Signup (Admin) --------------------------------

def switchS_L():
    from authenticate import AdminLogin

    for widget in app.signup_var:
        widget.destroy()
    data = AdminLogin()
    app.login_var = list(data.__dict__.values())

def switchL_S():
    from authenticate import AdminSignUp

    for widget in app.login_var:
        widget.destroy()
    data = AdminSignUp()
    app.signup_var = list(data.__dict__.values())


# ------------------ Custom functions to create entries/buttons to reduce boilerplate code ------------------

def create_entry(control, varx, vary, text, *args, **kwargs):
    entry = Entry(control, args,  bd=16, relief="flat", **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry

def create_button(control, text, varx, vary, **kwargs):
    if 'activebackground' not in kwargs: kwargs['activebackground'] = '#FF5733'
    if 'background' not in kwargs: kwargs['background'] = '#EE4B2B'      # Add bg color if it's not mentioned

    button = Button(control, text=text, relief="flat", padx=35, pady=10, font=('Century Gothic', 11), bd=0, **kwargs)
    button.pack()
    button.place(x=varx, y=vary)
    return button


# ---------------------------------- Handling submitting From Login/Signup ----------------------------------

# for signup
def AdminSubmit(postCode, contact, hospName, passwrd):
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
        
    passwrd = passwrd.replace(' ', '_')
    try:
        vals = (hospName, passwrd, contact, postCode)
        query = "insert into Hospital (HospitalName, Password, Contact, PinCode) values (%s, %s, %s, %s)"

        f.cur.execute(query, vals)
        f.con.commit()
    except:
        messagebox.showerror('Error', 'Failed to signup. Try again.')
    else:
        messagebox.showinfo('Success', 'Account created successfully! Login to it here')
        f.switchS_L()


# for login
def AdminAccess(un, pw):
    for i in [un, pw]:
        accessFilter = ['User Name', 'Password', ' ']

        if i in accessFilter or len(i) == '' or isinstance(i, int):
            messagebox.showerror('Error', 'Invalid login details')
            return

    query = "select * from hospital where HospitalName=%s and Password=%s"
    values = (un, pw.replace(' ', '_'))

    f.cur.execute(query, values)
    res = f.cur.fetchone()

    if res == None:
        messagebox.showerror('Error', 'Login details are not correct.')
        return

    f.cur.execute('select HospitalID, PinCode from Hospital where HospitalName=%s', (un,))
    hId, pc = [i for i in f.cur.fetchall()[0]]
    program(un, pw, hId, pc)