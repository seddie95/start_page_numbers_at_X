# start_page_numbers_at_X
This application was developed to make the process of numbering word files from a specific page much simpler,
as Microsoft Word does not provide a straightforward method to achieve this. 

The Frontend serves the purpose of uploading the word document to the server and providing the users 
specifications to the backend.
The Backend is served using the [Django](https://www.djangoproject.com/) Web Framework. Django models are used to create database entries with information about the files including the name, time of upload (For deletion purposes)
and the path to the saved file.

The word documents are then edited using the  [python-docx](https://python-docx.readthedocs.io/en/latest/) 
library to manipulate the word documents XML files.  The numbered word files are then made available for
download by the web application.

## Application Instructions 
Before using this application you will be required to have a word document in .docx format. Word documents with Heading 1 headings are required, as it is not possible to determine the page numbers in python docx as it will change when rendered.


<p align="center">
  <img width="750"  src="start_page_numbers_at_X/static/images/select_heading.PNG">
</p>

The first option that is required is to choose the heading  as seen above on the left hand side, which will start the new section. This will place the paragraph number corresponding to the selected heading into the input box with the label “Paragraph number of Headings”

The Options seen above on the right hand side are optional 
The position option denotes where on the page the numbering will be either left, center or right.

The final option allows the user to specify the numbering style that will appear in the first section of the word document, these styles include Roman Numerals and Upper-case letters.

Once the user is satisfied, they can then submit the document to be numbered.
After the file has been processed the numbered word file is returned to the user to be downloaded.

### Numbering Process
The initial aim when using python-docx was to obtain the page numbers using page breaks. 
In a word XML file, the “lastRenderedPageBreak” attribute often denotes where one page ends and another starts 
but this is not always the case and as such should not be depended on. 
The solution found in this approach was to use page headings to suggest where section breaks should be inserted. 
All headings were used to begin with but this took up far too much space on the web application when large documents are processed,
which can lead to confusion on the users part. Users are more likely to want to start numbering from a new section beginning with a “Heading 1”.

# Running Locally
In order to run this application locall you  follow these steps.

Clone the repository using Git 

```bash
git clone https://github.com/seddie95/start_page_numbers_at_X.git
```

Create a new python environment and install the dependencies
```bash
pip install -r requirements.txt
```
Once Django has been installed successfully migrate the model data to the sqlite3 database
```bash
python manage.py makemigrations
python manage.py migrate
```
After successful migration start the django server 
```bash
python manage.py runserver
```
Then open the site at http://127.0.0.1:8000/
