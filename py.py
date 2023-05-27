from tkinter import *
from tkinter import messagebox
import mysql.connector as sql

root = Tk()

def main(): # Login Screen
    global root, signinLabel, unLbl, pwLbl, unField, pwField, loginBtn
    root.title('Blood bank mng')
    root.iconphoto(False, PhotoImage(file='./plus.png'))
    root.geometry('400x300')
    root.resizable(False, False)
    
    signinLabel = Label(root, text='LOG IN', font=('Bahnschrift', 20, 'bold'))

    signinLabel.place(y=10, relx=0.4)

    unLbl = Label(root, text='Username', font=('Cascadia Code', 10, 'italic'))
    unLbl.place(x=50, y=100)

    pwLbl = Label(root, text='Password', font=('Cascadia Code', 10, 'italic'))
    pwLbl.place(x=50, y=140)

    unField = Entry(root)
    unField.place(x = 150, y=100)

    pwField = Entry(root, show='*')
    pwField.place(x = 150, y=140)

    loginBtn = Button(root, text='Submit', relief=RIDGE, padx=40, command= lambda: unpwCheck(unField.get(), pwField.get()))
    loginBtn.place(x=150, y=200)


# Function that verifies the login Details
def unpwCheck(un, pw): # username, password
    # To access current login screen widgets
    widgets = [signinLabel, unLbl, pwLbl, unField, pwField, loginBtn]

    # Check Login Details
    if (un=='' or pw=='') or (un != 'a' or pw !='1'):
        return messagebox.showerror('Error', 'Invalid Login details')
    elif un == 'a' and pw == '1':
        for i in widgets:
            i.destroy() # Remove widgets as we're going out of login screen
    
        status = detailsWindow(pw) # Here we call the main interface. If any error occurs during startup, the following if statements will handle it

        if status == 'error': # if there is a error while running detailsWindow()
            messagebox.showerror('Error', 'Please login again')
            main() # Return to login screen


# Function that handles the main window after login
def detailsWindow(passw) -> None:
    con = sql.connect(host='localhost', user='root', password='root')

    if con.is_connected():
        root.geometry('700x500') # Resize window
        cur = con.cursor()
        cur.execute('use school')
        con.commit()

        text_1 = Label(root, text='| INITIALIZE', font=('Franklin Gothic', 20))
        text_1.place(x=40, y=15)

        OutputLbl = Label(root, text='Output', font=('Bahnscrift', 12), width=66, pady=20, bg='white', highlightbackground="black", highlightthickness=1)
        OutputLbl.place(x=40, y=350)
      
        # A dictionary containing all color, border font stuff of buttons
        buttonLooks = {
             'relief':FLAT, 'padx':20, 'font':('Century Gothic', 15),
             'bg':'#808080', 'fg':'white', 'activebackground':'#808083', 'activeforeground':'white'
        }

        intializeButton = Button(root, command= lambda: checkTable(), text='Check Tables', **buttonLooks)
        intializeButton.place(x=40, y=65)

        createButton = Button(root, command= lambda: createTable(), text='Create Tables', **buttonLooks)
        createButton.place(x=240, y=65)

        text_2 = Label(root, text='| COMMANDS', font=('Franklin Gothic', 20))
        text_2.place(x=40, y=120)

        QueryButton = Button(root, command= lambda: Query(), text='Run A Query',  **buttonLooks)
        QueryButton.place(x=40, y=170)


        # Function to check if the tables Donor and Reciever already exist
        def checkTable():
            checkQuery = "SHOW TABLES FROM school LIKE %s"
            tables = [[False, 'Donor'], [False, 'Reciever']] # Storing the result here
            cursor = con.cursor()
            OutputLbl['text'] = ''

            for i in tables: # check both tables
                cursor.execute(checkQuery, (i[1],))
                row = cursor.fetchone()
                if row: # i[1] gives the table name (see 'tables' list)
                    OutputLbl['text'] += f'   {i[1]} table was found     '
                else:
                    OutputLbl['text'] += f'   {i[1]} table was not found     '

        # Function to create Donor and Reciever tabke
        def createTable():
            cursor = con.cursor()
            createQuery_1 = "create table Donor (DonorID int(3) primary key not null unique, DonorName char(20), DonorAge int(2), DonorAddress char(40), BloodType char(3))"
            createQuery_2 = "create table Reciever (RecieverID int(3) primary key not null unique, DonorID int, foreign key (DonorID) references Donor(DonorID), RecieverName char(20), RecieverAddress char(40), RecieverAge int(2), BloodGroup char(3), Date date)"

            cursor.execute(createQuery_1)
            cursor.execute(createQuery_2)
            
            OutputLbl['text'] = 'Created both tables.'

    else:
        return 'error'

if __name__ == '__main__':
    main()
    root.mainloop()