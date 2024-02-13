from os import path, walk
import json
import threading
import time

SAVED_DATA_FOLDER = "data.json"
INTERVAL = 1

ACTIVE = True
SOURCE_FOLDER = ''
REPLICA_FOLDER = ''
FILES_INFO = {}

mutex = threading.Lock()


def set_source_folder(source: str):
    mutex.acquire()
    try:
        global SOURCE_FOLDER
        SOURCE_FOLDER = source
    finally:
        mutex.release()
    # TODO More commands


def set_replica_folder(replica: str):
    global REPLICA_FOLDER
    mutex.acquire()
    try:
        REPLICA_FOLDER = replica
    finally:
        mutex.release()
    # TODO More commands


def set_files_info(files: dict):
    global FILES_INFO
    mutex.acquire()
    try:
        FILES_INFO = files
    finally:
        mutex.release()
    # TODO more commands


def get_folder_info():
    files_info = {}
    mutex.acquire()
    for (root, dirs, files) in walk(SOURCE_FOLDER, topdown=True):
        file_list = []
        dir_list = []

        for file in files:
            file_list.append((file, path.getctime(path.join(root, file))))

        for directory in dirs:
            dir_list.append(
                (directory, path.getctime(path.join(root, directory))))

        files_info[root] = {
            'directories': tuple(dir_list),
            'files': tuple(file_list)
        }
    mutex.release()
    set_files_info(files_info)


def save_data():
    mutex.acquire()
    data = {
        "source_folder": SOURCE_FOLDER,
        "replica_folder": REPLICA_FOLDER,
        "files_info": FILES_INFO
    }
    mutex.release()
    with open(path.join(path.dirname(__file__), SAVED_DATA_FOLDER), "w") as outfile:
        json.dump(data, outfile)


def load_data():
    with open(path.join(path.dirname(__file__), SAVED_DATA_FOLDER), "r") as openfile:
        data = json.load(openfile)

    set_source_folder(data["source_folder"])
    set_replica_folder(data["replica_folder"])
    set_files_info(data["files_info"])


def reset_data():
    # TODO
    pass


def sync():
    while (ACTIVE):
        get_folder_info()
        save_data()
        time.sleep(INTERVAL)
    # TODO


if (path.exists(path.join(path.dirname(__file__), SAVED_DATA_FOLDER))):
    load_data()

if SOURCE_FOLDER == '':
    set_source_folder(input("Type the folder you want to synchronize: "))
    print()

if REPLICA_FOLDER == '':
    set_replica_folder(
        input("Type the folder where you want to store the files: "))
    print()

print(SOURCE_FOLDER)

thread = threading.Thread(target=sync)
thread.start()

while (ACTIVE):
    command = input("Enter\n")

    if command.lower() == "exit":
        ACTIVE = False
        thread.join()
        break
