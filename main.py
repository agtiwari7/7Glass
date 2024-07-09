import sqlite3, sys
import bcrypt, os
import time, random


def create_table():
    # Create the table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age TINYINT NOT NULL,
        contact INTEGER NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance INTEGER NOT NULL
    )
    ''')
    # Commit the changes and close the connection
    conn.commit()

def register():
    try:
        name = input("Enter Your name     : ").split(" ")[0]
        age = int(input("Enter your age      : "))
        contact = int(input("Enter your contact  : "))
        password = input("Enter your password : ")
    except Exception as e:
        print(f"\n{e}\n")
        sys.exit()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        cursor.execute('INSERT INTO users (name, age, contact, password, balance) VALUES (?, ?, ?, ?, ?)', (name, age, contact, hashed, 0))
        conn.commit()
        print("\nUser saved successfully")
    except sqlite3.IntegrityError:
        print("\nUser already exists with this contact number.")

    print("Redirect to login in 3 sec.")
    time.sleep(3)
    screen_clear()

def verify_login(contact, password):
    cursor.execute('SELECT password FROM users WHERE contact = ?', (contact,))
    result = cursor.fetchone()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        return True
    else:
        return False

def login():
    try:
        contact = int(input("Enter your contact  : "))
        password = input("Enter your password : ")
        time.sleep(0.25)

    except Exception as e:
        print(f"\n{e}\n")
        sys.exit()

    if verify_login(contact, password):
        screen_clear()
        print("Logged in successfully")
        print(f"Your balance is  : {show_balance(contact)}")
        return contact
    else:
        print("\nInvalid contact or password")
        sys.exit()

def show_balance(contact):
    cursor.execute('SELECT balance FROM users WHERE contact = ?', (contact,))
    result = cursor.fetchone()
    return result[0]

def add_balance(contact):
    previous_balance = show_balance(contact)
    balance = int(input("\nEnter your money : "))
    cursor.execute('UPDATE users SET balance = ? WHERE contact = ?', (previous_balance+balance, contact))
    conn.commit()
    print(f"Your balance is  : {show_balance(contact)}")

def screen_clear():
    if os.name == "posix":
        _ = os.system("clear")
    else:
        _ = os.system("cls")

def update_balance(balance, contact):
    cursor.execute('UPDATE users SET balance = ? WHERE contact = ?', (balance, contact))
    conn.commit()

def play(contact):
    main_balance = show_balance(contact)
    print(f"Your current balance is : {main_balance}")
    bet_amount = int(input("\nEnter balance for play  : "))

    if bet_amount>main_balance:
        bet_amount = main_balance
    
    number = random.randint(2,12)
    # number = 7
    bet_side = input("\n(2,3,4,5,6)    - Left\n(    7    )    - Middle\n(8,9,10,11,12) - Right\n\nChoose your bet side : ")

    if (bet_side == "left" or bet_side == "Left") and (number >= 2 and number <=6):
        print("\n You won. Adding 2x of your bet money in account.")
        update_balance((main_balance-bet_amount)+bet_amount*2, contact)
    elif (bet_side == "middle" or bet_side == "Middle") and number == 7:
        print("\n You won. Adding 3x of your bet money in account.")
        update_balance((main_balance-bet_amount)+bet_amount*3, contact)
    elif (bet_side == "right" or bet_side == "right") and (number >= 8 and number <=12):
        print("\n You won. Adding 2x of your bet money in account.")
        update_balance((main_balance-bet_amount)+bet_amount*2, contact)
    else:
        print("\nYou loose. Lost your bet money.")
        update_balance(main_balance-bet_amount, contact)
    
    print(f"\nYour current balance is : {show_balance(contact)}")
    sys.exit()
#--------------------------------------------------------------------------------------------
# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('user_data.db')

# Create a cursor object
cursor = conn.cursor()

create_table()

register_login = input("Register or Login : ")
if register_login == "register" or register_login == "Register":
    time.sleep(0.25)
    screen_clear()
    register()
    login_contact = login()
elif register_login == "login" or register_login == "Login":
    time.sleep(0.25)
    screen_clear()
    login_contact = login()
else:
    print("\n Something went wrong.")
    sys.exit()


add_balance_or_play = input("\nAdd balance or Play : ")
if add_balance_or_play == "add balance" or add_balance_or_play == "Add balance" or add_balance_or_play == "Add Balance":
    time.sleep(0.25)
    screen_clear()
    add_balance(login_contact)
elif add_balance_or_play == "play" or add_balance_or_play == "Play":
    time.sleep(0.25)
    screen_clear()
    play(login_contact)
else:
    print("\n Something went wrong.")
    sys.exit()

conn.close()