from __main__ import app
from tkinter import Entry, Button, Label

def pinVerify(pin) -> True:
    if not pin.isdigit() or pin[0] == '0' or len(pin) != 6:
        return False
    invalid = [29, 35, 54, 55, 65, 66]
    if pin[:2] in invalid:
        return False
    return status


def switchS_L():
    from authenticate import Login

    for widget in app.signup_var:
        widget.destroy()
    data = Login()
    app.login_var = [data.login_canvas, data.signin_button, data.submit_button, data.user_name, data.user_pass]

def switchL_S():
    from authenticate import SignUp

    for widget in app.login_var:
        widget.destroy()
    data = SignUp()
    app.signup_var = [data.signup_canvas, data.Contact, data.hospName, data.PassWord, data.pinCode, data.submitBtn, data.switchBtn]


def create_entry(control, varx, vary, text, *args, **kwargs):
    entry = Entry(control, args,  bd=16, relief="flat", **kwargs)
    entry.place(x=varx, y=vary)
    entry.insert(0, text)
    return entry

def create_button(control, text, varx, vary, **kwargs):
    abg = '#6CB4EE' if not kwargs.get('activebackground') else kwargs.get('activebackground')
    bg = '#6CB4EE' if not kwargs.get('background') else kwargs.get('background')
    for i in ['activebackground', 'background']:
        kwargs.pop(i, None)
    button = Button(control, text=text, background=bg, relief="flat", padx=40, pady=10, activebackground=abg, **kwargs)
    button.pack()
    button.place(x=varx, y=vary)
    return button