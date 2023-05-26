from tkinter import *
from tkinter import messagebox
import mysql.connector as msor

root = Tk()

def unpwCheck(un, pw):
    # To access current login screen widgets
    widgets = [signinLabel, unLbl, pwLbl, unField, pwField, loginBtn]
    status = None

    # Check Login Details
    if (un=='' or pw=='') or (un != 'a' or pw !='1'):
        return messagebox.showerror('Error', 'Invalid Login details')
    elif un == 'a' and pw == '1':
        for i in widgets:
            i.destroy() # Remove widgets as we're going out of login screen
    
        status = detailsWindow(pw) # Here we call the main interface. If any error occurs during startup, the following if statements will handle it

        if status == 'fail-initial': # If SQL itself had a error in doing .connect()
            messagebox.showerror('SQL Error', 'Could not initialize SQL Connection, login again.')
            main() # Return to login screen
        if status == 'fail-connect': # If there is a mistake in login details
            messagebox.showerror('SQL Error', 'Could not connect to database, login again.')
            main() # Return to login screen

def detailsWindow(passw):
    try:
        sqlMain = msor.connect(host='localhost', user='root', password='root', database='school')
    except msor.Error:
        return 'fail-initial' 

    if sqlMain.is_connected() == False:
        return 'fail-connect'
        
    root.geometry('700x500') # Resize window
    cur = sqlMain.cursor()

    intializeButton = Button()
    # Function to check if the tables Donor and Reciever already exist
    def checkTable():
        checkQuery = "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '%s') AS table_exists;"
        exists = [[False, 'Donor'], [False, 'Reciever']] # Storing the result here

        cur.execute(checkQuery, ('Donor',))
        exists[0][0] = bool(cur.fetchone()[0])
        cur.execute(checkQuery, ('Reciever',))
        exists[1][0] = bool(cur.fetchone()[0])

        return exists


    headingLabel = Label(root, text='')
    
        
    
def main():
    global root, signinLabel, unLbl, pwLbl, unField, pwField, loginBtn
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='./plus.png'))
    root.geometry('400x300')
    root.resizable(False, False)
    
    signinLabel = Label(root, text='LOG IN', font=('Bahnschrift', 20, 'bold'))
    signinLabel.pack()
    signinLabel.place(y=10, relx=0.4)

    unLbl = Label(root, text='Username', font=('Cascadia Code', 10, 'italic'))
    unLbl.pack()
    unLbl.place(x=50, y=100)

    pwLbl = Label(root, text='Password', font=('Cascadia Code', 10, 'italic'))
    pwLbl.pack()
    pwLbl.place(x=50, y=140)

    unField = Entry(root)
    unField.pack()
    unField.place(x = 150, y=100)

    pwField = Entry(root, show='*')
    pwField.pack()
    pwField.place(x = 150, y=140)

    loginBtn = Button(root, text='Submit', relief=RIDGE, padx=40, command= lambda: unpwCheck(unField.get(), pwField.get()))
    loginBtn.pack()
    loginBtn.place(x=140, y=200)

if __name__ == '__main__':
    main()
    root.mainloop()