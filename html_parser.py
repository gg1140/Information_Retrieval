"""
#   Responsible for file reading
#   Parsing HTML documents for search engine indexer
#   Into HTML object that could be used to retrive information
"""
import time
import codecs
import StringIO
import os
from lxml import html, etree
import json

from doc_struct import doc_struct
from posting import posting
from new_tokenizer import wl_tokenize as tokenize
from new_tokenizer import tok_counting as counting

scored_tag_name = set() #(tag)
inverted_index = dict() #tok:(docID, ifd, score)
doc_dic = dict() #docID: Doc_obj
stop_words = set() #(tok)

# token_log = set() #(tok, total_freq, doc_occurrance)
tag_log = set() #(tag, occurrance, contain_text_count)
#exception_log = list() #(string)

def read_web_doc(file_name):
    '''
    #   generally, the size of web document should fit nicely within memory
    #   return string that contain the content of file
    '''
    with codecs.open(file_name, encoding='UTF-8', mode='r', errors='ignore') as web_doc: #seek doc from disk
        return web_doc.read() #read from memory

def load_scored_tag_name(file_path):
    global scored_tag_name
    with codecs.open(file_path, encoding='UTF-8', mode='r') as f:
        scored_tag_name.clear()
        scored_tag_name = json.load(f)

def _extract_txt_from_html(html_str):
    temp_txt_storage = dict() #{tag:[str, str, ...]}
    parser = etree.HTMLParser()

    tree = etree.parse(StringIO.StringIO(html_str), parser)
    body_ele = tree.xpath('/html/body')[0] #'//p') #list of all <p>
    for i in body_ele.iter():
        ls = temp_txt_storage.get(i.tag)
        if ls == None:
            ls = list()
            ls.append(i.text)
            ls.append(i.tail)
            temp_txt_storage[i.tag] = ls
        else:
            ls.append(i.text)
            ls.append(i.tail)
    return temp_txt_storage

def _generate_doc_obj(docID, extracted_txt):
    doc = doc_struct(docID)
    for tag in extracted_txt:
        for txt in extracted_txt[tag]:
            if txt != None:
                tokens = tokenize(txt)
                for token in tokens:
                    doc.add_tok(token, tag)
    return docprint(doc)

def _create_inverted_index(doc):
    pass

def output_index(destination):
    pass


if __name__ == '__main__':
    load_scored_tag_name('text_tag_whitelist.json')
    web_doc_lib_path = './WEBPAGES_RAW'

#    for root, directory, files in os.walk(web_doc_lib_path):
#        if len(files) != 0:
#            for f in files:
#                file_path = (os.path.join(root,f))
#                doc_ID = file_path[15:]
    file_path = 'my_test_html.html'
    raw_str = read_web_doc(file_path)
    _generate_doc_obj(file_path, _extract_txt_from_html(raw_str))
