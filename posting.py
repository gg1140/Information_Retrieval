import StringIO

class posting:
    def __init__(self, docID, freq, idf, score):
        self.docID = docID
        self.freq = freq
        self.idf = idf
        self.score = score

    def __repr__(self):
        output = '(docID=%s,freq=%d,idf=%.2f,score=%.2f)' % (self.docID, self.freq, self.idf, self.score)
        return output

def _test():
    testobj = posting('10/115', 18, 0.13, 10)
    print(testobj)

if __name__ == '__main__':
    _test()
