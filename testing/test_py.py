from StringIO import StringIO
import codecs

def test_funct(file_obj):
    print("test_funct", type(file_obj))
#    print(file_obj.getvalue())
    for line in file_obj:
        print(line)
    #for chunk in iter(lambda:file_obj.read(10000), u''):
    #    print(chunk)

if __name__ == '__main__':
    file_obj = StringIO()
    f = codecs.open('inputfile1.txt', encoding='UTF-8', mode='r', errors='ignore')
    for l in f:
        print(l)
        file_obj.write(l)
#    print(file_obj.getvalue())
    file_obj.seek(0)
    print(type(file_obj))
    #test_funct(file_obj)
    print(file_obj.read())
