import os
import time


def remove(file_path):
    """
    Remove the file or directory
    """
    if os.path.isdir(file_path):
        try:
            os.rmdir(file_path)
        except OSError:
            print("Unable to remove folder: %s" % file_path)
    else:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except OSError:
            print("Unable to remove file: %s" % file_path)


def cleanup(delete_time, file_path):
    """
    Removes files from the passed in path that are older than or equal 
    to the number_of_days
    """
    time_in_secs = time.time() - delete_time
    for root, dirs, files in os.walk(file_path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)

            if stat.st_mtime <= time_in_secs:
                remove(full_path)

        if not os.listdir(root):
            remove(root)


if __name__ == "__main__":
    days, path = 600, '../media'
    cleanup(days, path)
