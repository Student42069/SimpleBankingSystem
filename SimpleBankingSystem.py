import random
import sys
import sqlite3

open("card.s3db", "a").close()
conn = sqlite3.connect("card.s3db")
cur = conn.cursor()

cur.execute("CREATE table IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()

def lunh(card):
    count = 0
    sum1 = 0
    for i in str(card):
        if count%2 == 0:
            sum2 = int(i)*2
            if sum2 > 9:
                sum2 = sum2 - 9
            sum1 += sum2
            count += 1
        else:
            sum1 += int(i)
            count += 1
    if sum1%10 == 0:
        return True
    else:
        return False

def transfer_menu(account_number):
    while True:
        print("\nTransfer\nEnter card number:")
        send = input()
        possible = lunh(send)

        if account_number == send:
            print("You can't transfer money to the same account!\n")
            break
        if possible == False:
            print("Probably you made a mistake in the card number. Please try again!\n")
            break
        else:
            cur.execute(f"SELECT number, pin, balance FROM card WHERE number = {send}")
            existe = cur.fetchone()
            conn.commit()

            if type(existe) == type(None):
                print("Such a card does not exist.\n")
                break
            else:
                print("Enter how much money you want to transfer:")
                transfer = int(input())
                cur.execute(f"SELECT balance FROM card WHERE number={account_number}")
                available = cur.fetchone()[0]
                conn.commit()

                if available < transfer:
                    print("Not enough money!\n")
                    break
                elif available > transfer:
                    cur.execute(f"SELECT balance FROM card WHERE number={send}")
                    send_balance = cur.fetchone()[0]
                    conn.commit()
                    cur.execute(f"UPDATE card SET balance={send_balance+transfer} WHERE number={send}")
                    conn.commit()
                    cur.execute(f"UPDATE card SET balance={available - transfer} WHERE number={account_number}")
                    conn.commit()
                    print("Success!\n")
                    break

def pinnumber(number):
    num = ""
    for i in range(number):
        num += str(random.randint(0,9))
    return num

def cardnumber(number):
    num = "400000"
    for i in range(number-1):
        num += str(random.randint(0,9))
    count = 0
    sum1 = 0
    for i in num:
        if count%2 == 0:
            sum2 = int(i)*2
            if sum2 >9:
                sum2 = sum2 - 9
            sum1 += sum2
            count += 1
        else:
            sum1 += int(i)
            count += 1
    if sum1%10 == 0:
        num += "0"
    else:
        last = (((sum1//10) + 1)*10) - sum1
        num += str(last)
    return num

def account_menu(number2):
    while True:
        print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")
        account_choice = int(input(""))

        if account_choice == 0:
            sys.exit()
        elif account_choice == 1:
            cur.execute(f"SELECT balance FROM card WHERE number={number2}")
            print(f"\nBalance: {cur.fetchone()[0]}\n")
            conn.commit()
        elif account_choice == 2:
            cur.execute(f"SELECT balance FROM card WHERE number={number2}")
            print("\nEnter income:")
            income = cur.fetchone()[0] + int(input())
            conn.commit()
            print("Income was added!\n")
            cur.execute(f"UPDATE card SET balance={income} WHERE number={number2}")
            conn.commit()
        elif account_choice == 3:
            transfer_menu(number2)
        elif account_choice == 4:
            cur.execute(f"DELETE FROM card WHERE number = {number2}")
            conn.commit()
            print("\nThe account has been closed!\n")
            break
        elif account_choice == 5:
            print("\nYou have successfully logged out!\n")
            break

while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    choice = int(input(""))

    if choice == 0:
        print("\nBye!")
        break
    elif choice == 1:
        number = cardnumber(10)
        pin = pinnumber(4)
        print(f"\nYour card has been created\nYour card number:\n{number}\nYour card PIN:\n{pin}\n")
        cur.execute(f"INSERT INTO card (number, pin, balance) VALUES({number},{pin},0)")
        conn.commit()
    elif choice == 2:
        inputnumber = input("\nEnter your card number:\n")
        pin = input("Enter your PIN:\n")
        cur.execute(f"SELECT number, pin FROM card WHERE number = {inputnumber} AND pin = {pin}")
        verification = cur.fetchone()
        conn.commit()

        if type(verification) != type(None):
            if len(verification[1]) == 3:
                verification = list(verification)
                verification[1] = "0" + verification[1]
        if type(verification) == type(None) or len(verification[0]) != 16:
            print("\nWrong card number or PIN!\n")
        elif verification[1] == pin:
            print("\nYou have successfully logged in!\n")
            account_menu(inputnumber)
        else:
            print("\nWrong card number or PIN!\n")