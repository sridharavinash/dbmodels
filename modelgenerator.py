import os
import collections

class ModelGenerator(object):
    def __init__(self):
        self.class_name = ''
        self.vars={}
        self.defs={}
        self.generated = ''
        self.primary_key= ''
        self.imports={}

    def _parse_keywordarg(self, **kwargs):
        self.class_name = kwargs.get('class_name')
        self.imports = kwargs.get('imports')
        self.vars = kwargs.get('vars')
        defs = kwargs.get('defs')
        self.defs = collections.OrderedDict(sorted(defs.items()))
        self.primary_key = kwargs.get('primary_key')
        
    def generate(self, **kwargs):
        self._parse_keywordarg(**kwargs)
        self.gen_import_string()
        self.generated += '\n'
        self.gen_class_string()
        for d in self.defs:
            self.gen_def_string(d ,self.defs[d]['args'])
            if d == '__init__':
                self.gen_self_var()
            else:
                if self.defs[d]['body']:
                    self.generated += self.defs[d]['body']
            self.generated += '\n'

        self.write_to_file(kwargs.get('dest'))

    def gen_import_string(self):
        for i in self.imports:
            if not self.imports[i]:
                self.generated += '''import {0}\n'''.format(i)
            else:
                self.generated += '''from {0} import {1}\n'''.format(i,self.imports[i])
        
    def gen_class_string(self):
        self.generated += '''class {0}(object):\n'''.format(self.class_name)  
        
    def gen_def_string(self, f_name, f_args=''):
        if not f_args:
            self.generated += '''\tdef {0}(self{1}):\n'''.format(f_name,f_args)
        else:
            f_args = ','.join(x for x in f_args.split(','))
            self.generated += '''\tdef {0}(self, {1}):\n'''.format(f_name,f_args)
    
    def gen_self_var(self):
        for v in self.vars:
            self.generated += '''\t\tself.{0} = {1}\n'''.format(v,self.vars[v])

    def write_to_file(self, dest):
        full_dest = os.path.join(os.getcwd(),dest)
        if not os.path.exists(full_dest):
            os.makedirs(full_dest)

        filename = os.path.join(full_dest, self.class_name +'.py')
        print("Writing to:", filename)
        with open(filename, 'w+') as f:
            f.write(self.generated)
