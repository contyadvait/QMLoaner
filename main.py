from time import sleep
import hashlib
from getpass import getpass
import mongodb
from pdfs import create_loa_pdf, create_loan_pdf
import secrets

username = ""
password = ""

from datetime import datetime


def validate_date(date_str):
    if len(date_str) != 8:  # Save time with some pre-processing
        return False

    try:
        # Create a date time object from the string
        datetime.strptime(date_str, "%d%m%Y")
        return True
    except ValueError:
        # If fails, return not possible
        return False


def sha256_hash(data):
    hasher = hashlib.sha256()
    hasher.update(data.encode())
    return hasher.hexdigest()


def verified_input(question, max_int, min_int):
    while True:
        answer = input(question)
        try:
            if int(answer) > min_int or int(answer) < max_int:
                print("Your answer is beyond the numbers provided. Please enter again")
            else:
                break
        except ValueError:
            print("Your answer is not a valid number. Please enter again.")

    return answer


def login_page():
    global username, password
    while True:
        userID = input("Please enter your username (enter q to exit): ")
        if userID == "q":
            print("Exiting...")
            exit(0)
        password = getpass("Please enter your password: ")
        result = mongodb.login(userID, password)
        if result:
            print("Login successful!")
            break
        else:
            print("Login failed. Please try again.")


def create_loa():
    while True:
        loa_date = input("What is the date you are not coming for CCA? (in DDMMYYYY) ")
        if validate_date(loa_date):
            break

        else:
            print("The date is invalid.")

    reason = input("What is the reason for not coming on that date? ")

    while True:
        name = input("What is your name? (Please enter in the exact format of the attendance sheet) ")

        if name.title() in secrets.NAMES:
            break
        else:
            print("Name not found. Please try again.")

    create_loa_pdf(name=name.title(), reason=reason, date=loa_date)
    print("PDF created successfully and sent!")
    print("Thank you for using SPSGE App!")
    print("To do something else, please run the app again.")


def main():
    print("Welcome to the SPSGE Loan App!")
    print("Please select one of the options, based on the index on the side (the number in the square brackets)")
    print("[1] Log in")
    print("[2] Request a Leave-Of-Absence")
    print("[3] Loan a guitar")
    print("[4] Exit")
    answer = verified_input("Which index would you like to select? ", 1, 2)
    if answer == "1":
        login_page()
    elif answer == "2":
        create_loa()
    else:
        exit(0)


if __name__ == "__main__":
    main()
