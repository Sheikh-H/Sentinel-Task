import sys
import json
import os
from time import sleep
from datetime import datetime
import hashlib
import secrets

# Global Variables:
TASKS_FILE = "tasks.json"
USERS_FILE = "users.json"


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


# Function calls placed here as it's not defining the functions
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
            attempt = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), user["salt"].encode(), 100000
            ).hex()
            if attempt == user["password"]:
                return user
            else:
                error("Password Incorrect, Try again!")
    else:
        error("Username doesn't exist!")


def new_user(username, password):
    global ALL_USERS

    for user in ALL_USERS:
        if user["username"] == username:
            error("Username Already Exists, try again!")

    user_id = max((user["id"] for user in ALL_USERS), default=0) + 1

    now = str(datetime.now().replace(microsecond=0))

    if username.strip() == "" or password.strip() == "":
        error("Please enter a valid username and password to register an account!")

    username = username.strip()
    password = password.strip()

    salt = secrets.token_hex(16)

    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 100000
    ).hex()

    add_user = {
        "id": int(user_id),
        "username": username,
        "password": hashed_password,
        "created_at": now,
        "salt": salt,
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

    current_user_tasks = []

    for task in ALL_TASKS:
        if (
            str(task["user_id"]) == str(current_user["id"])
            and task["title"].lower() == task_title.lower()
        ):
            error("You already have a task with that title!")

    for task in ALL_TASKS:
        if str(task["user_id"]) == str(current_user["id"]):
            current_user_tasks.append(task)

    task_id = max((task["id"] for task in current_user_tasks), default=0) + 1

    new_task = {
        "id": int(task_id),
        "user_id": int(current_user["id"]),
        "title": task_title,
        "status": "To-Do",
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
                        f"Updated task for '{current_user['username']}' from '{old}' to '{new_title}'"
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


def view_tasks_print(user, category):
    global ALL_TASKS
    for task in ALL_TASKS:
        if (
            str(task["user_id"]) == str(user["id"])
            and task["status"].lower() == category.lower()
        ):
            print("-" * 50)
            print(f"Task ID: {task['id']}")
            print(f"Title: {task['title']}")
            print(f"Status: {task['status']}")
            print(f"Created at: {task['created_at']}")
            print(f"Last updated: {task['updated_at']}")
    print("-" * 50)


def list_task(username, password, list_type):
    global ALL_TASKS

    current_user = user_login(username, password)

    if list_type == "all":
        view_tasks_print(current_user, "all")
    elif list_type in ["done", "completed", "finished", "complete"]:
        view_tasks_print(current_user, "completed")
    elif list_type in [
        "new",
        "new tasks",
        "just added",
        "recent",
        "recently added",
        "to-do",
        "todo",
    ]:
        view_tasks_print(current_user, "to-do")
    elif list_type in [
        "doing",
        "current",
        "currently active",
        "active",
        "active tasks",
        "current tasks",
    ]:
        view_tasks_print(current_user, "in-progress")
    else:
        error(
            "To view tasks you can enter a number of phrases that correlate to the task type you would like to view. Here is a list of the ones you can use:",
            "For tasks that are completed: ['done', 'complete', 'completed', 'finished']",
            "For tasks that are in progress: ['doing', 'current', 'currently active', 'active', 'active tasks', 'current tasks']",
            "For tasks that recently added or awaiting to be started ['new', 'new tasks', 'just added', 'recent', 'recently added']",
            "To view all tasks, just exclude a parameter for the type of tasks you want to view or type 'all'",
        )


def mark_as_complete(username, password, task_search):
    global ALL_TASKS

    now = str(datetime.now().replace(microsecond=0))

    current_user = user_login(username, password)

    if task_search.isnumeric():
        for task in ALL_TASKS:
            if (
                str(task["user_id"]) == str(current_user["id"])
                and str(task["id"]) == str(task_search)
                and task["status"].lower() != "COMPLETED".lower()
            ):
                task["status"] = "COMPLETED"
                task["updated_at"] = now
                save_data(ALL_TASKS, TASKS_FILE)
                print(f"Task '{task['title']}' has now been marked as completed!")
                break
        else:
            error("This task is already marked as completed!")
    else:
        for task in ALL_TASKS:
            if (
                task["title"].lower() == task_search.lower()
                and str(task["user_id"]) == str(current_user["id"])
                and task["status"].lower() != "COMPLETED".lower()
            ):
                task["status"] = "COMPLETED"
                task["updated_at"] = now
                save_data(ALL_TASKS, TASKS_FILE)
                print(f"Task '{task['title']}' has now been marked as completed!")
                break
        else:
            error("This task is already marked as completed!")


def mark_in_progress(username, password, task_search):
    global ALL_TASKS

    now = str(datetime.now().replace(microsecond=0))

    current_user = user_login(username, password)

    if task_search.isnumeric():
        for task in ALL_TASKS:
            if (
                str(task["user_id"]) == str(current_user["id"])
                and str(task["id"]) == str(task_search)
                and task["status"].lower() != "IN-PROGRESS".lower()
            ):
                task["status"] = "IN-PROGRESS"
                task["updated_at"] = now
                save_data(ALL_TASKS, TASKS_FILE)
                print(f"Task '{task['title']}' has now been marked as in-progress!")
                break
        else:
            error("This task is already marked as in-progress!")
    else:
        for task in ALL_TASKS:
            if (
                task["title"].lower() == task_search.lower()
                and str(task["user_id"]) == str(current_user["id"])
                and task["status"].lower() != "IN-PROGRESS".lower()
            ):
                task["status"] = "IN-PROGRESS"
                task["updated_at"] = now
                save_data(ALL_TASKS, TASKS_FILE)
                print(f"Task '{task['title']}' has now been marked as in-progress!")
                break
        else:
            error("This task is already marked as in-progress!")


def main():
    if len(sys.argv) <= 2 or "--help" in sys.argv:
        error(
            "To use the Task Manager CLI, please enter with the following syntax:",
            "To add new user: task-cli.py new-user [new username] [new password]",
            "To change password: task-cli.py change-password [username] [old password] [new password]",
            "To add a task: task-cli.py [username] [password] add-task [task title]",
            "To update a task: task-cli.py [username] [password] update-task [task id number or 'task title']",
            "To delete a task: task-cli.py [username] [password] delete-task [task id number or 'task title']",
            "To marks a task as complete: task-cli.py [username] [password] mark-complete [task id number or 'task title']",
            "To marks a task as complete: task-cli.py [username] [password] mark-in-progress [task id number or 'task title']",
            "To view all tasks: task-cli.py [username] [password] view",
            "To view specific type of tasks: task-cli.py [username] [password] view [type of task i.e. 'to be completed']",
            "NOTE: Where you could use more than one word for a criteria please enclose in speech marks ('')",
            "Type task-cli.py --help to see this menu again",
        )
    elif (
        len(sys.argv) == 4
        and sys.argv[1].lower() == "new-user"
        or sys.argv[1].lower() == "add-user"
    ):
        new_user(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5 and sys.argv[1].lower() == "change-password":
        change_password(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "add-task":
        add_task(sys.argv[1], sys.argv[2], sys.argv[4])
    elif len(sys.argv) == 6 and sys.argv[3].lower() == "update-task":
        update_task(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5])
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "delete-task":
        delete_task(sys.argv[1], sys.argv[2], sys.argv[4])
    elif len(sys.argv) == 4 and sys.argv[3].lower() == "view":
        list_task(sys.argv[1], sys.argv[2], "all".lower())
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "view":
        list_task(sys.argv[1], sys.argv[2], sys.argv[4].lower())
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "mark-complete":
        mark_as_complete(sys.argv[1], sys.argv[2], sys.argv[4].lower())
    elif len(sys.argv) == 5 and sys.argv[3].lower() == "mark-in-progress":
        mark_in_progress(sys.argv[1], sys.argv[2], sys.argv[4].lower())

    else:
        error("Invalid command!", "Type task-cli.py --help for manual")


if __name__ == "__main__":
    main()
