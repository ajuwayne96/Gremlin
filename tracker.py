import os
import time

def get_last_edit_time(folder):
    latest_edit = 0
    for root, _, files in os.walk(folder):
        for file in files:
            try:
                filepath = os.path.join(root, file)
                edit_time = os.path.getmtime(filepath)
                if edit_time > latest_edit:
                    latest_edit = edit_time
            except:
                continue
    return latest_edit

def days_since_edit(folder):
    last_edit = get_last_edit_time(folder)
    if last_edit == 0:
        return 999  # No files found
    return int((time.time() - last_edit) / 86400)
