import re
import logging

from tqdm import tqdm

class FuncRecord:

    def __init__(self, name, ret):
        self.name = name
        self.ret = ret


class SvClass:

    def __init__(self, name, parant=None, param=None):
        self.name = name
        self.parent = parant
        self.param = param
        self.members = []
        self.functions = []

    def addMem(self, member):
        self.members.append(member)

    def addFunc(self, func):
        self.functions.append(func)

    def getMemNum(self):
        return len(self.members)

    def getFuncNum(self):
        return len(self.functions)

    def printAllMem(self):
        print(self.members)

    def printAllFunc(self):
        print(self.functions)


if __name__ == "__main__":
    cls_mem = []
    in_class = 0
    for line in open("SvFile/Boy.sv"):
        if re.match(r'\s*//.*\n', line):
            pass
        elif re.match(r'\W*class\s*(?:extands)?(\w+);\s*\n', line):
            print('CLASS')
        elif re.match(r'\W*endclass.*\n',line):
            print('ENDCLASS')
        elif re.match(r'\W*function.*\n',line):
            print('FUNCTION')
        elif re.match(r'\W*endfunction.*\n',line):
            print('ENDFUNCTION')

        _list = line.split()
        if len(_list) > 0:
            if _list[0] == 'class':
                cls = SvClass(_list[1])
                in_class = 1
            elif _list[0] == 'endclass':
                cls_mem.append(cls)
                in_class = 0
            elif _list[0] == 'function':
                cls.addFunc(' '.join(str(i) for i in _list))
            elif _list[0] == 'endfunction':
                pass
            else:
                if in_class:
                    cls.addMem(' '.join(str(i) for i in _list))

    regex = re.match(r'class\s+(\w+)\s+(?:extands)?\s+(\w+)\s*;', "class A extands B ;")