"""
#   Responsible for file reading
#   Parsing HTML documents for search engine indexer
#   Into HTML object that could be used to retrive information
"""
import time
import codecs
import StringIO
import os
from collections import Counter
from lxml import html, etree
import json

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
       # for _ in f:
       #     scored_tag_name.add(_.strip())
       # print(scored_tag_name)

def _extract_txt_from_html(html_str):
    global scored_tag_name
    temp_txt_storage = dict() #{tag:[str, str, ...]}
    parser = etree.HTMLParser()

    tree = etree.parse(StringIO.StringIO(html_str), parser)
    body_ele = tree.xpath('/html/body')[0] #'//p') #list of all <p>
    with codecs.open("output.txt", encoding='UTF-8', mode='w') as f:
        for i in body_ele.iter():
            ls = temp_txt_storage.get(i.tag.__repr__())
            if ls == None:
                ls = list()
                ls.append(i.text)
                ls.append(i.tail)
                temp_txt_storage[i.tag.__repr__()] = ls
            else:
                ls.append(i.text)
                ls.append(i.tail)
    return temp_txt_storage

def _generate_doc_obj(extracted_txt):
    for tag, txt_ls in extracted_txt.iteritems:
        for txt in txt_ls:
            if txt != None:
                token = tokenize(txt)

def _create_inverted_index():
    pass

def output_index(destination):
    pass


if __name__ == '__main__':
    load_scored_tag_name('text_tag_whitelist.json')
    web_doc_lib_path = './WEBPAGES_RAW'

    for root, directory, files in os.walk(web_doc_lib_path):
        if len(files) != 0:
            for f in files:
                file_path = (os.path.join(root,f))
                doc_ID = file_path[15:]
                raw_str = read_web_doc(file_path)
                generate_doc_obj(extract_txt_from_html(raw_str))
