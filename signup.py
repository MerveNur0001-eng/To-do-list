import mysql.connector
from mysql.connector import Error
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

def connect_database():
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error', 'Passwords Dismatch')
    elif check.get() == 0:
        messagebox.showerror('Error', 'Please accept the Terms & Conditions')
    else:
        try:
            con = mysql.connector.connect(
                host='localhost',
                user='root',
                password='1234',
                database='userdata'
            )
            mycursor = con.cursor()
            query = 'CREATE DATABASE IF NOT EXISTS userdata'
            mycursor.execute(query)
            query = 'USE userdata'
            mycursor.execute(query)
            query = '''
                CREATE TABLE IF NOT EXISTS data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(50),
                    username VARCHAR(100),
                    password VARCHAR(20)
                )
                '''
            mycursor.execute(query)
            query = 'SELECT * FROM data WHERE username=%s'
            mycursor.execute(query, (usernameEntry.get(),))

            row = mycursor.fetchone()
            if row is not None:
                messagebox.showerror('Error', 'Username Already exists')
            else:
                query = 'INSERT INTO data (email, username, password) VALUES (%s, %s, %s)'
                mycursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'Registration successful')
                clear()
                signup_window.destroy()
                import signin
        except Error as e:
            messagebox.showerror('Error', f'Error creating database or table\n{e}')
            return
        query = 'SELECT * FROM data WHERE username=%s'
        mycursor.execute(query, (usernameEntry.get(),))

        row = mycursor.fetchone()
        if row is not None:
            messagebox.showerror('Error', 'Username Already exists')
        else:
            query = 'INSERT INTO data (email, username, password) VALUES (%s, %s, %s)'
            mycursor.execute(query, (emailEntry.get(), usernameEntry.get(), passwordEntry.get()))
            con.commit()
            con.close()
            messagebox.showinfo('Success', 'Registration successful')
            clear()
            signup_window.destroy()
            import signin

def login_page():
    signup_window.destroy()
    import signin

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.convert('RGB')
    resized_image = image.resize((width, height), Image.LANCZOS)
    resized_image.save('Imagee/resized_bg.jpg', 'JPEG', quality=85)
    return ImageTk.PhotoImage(resized_image)


def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)

def forget_pass():
    def change_password():
        if user_entry.get() == '' or newpass_entry.get() == '' or confirmpass_entry.get() == '':
            messagebox.showerror('Error', 'All Fields Are Required', parent=window)
        elif newpass_entry.get() != confirmpass_entry.get():
            messagebox.showerror('Error', 'Password and Confirm Password are not matching', parent=window)
        else:
            try:
                con = mysql.connector.connect(host='localhost', user='root', password='1234', database='userdata')
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
    bgPic = resize_image('Imagee/bg.png', 400, 650)
    bglabel = Label(window, image=bgPic)
    bglabel.grid()

    heading_label = Label(window, text='RESET PASSWORD', font=('arial', '18', 'bold'), bg='white', fg='magenta2')
    heading_label.place(x=100, y=60)

    userLabel = Label(window, text='Username:', font=('arial', '12', 'bold'), bg='white', fg='orchid1')
    userLabel.place(x=60, y=130)

    user_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    user_entry.place(x=60, y=160)

    Frame(window, width=250, height=2, bg='orchid1').place(x=60, y=180)

    passwordLabel = Label(window, text='New Password', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    passwordLabel.place(x=60, y=210)

    newpass_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    newpass_entry.place(x=60, y=240)

    Frame(window, width=250, height=2, bg='orchid1').place(x=60, y=260)

    confirmLabel = Label(window, text='Confirm Password', font=('arial', 12, 'bold'), bg='white', fg='orchid1')
    confirmLabel.place(x=60, y=290)

    confirmpass_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    confirmpass_entry.place(x=60, y=320)

    Frame(window, width=250, height=2, bg='orchid1').place(x=60, y=340)

    submitButton = Button(window, text='Submit', bd=0, bg='magenta2', fg='white', font=('Open Sans', 16, 'bold'), width=24, cursor='hand2', activebackground='magenta2', activeforeground='white', command=change_password)
    submitButton.place(x=100, y=400)

    window.mainloop()

signup_window = Tk()
signup_window.geometry('400x650')
signup_window.title('Signup Page')
signup_window.resizable(False, False)

background = resize_image('Imagee/bg7.png', 400, 650)



bgLabel = Label(signup_window, image=background)
bgLabel.grid()

ac_image = resize_image("Imagee/accc.png", width=190, height=130)
# Resmi konumlandırın
ac_label = Label(signup_window, image=ac_image, bg='#F6F5F2')
ac_label.place(x=100, y=480)

frame = Frame(signup_window, bg='#F6F5F2')
frame.place(x=50, y=50)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Gabriola', 20, 'bold'), bg='#F6F5F2', fg='#401F71')
heading.grid(row=0, column=0, padx=10, pady=10)

emailLabel = Label(frame, text='Email:', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='#F6F5F2', fg='#912BBC')
emailLabel.grid(row=1, column=0, sticky='w', padx=25)

emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='#77B0AA')
emailEntry.grid(row=2, column=0, sticky='w', padx=25, pady=(10, 0))

usernameLabel = Label(frame, text='Username:', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='#F6F5F2', fg='#912BBC')
usernameLabel.grid(row=3, column=0, sticky='w', padx=25, pady=(10, 0))

usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='#77B0AA')
usernameEntry.grid(row=4, column=0, sticky='w', padx=25)

passwordLabel = Label(frame, text='Password:', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='#F6F5F2', fg='#912BBC')
passwordLabel.grid(row=5, column=0, sticky='w', padx=25, pady=(10, 0))

passwordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='white', bg='#77B0AA')
passwordEntry.grid(row=6, column=0, sticky='w', padx=25)

confirmLabel = Label(frame, text='Confirm Password:', font=('Microsoft Yahei UI Light', 12, 'bold'), bg='#F6F5F2', fg='#912BBC')
confirmLabel.grid(row=7, column=0, sticky='w', padx=25, pady=(10, 0))

confirmEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 10, 'bold'), fg='black', bg='#77B0AA')
confirmEntry.grid(row=8, column=0, sticky='w', padx=25)

check = IntVar()
termsandconditions = Checkbutton(frame, text='I agree to the Terms & Conditions', font=('Microsoft Yahei UI Light', 10, 'bold'), fg='firebrick1', bg='#F6F5F2', activeforeground='firebrick1', activebackground='#F6F5F2', cursor='hand2', variable=check)
termsandconditions.grid(row=9, column=0, pady=10, padx=15)

signupButton = Button(frame, text='Signup', font=('Open Sans', 16, 'bold'), bd=0, bg='#401F71', fg='white', activebackground='#6420AA', activeforeground='white', width=19, command=connect_database)
signupButton.grid(row=10, column=0)

alreadyaccount = Label(frame, text="Don't have an account? ", font=('Open Sans', '9', 'bold'), bg='#F6F5F2', fg='firebrick1')
alreadyaccount.grid(row=11, column=0, sticky='w', padx=25, pady=10)

loginButton = Button(frame, text='Log in', font=('Open Sans', '9', 'bold underline'), bg='#F6F5F2', fg='blue', bd=0, cursor='hand2', activebackground='white', activeforeground='blue', command=login_page)
loginButton.place(x=220, y=409)

signup_window.mainloop()
