import os


def get_source_file_from_root(file_name: str):
    return os.path.dirname(os.path.abspath(__file__)) + file_name

def get_source_file_from_test_resources(file_name: str):
    return os.path.dirname(os.path.abspath(__file__)) + "/resources/" + file_name