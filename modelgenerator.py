import os

class ModelGenerator(object):
    def __init__(self):
        "docstring"
        self.class_name = ''
        self.vars=[]
        self.defs=[]
        self.generated = ''

    def gen_class_string(self, class_name):
        self.class_name = class_name + '_model'
        self.generated += '''class {0}(object):\n'''.format(self.class_name)  

    def gen_init_string(self):
        self.gen_def_string('__init__')
        
    def gen_def_string(self, func_name):
        self.defs.append(func_name)
        self.generated += '''\tdef {0}(self):\n'''.format(func_name)  
    
    def gen_self_var(self, var):
        self.vars.append(var)
        self.generated += '''\t\tself.{0} = None\n'''.format(var)

    def write_to_file(self, dest):
        full_dest = os.path.join(os.getcwd(),dest)
        if not os.path.exists(full_dest):
            os.makedirs(full_dest)

        filename = os.path.join(full_dest, self.class_name +'.py')
        print("Writing to:", filename)
        with open(filename, 'w+') as f:
            f.write(self.generated)
