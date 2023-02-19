"""Defines patterns for callbacks"""


def set_group_pattern(callback_data):
    """Pattern for set_group"""
    if isinstance(callback_data, tuple):
        if callback_data[0] == "set_group":
            return True
    return False


def pick_faculty_pattern(callback_data):
    """Pattern for pick_faculty"""
    if isinstance(callback_data, tuple):
        if callback_data[0] == "pick_faculty" and callback_data[1]:
            return True
    return False


def pick_group_pattern(callback_data):
    """Pattern for pick_group"""
    if isinstance(callback_data, tuple):
        if callback_data[0] == "pick_group" and callback_data[1]:
            return True
    return False


def start_pattern(callback_data):
    """Pattern for start"""
    if isinstance(callback_data, tuple):
        if callback_data[0] == "start":
            return True
    return False
