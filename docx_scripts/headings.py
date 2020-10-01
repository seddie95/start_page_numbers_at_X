from docx import Document
import os
import time


def get_headings(path, heading='Heading'):
    """Function to retrieve Heading 1 from a word document"""

    # Check whether the file exists
    while not os.path.exists(path):
        time.sleep(1)

    if os.path.isfile(path):
        doc = Document(path)

        return {paragraph.text.strip(): val for (val, paragraph) in enumerate(doc.paragraphs) if
                paragraph.style.name.startswith(heading)}

    else:
        raise ValueError("%s isn't a file!" % path)
