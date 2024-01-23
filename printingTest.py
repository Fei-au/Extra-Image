from docx import Document
from docx.shared import Pt
import win32api
import os
import time

INV_START = 14600
NUM_OF = 1


def modify_document_and_print(doc, cur_num):
    # Find the bolded number and replace it with the new number
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.bold:
                run.text = str(cur_num)


def print_document(doc):
    modified_doc_path = "modified_template.docx"
    doc.save(modified_doc_path)

    # Send the document to the printer
    win32api.ShellExecute(0, "print", f"{modified_doc_path}", None, ".", 0)

    time.sleep(4)  # Wait for the print job to finish (adjust as needed)

    os.remove(modified_doc_path)


if __name__ == "__main__":
    template_path = "C:/Users/wangk/PycharmProjects/ExtractImage/Label.docx"
    doc = Document(template_path)
    new_number = INV_START

    for _ in range(NUM_OF):
        modify_document_and_print(doc, new_number)
        print_document(doc)
        new_number += 1
        time.sleep(4)  # Add a small delay between each print to avoid overwhelming the printer
