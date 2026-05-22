import sys
import json
import os
from time import sleep
from datetime import datetime


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
        if user["username"] == username:
            if user["password"] == password:
                return user
            else:
                return None, error("Password Incorrect, try again!")
    else:
        return None, error("Username doesn't exist!")


def new_user(username, password):
    global ALL_USERS

    for user in ALL_USERS:
        if user["username"] == username:
            error("Username Already Exists, try again!")
            break

    id = max((user["id"] for user in ALL_USERS), default=0) + 1

    now = str(datetime.now().replace(microsecond=0))

    add_user = {
        "id": int(id),
        "username": username,
        "password": password,
        "created_at": now,
        "last_updated": None,
    }

    ALL_USERS.append(add_user)

    save_data(ALL_USERS, USERS_FILE)

    error("New User Added!")


def change_password(username, old_password, new_password):
    global ALL_USERS

    if not ALL_USERS:
        error(
            "No Existing Users!",
            "Please create a new user first with 'new_user' [username] [password]",
        )

    now = str(datetime.now().replace(microsecond=0))

    current_user = user_login(username, old_password)
    if current_user:
        for user in ALL_USERS:
            if str(user["id"]) == str(current_user["id"]):
                user["password"] = new_password
                user["last_updated"] = now
                save_data(ALL_USERS, USERS_FILE)
                error(f"Password updated for '{user['username']}'")


def add_task(username, password, task_title):
    global ALL_TASKS
    global ALL_USERS

    current_user = user_login(username, password)

    if current_user:
        current_user_tasks = []

        for task in ALL_TASKS:
            if str(task["user_id"]) == str(current_user["id"]):
                current_user_tasks.append(task)

        id = max((task["id"] for task in current_user_tasks), default=0) + 1

        new_task = {
            "id": int(id),
            "user_id": int(current_user["id"]),
            "title": task_title,
            "status": "to-do",
            "created_at": f"{datetime.now().replace(microsecond=0)}",
            "updated_at": None,
        }

        ALL_TASKS.append(new_task)
        save_data(ALL_TASKS, TASKS_FILE)
        error(f"Task added for user '{current_user['username']}'!")


def delete_task(username, password, task_id):
    global ALL_TASKS
    # implement the search function via string also
    current_user = user_login(username, password)
    if current_user:
        for i, task in enumerate(ALL_TASKS):
            if str(task["user_id"]) == str(current_user["id"]):
                if str(task["id"]) == task_id:
                    del ALL_TASKS[i]
                    save_data(ALL_TASKS, TASKS_FILE)
                    error("Task deleted successfully!")
        else:
            error("No task with this ID, try again!")


def update_task(username, password, task_search, new_title):
    global ALL_TASKS

    current_user = user_login(username, password)

    now = str(datetime.now().replace(microsecond=0))

    if current_user:
        if task_search.isnumeric():
            for task in ALL_TASKS:
                if str(task["id"]) == str(task_search) and str(task["user_id"]) == str(
                    current_user["id"]
                ):
                    old = task["title"]
                    task["title"] = new_title
                    task["updated_at"] = now
                    save_data(ALL_TASKS, TASKS_FILE)
                    error(
                        f"Updating task for '{current_user['username']}' from '{old}' to '{new_title}'"
                    )
            else:
                error("No task found with that id")
        else:
            counter = 0
            for task in ALL_TASKS:
                if task["title"].lower() == task_search.lower() and str(
                    task["user_id"]
                ) == str(current_user["id"]):
                    counter += 1

            if counter == 1:
                for task in ALL_TASKS:
                    if task["title"].lower() == task_search.lower() and str(
                        task["user_id"]
                    ) == str(current_user["id"]):
                        old = task["title"]
                        task["title"] = new_title
                        task["update_at"] = now
                        save_data(ALL_TASKS, TASKS_FILE)
                        error(
                            f"Updating task for '{current_user['username']}' from '{old}' to '{new_title}'"
                        )
                else:
                    error("No task found with that title")
            else:
                error(
                    "You have more than one task with the same title, please use task id instead!"
                )


def list_view(username, password, list_type = ""):
    global ALL_TASKS
    
    current_user = user_login(username, password)
    
    if list_type not in ['done', 'todo', 'to-do', 'pending', 'in progress', 'in-progress', "", ]

def main():
    if len(sys.argv) <= 2:
        error(
            "Please use login details then task actions",
            "Syntax: task-cli.py [username] [password] [function] [task id] [parameter]",
        )

    # Add a new user:
    if str(sys.argv[1]).lower() == "new_user" and len(sys.argv) == 4:
        new_user(str(sys.argv[2]), str(sys.argv[3]))

    if str(object=sys.argv[1]).lower() == "new_user" and len(sys.argv) <= 3:
        error(
            "Please enter a username and password to create new user",
            "Syntax: task-cli.py new_user [username] [password]",
        )

    # Change a users password:
    if str(sys.argv[1]).lower() == "change_password" and len(sys.argv) == 5:
        change_password(str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))

    if str(sys.argv[1]).lower() == "change_password" and len(sys.argv) <= 4:
        error(
            "Please enter an existing username and password to change password",
            "Syntax: task-cli.py change_password [username] [old password] [password]",
        )

    # Add new task:
    if len(sys.argv) < 5 and str(sys.argv[3]).lower() == "add_task":
        error(
            "Please enter in the following format:",
            "task-cli.py [username] [password] add_task [task title]",
        )

    if len(sys.argv) == 5 and str(sys.argv[3]).lower() == "add_task":
        add_task(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[4]))

    # Delete Task:
    if len(sys.argv) < 5 and str(sys.argv[3]).lower() == "delete_task":
        error(
            "Please enter in the following format:",
            "task-cli.py [username] [password] delete_task [task id]",
        )
    if len(sys.argv) == 5 and str(sys.argv[3]).lower() == "delete_task":
        delete_task(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[4]))

    # Update Task:
    if len(sys.argv) < 6 and str(sys.argv[3]).lower() == "update_task":
        error(
            "Please enter in the following format:",
            "task-cli.py [username] [password] update_task [task id / title] [new task title]",
        )
    if len(sys.argv) == 6 and str(sys.argv[3]).lower() == "update_task":
        update_task(
            str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[4]), str(sys.argv[5])
        )


main()
