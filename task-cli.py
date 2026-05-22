import sys
import json
import os
from time import sleep


def save_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_data(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            data = json.dump([], f)
    with open(filename, "r") as f:
        data = json.load(f)
        return data


def error(*messages):
    clear_screen()
    for message in messages:
        print(message)
        sleep(1)
    sleep(3)
    clear_screen()
    exit()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# Global Variables:
TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"

# Global functions:
ALL_TASKS = load_data(TASKS_FILE)
ALL_USERS = load_data(USERS_FILE)


def user_login(username, password):
    global ALL_USERS

    if not ALL_USERS:
        error(
            "No users exist!",
            "Please create one with the following syntax:",
            "task-cli.py new_user [username] [password].",
        )

    for user in ALL_USERS:
        if sys.argv[2] == user["username"]:
            print("User exists, checking password...")
            if sys.argv[3] != user["password"]:
                error("Password incorrect")


def new_user(username, password):
    global ALL_USERS

    for user in ALL_USERS:
        if user["username"] == username:
            error("Username Already Exists, try again!")
            break

    id = max((user["id"] for user in ALL_USERS), default=0) + 1

    add_user = {
        "id": id,
        "username": username,
        "password": password,
    }

    ALL_USERS.append(add_user)

    save_data(ALL_USERS, USERS_FILE)

    error("New User Added!")


def change_password(username, password):
    pass


def main():
    # if the arg length is only 2:
    if len(sys.argv) == 2:
        error("Please enter a username and password!")

    # if arg length is only 1:
    if len(sys.argv) <= 1:
        error(
            "Please use login details then task actions",
            "Syntax: task-cli.py [username] [password] [function] [task id] [parameter]",
        )
    # if the first arg provided says 'new_user' use new_user function
    if str(sys.argv[1]).lower() == "new_user":
        new_user(str(sys.argv[2]), str(sys.argv[3]))

    # if the first arg entered is 'new_user' but no other arg provided after:
    if str(sys.argv[1]).lower() == "new_user" and len(sys.argv) < 2:
        error(
            "Please enter a username and password to create new user",
            "Syntax: task-cli.py new_user [username] [password]",
        )

    # If the first arg entered is change password:
    if str(sys.argv[1]).lower() == "change_password":
        change_password(str(sys.argv[2]), str(sys.argv[3]))

    if str(sys.argv[1]).lower() == "change_password" and len(sys.argv) < 2:
        error(
            "Please enter an existing username and password to change password",
            "Syntax: task-cli.py change_password [username] [password]",
        )
    
    


main()
