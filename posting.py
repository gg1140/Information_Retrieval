import StringIO

class posting:
    def __init__(self, tok=0, **kwargs):
        self.tok = tok
        self.extra_field = kwargs

    def add_field(self, key, val):
        if key not in self.extra_field:
            self.extra_field[key] = val
            return True
        else:
            return False

    def set_field(self, key, val):
        if key in self.extra_field:
            self.extra_field[key] = val
            return True
        else:
            return False

    def get_field(self, key):
        if key in self.extra_field:
            return self.extra_field[key]
        else:
            return None

    def __repr__(self):
        output = '[tok=%s' % self.tok
        for key, val in self.extra_field.iteritems():
            output += ', %s=%s' % (key.__repr__(), val.__repr__())
        return output + ']'

def test():
    testobj1 = posting('tok1', freq=10, grade=1)
    testobj2 = posting('tok2', freq=10, grade=1, anotherattr='h1')
    testobj3 = posting('tok3')
    print(testobj1)
    print(testobj2)
    print(testobj3)
    print(testobj3.get_field('freq'))
    print(testobj2.get_field('anotherattr'))
    print(testobj2.set_field('anotherattr', 1140))
    print(testobj2.set_field('anotherattir', 1140))
    print(testobj2.get_field('anotherattr'))

if __name__ == '__main__':
    test()
