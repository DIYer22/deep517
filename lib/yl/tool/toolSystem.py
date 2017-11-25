# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys, os, time

def importAllFunCode(mod=None):
    '''
    mod 为包名(type(mod)=='str')或包本身(type(mod)==module)
    自动生成导入所有模块语句 并过滤掉__name__等
    '''
    if mod is None:
        mod = 'yllab'
    if isinstance(mod,(str,unicode)):
        exec ('import %s as mod'%mod)

    names = [name for name in dir(mod) if not ((len(name)>2 and name[:2]=='__') or 
                                  name in ['unicode_literals',])]
    n = 5
    lines = []
    while len(names) > n:
        l,names = names[:n],names[n:]
        lines += [', '.join(l)]
    lines += [', '.join(names)]
    lines = ',\n          '.join(lines)
    
    strr = (("from %s import *\n    from %s import (%s)"%(mod.__name__,mod.__name__,lines)))
    strr = '''from %s import *
try:
    from %s import (%s)
except ImportError:
    pass'''%(mod.__name__,mod.__name__,lines)
    print strr

def crun(pycode, snakeviz=True):
    '''测试代码pycode的性能'''
    from cProfile import run
    if not snakeviz:
        return run(pycode,sort='time')
    run(pycode, "/tmp/snakeviz.result")
    os.system('snakeviz /tmp/snakeviz.result &')
    
    
def frun(pyFileName=None):
    '''在spyder中 测试pyFileName的性能'''
    if pyFileName:
        if '.py' not in pyFileName:
            pyFileName += '.py'
        crun("runfile('%s',wdir='.')"%pyFileName)
    else:
        crun("runfile(__file__,wdir='.')")

class timeit():
    '''
    记时 :
        >>> ti = timeit()
        # run your code
        >>> print ti()
    记时2 :
        >>> with timeit():
        >>>     fun()
        
    测试code时间 :
        >>> timeit(your_code)
    '''
    def __init__(self,code=''):
        self.begin = time.time()
        if len(code):
            exec code
            print self.s
    def __call__(self):
        '''返回时间差'''
        return time.time()-self.begin
    def __enter__(self):
        return self
    def __exit__(self, typee, value, traceback):
        self.p
    @property
    def s(self):
        t = time.time()-self.begin
        s='\x1b[36mspend time: %s\x1b[0m'%t
        return s
    @property
    def p(self):
        '''直接打印出来'''
        print self.s

def heatMap(pathOrCode):
    '''显示python代码的时间热力图
    ps.会让代码里面的中文全部失效
    
    Parameters
    ----------
    path : str of code or path of .py
        .py文件路径或着python代码
    '''
    from pyheat import PyHeat
    path = '/tmp/pyheat-tmp.py'
    code = pathOrCode
    try :
        if os.path.isfile(pathOrCode):
            path = pathOrCode+'_HEAT_MAP_TMP.py'
            with open(pathOrCode) as f:
                code = f.read()
        code = code.decode('ascii','replace').replace(u'\ufffd','$?')
        with open(path,'w') as f:
            f.write(code)
        ph = PyHeat(path)
        ph.create_heatmap()
        ph.show_heatmap()
    finally:
        if os.path.isfile(path):
            os.remove(path)
        
def strIsInt(s):
    '''判断字符串是不是整数型'''
    s = s.replace(' ','')
    return s.isdigit() or (s[0]==('-') and s[1:].isdigit())

def strIsFloat(s):
    '''判断字符串是不是浮点'''
    s = s.replace(' ','')
    return s.count('.')==1 and strIsInt(s.replace('.',''))
def strToNum(s):
    ''' 若字符串是float or int 是则返回 数字 否则返回本身'''
    if strIsInt(s):
        return int(s)
    if strIsFloat(s):
        return float(s)
    return s

def getArgvDic(argvTest=None):
    '''
    将cmd的`python main.py arg1 arg2 --k v --tag`形式的命令行参数转换为(list, dict)
    若v是数字 将自动转换为 int or float, --tag 将表示为 dic[tag]=True
    
    Return
    ----------
    l : list
        去除第一个参数 文件地址外的 第一个 '--'之前的所有参数
    dic : dict
        `--k v` 将以{k: v}形式存放在dic中
        `--tag` 将以{k: True}形式存放在dic中
    '''
    from toolLog import  pred
    argv = sys.argv
    if argvTest:
        argv = argvTest
    l = argv = map(strToNum,argv[1:])
    code = map(lambda x:(isinstance(x,(str,unicode)) 
        and len(x) >2 and x[:2]=='--'),argv)
    dic = {}
    if True in code:
        l = argv[:code.index(True)]
        n = len(code)
        for i,s in enumerate(code):
            x = argv[i]
            if int(s):
                k = x.replace('--','')
                if (i<=n-2 and code[i+1]) or i==n-1: # 不带参数
                    dic[k] = True
                else:  # 带参数
                    dic[k] = argv[i+1]
    if len(dic) or len(l):
        pred('command-line arguments are:\n  %s and %s'%(l,dic))
    return l,dic


def softInPath(softName):
    '''
    是否安装命令为softName的软件，即 判断softName 是否在环境变量里面
    '''
    for p in os.environ['PATH'].split(':'):
        if os.path.isdir(p) and softName in os.listdir(p):
            return True
    return False

def addPathToSys(_file_, pathToJoin='.'):
    '''
    将 join(__file__, pathToJoin)  加入 sys.path

    Parameters
    ----------
    _file_ : str
        .py 文件的路径 即__file__ 变量
    pathToJoin : str, default '.'
        相对路径
    '''
    from os.path import abspath,join,dirname
    apath = abspath(join(dirname(abspath(_file_)),pathToJoin))
    if apath not in sys.path:
        sys.path.append(apath)
    return apath
if __name__ == "__main__":

    pass