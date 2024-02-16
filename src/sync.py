from os import path, walk
from deepdiff import DeepDiff
import json
import threading
import time
import shutil

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


def get_folder_info(folder):
    files_info = {}
    mutex.acquire()
    for (root, dirs, files) in walk(folder, topdown=True):
        file_list = []
        dir_list = []

        for file in files:
            file_list.append((file, path.getctime(path.join(root, file))))

        for directory in dirs:
            dir_list.append(
                (directory, path.getctime(path.join(root, directory))))

        files_info[root] = {
            'directories': dir_list,
            'files': file_list
        }
    mutex.release()
    return files_info


def compare_folder_info(folder_info):
    differences = DeepDiff(FILES_INFO, folder_info)

    differences = {
        'added': differences['dictionary_item_added']
    }
    return differences


def copy_files(differences):
    if differences == {}:
        return
    print(differences)

    shutil.copytree(SOURCE_FOLDER, REPLICA_FOLDER, dirs_exist_ok=True)


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


def sync():
    while (ACTIVE):
        replica_files_info = get_folder_info(REPLICA_FOLDER)
        differences = compare_folder_info(replica_files_info)
        copy_files(differences)

        source_files_info = get_folder_info(SOURCE_FOLDER)
        differences = compare_folder_info(source_files_info)
        set_files_info(source_files_info)
        save_data()
        copy_files(differences)

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

print("Source folder: ", SOURCE_FOLDER)
print("Replica: ", REPLICA_FOLDER)

thread = threading.Thread(target=sync)
thread.start()

while (ACTIVE):
    command = input("Enter\n")

    if command.lower() == "exit":
        ACTIVE = False
        thread.join()
        break
