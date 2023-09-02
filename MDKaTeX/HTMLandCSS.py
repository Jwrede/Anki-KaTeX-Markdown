""" This file contains all the HTML / CSS strings for the different card types """
import os


def file_to_string(path):
    """Returns the content of a file as a string"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def path_relative_to_this_file(path):
    """Returns the absolute path of a file relative to this file"""
    return os.path.join(os.path.dirname(__file__), path)


HTMLforEditor = file_to_string(
    path_relative_to_this_file("js/HTMLforEditor.js"))

front = file_to_string(path_relative_to_this_file("html/front.html"))

back = file_to_string(path_relative_to_this_file("html/back.html"))

front_cloze = file_to_string(
    path_relative_to_this_file("html/front_cloze.html"))

back_cloze = file_to_string(path_relative_to_this_file("html/back_cloze.html"))

css = file_to_string(path_relative_to_this_file("css/style.css"))
