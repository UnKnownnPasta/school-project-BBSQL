from tkinter import *
from tkinter import messagebox
import mysql.connector as sql
import os, ctypes

#   SQL Password
#       Change this to your MySQL Password (host system)
MYSQL_PASSWORD = 'root'
current_dir = os.path.dirname(__file__)

def pathLoad(path):
    return os.path.join(current_dir, path)

class BloodBankApp:

    # __init__ starts the function - it's like calling a function with the stuff defined below, but automatic
    # self allows the variables defined with it, to be called ANYWHERE
    def __init__(self):
        self.root = Tk()
        self.root.title('Blood Bank System')
        self.root.title('Blood Bank Mng')
        self.root.iconphoto(False, PhotoImage(file=pathLoad('src/logo-nosh.png')))
        self.root.resizable(False, False)
        self.root.geometry(f"{940}x{500}+{(self.root.winfo_screenwidth() - 940) // 2}+{(self.root.winfo_screenheight() - 500) // 2}")

        gdi32 = ctypes.WinDLL('gdi32')          # Install necessary font(s)
        gdi32.AddFontResourceW.argtypes = (ctypes.c_wchar_p,)
        gdi32.AddFontResourceW(pathLoad('src/JosefinSans-Regular.ttf'))

        self.connection = None
        self.cursor = None

        self.login_var = None  # Stores login page widgets
        self.signup_var = None # Stores signup page widgets

        self.initializeDatabase()
        self.initializeImages()

    def initializeDatabase(self):
        try:
            self.connection = sql.connect(host='localhost', user='root', password=MYSQL_PASSWORD)
            self.cursor = self.connection.cursor()
        except:
            messagebox.showerror('Error', 'Failed to connect to SQL')
        else: # Runs if there is no error
            self.cursor.execute('show databases;')

            # any() return True if there is atleast 1 result that is returned by .fetchall()
            res = any(db[0] == 'bloodbank' for db in self.cursor.fetchall())
            if res == False:
                self.cursor.execute('create database bloodbank')
            self.cursor.execute('use bloodbank')

        try:
            self.cursor.execute('create table if not exists Hospital (HospitalID int(4) auto_increment primary key, HospitalName varchar(100) unique, Password varchar(20), Contact varchar(100), PinCode char(6) not null)')   #.zfill
            self.cursor.execute('create table if not exists BloodBank (BloodType char(2), Units int not null, RhFactor char(8))')
            self.cursor.execute('create table if not exists Donor (Name varchar(40), Age int(3), Gender char(20), BloodGroup char(2), HospitalID int(4), foreign key (HospitalID) references Hospital(HospitalID))')
            self.cursor.execute('create table if not exists Recipient (Name varchar(40), Age int(3), DateOfTransfer date, HospitalID int(4), BloodType char(2), foreign key (HospitalID) references Hospital(HospitalID))')
        except:
            messagebox.showerror('Error', 'Something went wrong while initializing tables.')
        finally:
            self.connection.commit()

    def initializeImages(self):
        global arrow, blob, globalImages
        # Defining a bunch of images to preload so that it loads instantly
        
        self.arrow = PhotoImage(file=pathLoad('src/arrow.png'))
        self.blob = PhotoImage(file=pathLoad('src/box.png'))
        
        bg_image_1 = PhotoImage(file=pathLoad('bg/bg-blur-v2.png'))
        bg_image_2 = PhotoImage(file=pathLoad('bg/bg-unblur.png'))    # If PIL was there, we can save file space by resizing images instead of loading new ones
        logo_80 = PhotoImage(file=pathLoad('src/logo-80.png'))        # ImageTk.PhotoImage(logo_img.resize([int(0.13 * s) for s in logo_img.size]))
        logo_120 = PhotoImage(file=pathLoad('src/logo-120.png'))      # ImageTk.PhotoImage(logo_img.resize([int(0.25 * s) for s in logo_img.size]))
        profileImage = PhotoImage(file=pathLoad('src/profile.png'))

        # Makes the images accessible globally -- called as globalImg[n], n being item index
        globalImages = [bg_image_1, bg_image_2, logo_80, logo_120, profileImage]
    
    def auth(self):
        from authenticate import Login
        login = Login() # Show login Page

        # Initialize a variable with all login page widgets for future usage
        self.login_var = [login.login_canvas, login.signin_button, login.submit_button, login.user_name, login.user_pass]


if __name__ == "__main__":
    app = BloodBankApp()

    # Run login page
    app.auth()
    app.root.mainloop()