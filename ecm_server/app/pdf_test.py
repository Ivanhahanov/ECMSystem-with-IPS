import pdfminer
from pdfminer.high_level import extract_text
print(pdfminer.__version__)
text = extract_text('files/1.pdf')
print(repr(text))