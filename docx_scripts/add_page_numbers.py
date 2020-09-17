from docx import Document
from docx.oxml import OxmlElement, ns
from django.conf import settings
from docx.shared import Mm
import os

def create_attribute(element, name, value):
    """ Create attribute for a given element """
    element.set(ns.qn(name), value)


def set_page_number_type(fmt='', start_num='1'):
    """ specify the starting page number and style"""
    # Add numbering to section
    num_type = OxmlElement('w:pgNumType')
    create_attribute(num_type, 'w:start', start_num)

    # Set the number format
    if fmt != '':
        create_attribute(num_type, 'w:fmt', fmt)

    return num_type


def add_section(parag, fmt=''):
    """ Create new section tag element"""
    pPr = OxmlElement('w:pPr')
    section = OxmlElement('w:sectPr')

    # set the page number type
    num_type = set_page_number_type(fmt)

    # Append the section to the paragraph
    section.append(num_type)
    pPr.append(section)
    parag._p.append(pPr)


def add_page_number(parag, position=''):
    """ Add page numbers to the footer of the document"""
    run = parag.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    create_attribute(fldChar1, 'w:fldCharType', 'begin')

    instrText = OxmlElement('w:instrText')
    create_attribute(instrText, 'xml:space', 'preserve')
    instrText.text = "PAGE"

    fldChar2 = OxmlElement('w:fldChar')
    create_attribute(fldChar2, 'w:fldCharType', 'end')

    # Set the position for the numbers
    if position != '':
        jc = OxmlElement('w:jc')
        create_attribute(jc, 'w:val', position)
        p = parag._p
        pPr = p.get_or_add_pPr()
        pPr.append(jc)

    # Append the new create elements to the r tag
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


def set_page_size(section):
    """ Ensure that both sections have the same size"""
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Mm(25.4)
    section.right_margin = Mm(25.4)
    section.top_margin = Mm(25.4)
    section.bottom_margin = Mm(25.4)
    section.header_distance = Mm(12.7)
    section.footer_distance = Mm(12.7)


def set_page_numbers(specs):
    # Retrieve page specification variables
    file_name = specs['file_name']
    paragraph_number = int(specs['heading'])
    position = specs['position']
    style = specs['style']

    # Obtain the path to the docx file
    media_root = settings.MEDIA_ROOT
    path = media_root + "\\" + file_name

    # Open existing and find last paragraph before section break
    doc = Document(path)

    # Set the page number type so that it starts from one
    sect = doc.sections[0]._sectPr
    pgNumType = set_page_number_type()
    sect.append(pgNumType)

    # add numbers starting at i
    chosen_paragraph = doc.paragraphs[paragraph_number - 1]
    new_paragraph = chosen_paragraph.insert_paragraph_before()
    add_section(new_paragraph, style)

    # set the page to be A4
    set_page_size(doc.sections[0])
    set_page_size(doc.sections[1])

    # Add the page numbers
    add_page_number(doc.sections[0].footer.paragraphs[0], position)

    # Save a copy of the file with the page numbers
    saved_file = f'media/numbered_{file_name}'
    doc.save(saved_file)

    # Delete original file
    os.remove(path)

    return saved_file
