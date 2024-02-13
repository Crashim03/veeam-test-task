from os import path
import json

SAVED_DATA_FOLDER = "data.json"

SOURCE_FOLDER = ''
REPLICA_FOLDER = ''


def set_origin_folder(source: str):
    SOURCE_FOLDER = source
    # TODO More commands


def set_replica_folder(replica: str):
    REPLICA_FOLDER = replica
    # TODO More commands


def save_data():
    data = {
        "source_folder": SOURCE_FOLDER,
        "replica_folder": REPLICA_FOLDER
    }

    with open(path.join(path.dirname(__file__), SAVED_DATA_FOLDER), "w") as outfile:
        json.dump(data, outfile)


def load_data():
    with open(path.join(path.dirname(__file__), SAVED_DATA_FOLDER), "r") as openfile:
        data = json.load(openfile)

    set_origin_folder(data["source_folder"])
    set_replica_folder(data["replica_folder"])


def reset_data():
    # TODO
    pass


def sync():
    # TODO
    pass


if (path.exists(path.join(path.dirname(__file__), SAVED_DATA_FOLDER))):
    load_data()
