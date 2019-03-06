
class doc_struct:
    def __init__(self, docID):
        self.docID = docID
        self.tok_dic = dict() #{tok:{tag:freq}}

    def add_tok(self, tok, tag):
        if tok in self.tok_dic:
            val = self.tok_dic[tok]
            if tag in val:
                val[tag] += 1
            else:
                val[tag] = 1
        else:
            self.tok_dic[tok] = {tag:1}

    def get_freq(self, tok, tag=None):
        try:
            if tag != None:
                return (self.tok_dic[tok])[tag]
            else:
                sum = 0
                val = self.tok_dic[tok]
                for tag in val:
                    sum += val[tag]
                return sum
        except KeyError as e:
            return 0

    def __repr__(self):
        output = 'docID=%s, toks=%s' % (self.docID, self.tok_dic.__repr__())
        return output

def _test():
    testobj = doc_struct('1234/10')
    testobj.add_tok('testtok1', 'h1')
    testobj.add_tok('testtok1', 'p')
    testobj.add_tok('testtok1', 'p')
    testobj.add_tok('lecture', 'strong')
    print(testobj)
    print(testobj.get_freq('testtok1'))
    print(testobj.get_freq('lecture', 'strong'))
    print(testobj.get_freq('asbc', ''))

if __name__ == '__main__':
    _test()
