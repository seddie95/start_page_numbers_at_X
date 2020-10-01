import os
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "specific_page.settings")
import django

django.setup()
from pages.models import WordDoc


def remove(file_path):
    """ Remove the file or directory"""
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
    """ Remove numbered doc files from the path older than 2 minutes"""
    time_in_secs = time.time() - delete_time
    for root, dirs, files in os.walk(file_path, topdown=False):
        for file_ in files:
            full_path = os.path.join(root, file_)
            stat = os.stat(full_path)

            if stat.st_mtime <= time_in_secs:
                remove(full_path)

        if not os.listdir(root):
            remove(root)


def clean_database(delete_time):
    """ Delete database entries with unprocessed files after 2 minutes"""
    # Obtain the current time and valid time
    current_time = time.time()
    valid_time = current_time - delete_time

    # Retrieve all of the word doc models
    docs = WordDoc.objects.all()

    # loop through the models and delete if older than 2 minutes
    for doc in docs:
        doc_time = doc.time.timestamp()
        diff = valid_time - doc_time

        if diff > delete_time:
            doc.delete()


if __name__ == "__main__":
    deletion_time = 120
    path = '../media'
    cleanup(deletion_time, path)
    clean_database(deletion_time)
