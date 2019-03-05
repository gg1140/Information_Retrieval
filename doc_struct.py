
class doc_struct:
    def __init__(self, docID, tag_dic):
        self.docID = docID
        self.tok_dic = dict() #tok:[freq,tag_code]
        self.tag_dic = tag_dic

    def add_tok(tok, tag):
        if tok in self.tok_dic:
            val = self.tok_dic[tok]
            val[0] += 1
            val[1] 
        else:
        self.tok_dic[tok] = [1, self.tag_dic[tag]]

    def __repr__(self):
        output = 'docID=%s::[' % self.docID
        for key, val in self.tok_dic.iteritems():
            output += ', %s=%s' % (key.__repr__(), val.__repr())
        return output + ']'
