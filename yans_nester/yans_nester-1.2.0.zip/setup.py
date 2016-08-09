from distutils.core import setup #从python发布工具导入setup函数

setup(
        name           = 'yans_nester',
        version        = '1.2.0',
        py_modules     =['nester'],   #将模块元数据与setup函数的参数关联

        #以下是一些元数据，可以修改
        author         ='rc',
        author_email   ='runcihuang@gmail.com',
        url            ='http://www.headfirstlabs.com',
        description    ='A simple printer of nested lists',
      )
