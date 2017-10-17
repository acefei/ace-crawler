#encoding: utf-8
from readability import Document
from lxml.html import document_fromstring

def get_html_body(html):
    doc = Document(html)
    body = doc.summary()
    c = document_fromstring(body)
    return c.text_content()
