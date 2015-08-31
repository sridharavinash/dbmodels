class ModelGenerator(object):
    def __init__(self):
        "docstring"
        self.class_name = ''
        self.vars=[]
        self.defs=[]
        self.generated = ''

    def gen_class_string(self, class_name):
        self.class_name = class_name + '_model'
        self.generated += '''class {0}l(object):\n'''.format(self.class_name)  

    def gen_def_string(self, func_name):
        self.defs.append(func_name)
        self.generated += '''\tdef {0}(self):\n'''.format(func_name)  
    
    def gen_self_var(self, var):
        self.vars.append(var)
        self.generated += '''\t\tself.{0} = None\n'''.format(var)

    def write_to_file(self):
        filename = self.class_name+'.py'
        with open(filename, 'w+') as f:
            f.write(self.generated)
