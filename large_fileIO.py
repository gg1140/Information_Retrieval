import codecs

class chunk_file_read:
    def __init__(self, file_name=None, word_sep=None, whitelist=True, chunk_Size=10000):
        self.file_name = file_name
        self._file_obj = None
        self.chunk_size = chunk_size
        self._buf = []
        self._offset = None

    def __iter__(self):
        return self

    def __next__(self):

    def open(file_name, encode='UTF-8'):
        self._file_obj = codecs.open(file_name, encoding=encode, mode='r', errors='ignore')

    def _chunk_read(file_obj, output, chunk_size=10000):
        """
        Open input file
        Read in a chunk from the file, each chunk is 10Kb as default
        Retain the last word and determine if it is a standalone word according to the next chunk
        Call on tokenizer() to properly remove all illegal characters

        Complexity: Worst Case would be O(n), where n = 1 byte
        """
        #with codecs.open(file_name, encoding='UTF-8', mode='r', errors='ignore') as input_file:
        buf = u''
        start_index = 0
        last_ws_index = 0

        for chunk in iter(lambda:file_obj.read(chunk_size), u''):
            chunk = buf.join(chunk) #   Combining reminder & empty previous buf
            buf = u''           #   put the last whitespace seperated string of characters to the buffer ...
                                #   ... to make sure it is a complete word
            last_ws_index = find_last_ws(chunk)
            if last_ws_index >= 0: #    pass the chunk with complete whitespace seperated words to the tokenizer
                buf = chunk[last_ws_index:]
                wl_tokenizer(chunk, tok_filter, start_pos=0, end_pos=last_ws_index)
            else: # chunk is a continous string with no whitespace, but may require the next chunk to form a complete word
                buf = chunk
        if not len(buf) == 0: # meaning the reminder chunk is a complete word with no whitespace
                #tokenizer(buf, last_ws_index, len(buf),tok_filter, dic)
                wl_tokenizer(buf, tok_filter, start_pos=last_ws_index)

    def __del__(self):
        if self._file_obj != None:
            self._file_obj.close()
