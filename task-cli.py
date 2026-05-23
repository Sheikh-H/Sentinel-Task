import sys
import json
import os
from time import sleep
from datetime import datetime

# Global Variables:
TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"

# Global functions:
ALL_TASKS = load_data(TASKS_FILE)
ALL_USERS = load_data(USERS_FILE)


def save_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_data(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)
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
                error("Password Incorrect, try again!")
    else:
        error("Username doesn't exist!")


def new_user(username, password):
    global ALL_USERS

    for user in ALL_USERS:
        if user["username"] == username:
            error("Username Already Exists, try again!")
            break

    user_id = max((user["id"] for user in ALL_USERS), default=0) + 1

    now = str(datetime.now().replace(microsecond=0))

    add_user = {
        "id": int(user_id),
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

        task_id = max((task["id"] for task in current_user_tasks), default=0) + 1

        new_task = {
            "id": int(task_id),
            "user_id": int(current_user["id"]),
            "title": task_title,
            "status": "Recently added",
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
                        task["updated_at"] = now
                        save_data(ALL_TASKS, TASKS_FILE)
                        error(
                            f"Updating task for '{current_user['username']}' from '{old}' to '{new_title}'"
                        )
            else:
                error(
                    "You have more than one task with the same title, please use task id instead!"
                )


def list_task(username, password, list_type):
    global ALL_TASKS

    current_user = user_login(username, password)

    if list_type == "all":
        for task in ALL_TASKS:
            if str(task["user_id"]) == str(current_user["id"]):
                print("-" * 50)
                print(f"Task ID: {task['id']}")
                print(f"Title: {task['title']}")
                print(f"Status: {task['status']}")
                print(f"Created at: {task['created_at']}")
                print(f"Last updated: {task['updated_at']}")
    elif list_type in ["completed", "finished", "done"]:
        view_tasks_print(current_user, "completed")
    elif list_type in [
        "to-do",
        "incomplete",
        "not done",
        "unfinished",
        "todo",
        "pending",
    ]:
        view_tasks_print(current_user, "to-do")
    elif list_type in ["just started", "new", "recently added", "new tasks"]:
        view_tasks_print(current_user, "recently added")
    else:
        error(
            "Please enter from the following values:",
            "['completed', 'finished', 'done', 'to-do', 'incomplete', 'not done', 'unfinished','todo', 'pending','just started', 'new', 'recently added', 'new tasks']",
            "Or leave blank to have all tasks displayed",
        )


def view_tasks_print(user, category):
    global ALL_TASKS
    found = False
    for task in ALL_TASKS:
        if (
            str(task["user_id"]) == str(user["id"])
            and task["status"].lower() == category
        ):
            found = True
            print("-" * 50)
            print(f"Task ID: {task['id']}")
            print(f"Title: {task['title']}")
            print(f"Status: {task['status']}")
            print(f"Created at: {task['created_at']}")
            print(f"Last updated: {task['updated_at']}")

    if not found:
        error(f"You have no {category} tasks!")


def main():
    if len(sys.argv) <= 2 or "--help" in sys.argv:
        error(
            "To use the Task Manager CLI, please enter with the following syntax:",
            "To add new user: task-cli.py new_user [new username] [new password]",
            "To change password: task-cli.py change_password [username] [old password] [new password]",
            "To add a task: task-cli.py [username] [password] add_task [task title]",
            "To update a task: task-cli.py [username] [password] update_task [task id number or 'task title']",
            "To delete a task: task-cli.py [username] [password] delete_task [task id number or 'task title']",
            "To view all tasks: task-cli.py [username] [password] view",
            "To view specific type of tasks: task-cli.py [username] [password] view [type of task i.e. 'to be completed']",
            "NOTE: Where you could use more than one word for a criteria please enclose in speech marks ('')",
            "Type task-cli.py --help to see this menu again",
        )
    elif len(sys.argv) == 4 and sys.argv[1].lower() == "new_user":
        new_user(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5 and sys.argv[1].lower() == "change_password":
        change_password(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "add_task":
        add_task(sys.argv[1], sys.argv[2], sys.argv[4])
    elif len(sys.argv) == 6 and sys.argv[3].lower() == "update_task":
        update_task(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5])
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "delete_task":
        delete_task(sys.argv[1], sys.argv[2], sys.argv[4])
    elif len(sys.argv) == 4 and sys.argv[3].lower() == "view":
        list_task(sys.argv[1], sys.argv[2], "all")
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "view":
        list_task(sys.argv[1], sys.argv[2], sys.argv[4].lower())
    else:
        error("Invalid command!", "Type task-cli.py --help for manual")


if __name__ == "__main__":
    main()
