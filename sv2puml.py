import re

class Vector:
    def __init__(self, name = '', init_item = []):
        self.name = name
        self.vector = init_item

    def get_name(self):
        return self.name

    def front(self):
        assert self.size() > 0
        return self.vector[0]

    def back(self):
        assert self.size() > 0
        return self.vector[-1]

    def print(self):
        print(self.vector)

    def size(self):
        return len(self.vector)

    def get(self, index):
        assert self.size() > 0
        return self.vector[index]

    def pop_front(self):
        return self.vector.pop(0)

    def pop_back(self):
        return self.vector.pop(-1)

    def push_front(self, item):
        if type(item) == type([]):
            self.vector.insert(item[:])
        else:
            self.vector.insert(item)

    def push_back(self, item):
        if type(item) == type([]):
            self.vector.extend(item[:])
        else:
            self.vector.append(item)

    def clear(self):
        while self.size():
            self.pop_front()

    def iter(self):
        return self.vector


class Queue(Vector):
    def __init__(self, name = '', init_item = []):
        super(Queue, self).__init__(name, init_item)

    def push(self, item):
        self.push_back(item)

    def pop(self):
        return self.pop_front()

    def reuse(self, item):
        self.clear()
        self.push(item)


class Stack(Vector):

    def __init__(self, name = '', init_item = []):
        super(Stack, self).__init__(name, init_item)

    def push(self, item):
        return self.push_back(item)

    def pop(self):
        return self.pop_back()

    def reuse(self, item):
        self.clear()
        self.push(item)


class SvClass:

    def __init__(self, name, virtual = False, parant=None, param=None):
        print('[SvClass::__init__]',f'name : {name}')
        self.name = name
        self.parent = parant
        self.param = param
        self.virtual = virtual
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

    def print(self):
        print('[SvClass::print]\n', f'\tname: {self.name}\n\tvirtual: {self.virtual}, parant: {self.parent}')

class SvFnTsk:

    def __init__(self, name, field = None, virtual = False, static= False, visibility = 'public'):
        self.name = name
        self.field_type = field.getType()
        self.field_name = field.getName()
        self.virtual = virtual
        self.static = static
        self.visibility = visibility

    def print(self):
        print('[SvFnTsk::print]\n', f'\tname: {self.name} field_type: {self.field_type} field_name: {self.field_name}\n'
                                    f'\tvirtual: {self.virtual}, visibility: {self.visibility}, static: {self.static}')


def pre_proc(fp):
    line_q = Queue('line_stack')
    for line in fp:
        # 清除注释段、空白行、换行符
        # 清除换行符是为了适配sv的语句可能分布在多行的影响
        _line = re.sub(r'(?://.*)|(?:^\s*\n)|\n', '', line)
        if _line != '':
            if   re.match(r'\s*endpackage\s*', _line):
                _line += ' ~END-PACKAGE~'
            elif re.match(r'\s*endclass\s*', _line):
                _line += ' ~END-CLASS~'
            elif re.match(r'\s*endfunction\s*', _line):
                _line += ' ~END-FUNC~'
            line_q.push(_line)
        # TODO : process /**/ statment
        # TODO : process `define muiltipul line situation
    # line_q.print()
    file = ''.join([str(i) for i in line_q.iter()])

    # 重定义有效代码段分割行标准
    lines = re.split(';|(?:~END-PACKAGE~)|(?:~END-CLASS~)|(?:~END-FUNC~)', file)
    # file = '\n'.join([str(i) for i in lines])
    # print('[file]\n', file)
    return lines

class CodeField(Stack):
    def __init__(self):
        super(CodeField, self).__init__('', [('GLOBAL', 'top')])

    def getType(self):
        return self.back()[0]

    def getName(self):
        return self.back()[1]

    def isGlobal(self):
        return self.getType() == 'GLOBAL'

    def isPackage(self):
        return self.getType() == 'PACKAGE'

    def isClass(self):
        return self.getType() == 'CLASS'

    def isFnTsk(self):
        return self.getType() == 'FNTSK'

    def push(self, item):
        assert type(item) == type(())
        assert len(item) == 2
        super(CodeField, self).push(item)

cls_pat1 = re.compile(r'^\s*((?:virtual))?\s*class\s+(\w+)\s*$')
cls_pat2 = re.compile(r'^\s*((?:virtual))?\s*class\s+(\w+)\s+extands\s+(\w+)\s*$')
cls_end = re.compile(r'^\s*endclass.*$')

def createSvClass(line):
    tmp = cls_pat1.match(line)
    # print('11111111111111111')
    if tmp:
        # print('22222222222222222')
        if tmp.lastindex == 1 :
            return SvClass(tmp.group(1),False,None,None)
        elif tmp.lastindex == 2:
            return SvClass(tmp.group(2),True,None,None)

    # print('33333333333333333', line)
    tmp = cls_pat2.match(line)
    if tmp:
        # print('44444444444444444')
        if tmp.lastindex == 2 :
            # print('55555555555555555',tmp.group(1), tmp.group(2), tmp.group(3))
            return SvClass(tmp.group(1),False,tmp.group(2),None)
        elif tmp.lastindex == 3:
            # print('66666666666666666')
            return SvClass(tmp.group(2),True,tmp.group(2),None)

    return None

ft_start = re.compile(r'^(.*)((?:(?:function)|(?:task)).*)$')
ft_end = re.compile(r'^\s*((?:(?:endfunction)|(?:endtask)).*)$')

def createSvFnTsk(line, field):
    # TODO: use static function in SvFnTsk
    is_start = ft_start.match(line)

    # print('[createSvFnTsk]', line)

    # def __init__(self, name, field=None, virtual=False, is_static=False, visibility='public'):
    if is_start:
        if is_start.lastindex == 2:
            # print('[createSvFnTsk]', line, is_start.group(1), is_start.group(2))
            is_virtual = re.match(r'.*virtual.*', is_start.group(1))
            is_static = re.match(r'.*static.*', is_start.group(1))
            visibility = re.match(r'.*((?:protected)|(?:local)).*', is_start.group(1))
            return SvFnTsk(is_start.group(2),
                           field,
                           False if is_virtual == None else True,
                           False if is_static == None else True,
                           'public' if visibility == None else visibility.group(1) )
        else :
            # TODO : bug
            return SvFnTsk(exist.group(1), field, False, False, False)

    return None


if __name__ == "__main__":
    cls_mem = []
    field = CodeField()
    fp = open("SvFile/Boy.sv")
    lines = pre_proc(fp)

    # add \n to view file and debug
    print('[view file before process]\n','\n'.join([str(i) for i in lines]))

    for line in lines:
        # print('--------------', line, field.getName())
        if field.isGlobal():
            sv_class = createSvClass(line)
            if sv_class:
                sv_class.print()
                field.push(('CLASS', sv_class.name))
        elif field.isPackage():
            pass
        elif field.isClass():
            is_end = cls_end.match(line)
            if is_end:
                field.pop()
                continue
            sv_fntsk = createSvFnTsk(line, field)
            if sv_fntsk:
                sv_fntsk.print()
                field.push(('FNTSK', sv_fntsk.name))
        elif field.isFnTsk():
            is_end = ft_end.match(line)
            if is_end:
                field.pop()
                # print('POP OUT', field.getType(), field.getName())

# TODO : break to class!!!