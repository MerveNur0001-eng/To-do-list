from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import Image, ImageTk
import os

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    resized_image = image.resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(resized_image)


def forget_pass():
    def change_password():
        if user_entry.get()=='' or newpass_entry.get()=='' or confirmpass_entry.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=window)
        elif newpass_entry.get()!= confirmpass_entry.get():
            messagebox.showerror('Error', 'Password and Confirm Password are not matching', parent=window)
        else:
            try:
                con = pymysql.connect(host='localhost', user='root',password='1234', database='userdata')
                mycursor = con.cursor()
                query = 'select * from data where username=%s'
                mycursor.execute(query, (user_entry.get(),))
                row = mycursor.fetchone()
                if row is None:
                    messagebox.showerror('Error', 'Incorrect Username', parent=window)
                else:
                    query = 'update data set password=%s where username=%s'
                    mycursor.execute(query, (newpass_entry.get(), user_entry.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success', 'Password is reset, please login with new password', parent=window)
                    window.destroy()
            except Exception as e:
                messagebox.showerror('Error', f"Error due to: {str(e)}", parent=window)

    window = Toplevel()
    window.geometry('400x650')
    window.title('Change Password')

    bgFrame = Frame(window, width=400, height=650)
    bgFrame.place(x=0, y=0)
    bgPic = resize_image('Imagee/bg3.png', 400, 650)
    bgLabel = Label(bgFrame, image=bgPic)
    bgLabel.place(x=0, y=0)

    pass_image = Image.open("Imagee/pass.png")
    pass_width = 100  # Resmin genişliği
    pass_height = 100  # Resmin yüksekliği
    pass_image = pass_image.resize((pass_width, pass_height), Image.LANCZOS)
    pass_photo = ImageTk.PhotoImage(pass_image)
    pass_label = Label(window, image=pass_photo, bg='#F1F1F1')
    pass_label.place(x=170, y=450)

    heading_label = Label(window, text='RESET PASSWORD', font=('Gabriola', '25','bold'), bg='#EEEEEE', fg='#004225')
    heading_label.place(x=28, y=60)

    userLabel = Label(window, text='Username:', font=('arial', '12','bold'), bg='#EEEEEE', fg='#367E18')
    userLabel.place(x=60, y=130)

    user_entry = Entry(window, width=25, fg='#004225', font=('arial', 13, 'bold'), bd=0,bg='#EEEEEE')
    user_entry.place(x=60, y=160)

    Frame(window, width=250, height=2, bg='#4E944F').place(x=60, y=180)

    passwordLabel = Label(window, text='New Password:', font=('arial', 12, 'bold'), bg='#EEEEEE', fg='#367E18')
    passwordLabel.place(x=60, y=210)

    newpass_entry = Entry(window, width=25, fg='#004225', font=('arial', 11, 'bold'), bd=0,bg='#F1F1F1')
    newpass_entry.place(x=60, y=240)

    Frame(window, width=250, height=2, bg='#4E944F').place(x=60, y=260)

    confirmLabel = Label(window, text='Confirm Password:', font=('arial', 12, 'bold'), bg='#EEEEEE', fg='#367E18')
    confirmLabel.place(x=60, y=290)

    confirmpass_entry = Entry(window, width=25, fg='#004225', font=('arial', 11, 'bold'), bd=0,bg='#EEEEEE')
    confirmpass_entry.place(x=60, y=320)

    Frame(window, width=250, height=2, bg='#4E944F').place(x=60, y=340)

    submitButton = Button(window, text='Submit', bd=0, bg='#116530', fg='white', font=('Open Sans', 16, 'bold'), width=21, cursor='hand2', activebackground='#1E5128', activeforeground='white', command=change_password)
    submitButton.place(x=80, y=400)

    window.mainloop()


def login_user():
    if usernameEntry.get() == "" or passwordEntry.get() == "":
        messagebox.showerror('Error', 'All Fields Are Required')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata')
            mycursor = con.cursor()
            query = 'select * from data where username=%s and password=%s'
            mycursor.execute(query, (usernameEntry.get(), passwordEntry.get()))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror('Error', 'Invalid Username or Password')
            else:
                messagebox.showinfo('Welcome', 'Login is successful')
                os.system("python main.py")  # main.py dosyasını başlat
            con.close()
        except Exception as e:
            messagebox.showerror('Error', f"Error due to: {str(e)}")

def signup_page():
    login_window.destroy()
    import signup

def hide():
    openeye.config(file='Imagee/closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='Imagee/openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

login_window = Tk()
login_window.geometry('400x650')
login_window.resizable(0, 0)
login_window.title('Login Page')

image = Image.open('Imagee/bg.png')
image = image.resize((400, 650), Image.Resampling.LANCZOS)
bgImage = ImageTk.PhotoImage(image)

bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0)

heading = Label(login_window, text='USER LOGIN', font=('Gabriola', 31, 'bold'), bg='white', fg='#003285')
heading.place(x=120, y=40)

usernameEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='#003285')
usernameEntry.place(x=50, y=120)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)
frame1 = Frame(login_window, width=310, height=2, bg='#003285').place(x=50, y=141)

passwordEntry = Entry(login_window, width=25, font=('Microsoft Yahei UI Light', 11, 'bold'), bd=0, fg='#003285')
passwordEntry.place(x=50, y=180)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)
frame2 = Frame(login_window, width=310, height=2, bg='#003285').place(x=50, y=201)

openeye = PhotoImage(file='Imagee/openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
eyeButton.place(x=330, y=171)

forgetButton = Button(login_window, text='Forgot Password?', bd=0, bg='white', activebackground='white', cursor='hand2', font=('Microsoft Yahei UI Light', 10, 'bold'), fg='firebrick1', activeforeground='firebrick1', command=forget_pass)
forgetButton.place(x=240, y=207)

loginButton = Button(login_window, text='Login', font=('Open Sans', 16, 'bold'), fg='white', bg='#003285', activeforeground='white', activebackground='#003285', cursor='hand2', bd=0, width=23, command=login_user)
loginButton.place(x=50, y=280)

orLabel = Label(login_window, text='-------------------OR-------------------', font=('Open Sans', 16), fg='firebrick1', bg='white')
orLabel.place(x=50, y=340)

signupLabel = Label(login_window, text='Do not have an account?', font=('Open Sans', 9, 'bold'), fg='firebrick1', bg='white')
signupLabel.place(x=50, y=400)

newaccountButton = Button(login_window, text='Create new one', font=('Open Sans', 10, 'bold underline'), fg='blue', bg='white', activeforeground='blue', activebackground='white', cursor='hand2', bd=0, width=23, command=signup_page)
newaccountButton.place(x=190, y=400)


welcome1_image = Image.open("Imagee/welcome.png")
new_width = 275
new_height = 200
welcome1_image = welcome1_image.resize((new_width, new_height), Image.LANCZOS)
welcome1_photo = ImageTk.PhotoImage(welcome1_image)

welcome1_label = Label(login_window, image=welcome1_photo, bg='white')
welcome1_label.place(x=70, y=420)


login_window.mainloop()
