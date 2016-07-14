"""
作者 金玺曾

How to use it?
Just copy this file to where you want, and modify the codes as you wish.
"""

if __name__ == '__main__':
    import sys
    import shutil
    import glob
    import os
    from datapacker import excel2class, excel2data

    CS_NAMESCAPE = 'ExampleGameDB'  # cs 类的名称域，在Unity中使用，为空也可
    GAMEINFO = 'GameInfo' # 配置类名称(所有配置类对象都集中存放在这个类中), Json文件也使用这个名称，只是后缀不同

    PASSWORD = '123456'  # 密码
    SUFFIX = '.txt'  # 后缀

    # 生成代码的临时目录
    DIST_PATH = 'dist'

    # 存放Unity脚本的目录名称, 如果为空，将不会生成.cs文件
    # 因为默认生成的脚本存放在 当前目录/dist/，所以至少需要返回2级目录
    UNITY_PATH = '../../UnityProjectName/Assets/Scripts/GameInfo'

    # 存放py脚本的路径，如果为空，将不会生成.py文件
    # 因为默认生成的脚本存放在 当前目录/dist/，所以至少需要返回2级目录
    PY_PATH = '../../ServerProjectName/ntserver/GameInfo'
    
    TEST = True  # 测试模式, 实际使用时设为False，测试模式将不会copy脚本

    # 实际运行的代码
    # 一般来说，下面的代码没必要修改，只需要配置上方的名称和目录位置即可
    curpath = __file__
    curpath = curpath.rpartition('\\')
    curpath = curpath[0]
    os.chdir(curpath)

    curpath = os.path.abspath(os.getcwd())
    print('curdir:', curpath)

    if not os.path.exists ( DIST_PATH ):
        os.mkdir(DIST_PATH)
    
    # create cs classes
    e2c = excel2class.Excel2Class(output_path = DIST_PATH + '/')
    if UNITY_PATH:
        e2c.make(namespace=CS_NAMESCAPE, gameinfoclass=GAMEINFO)
    if PY_PATH:
        e2c.make(namespace='', gameinfoclass=GAMEINFO, lang=excel2class.Excel2Class.LANG_PY)

    # create JSON
    e2d = excel2data.Excel2Data(output_path = DIST_PATH + '/')
    e2d.password = PASSWORD
    e2d.suffix = SUFFIX
    e2d.make_json(filename=GAMEINFO)

    os.chdir(DIST_PATH)

    # COPY FILES
    print()
    print()
    # copy cs file to unity
    if UNITY_PATH:
        csfiles = glob.glob('*.cs')
        for cs in csfiles:
            unitypath = '{0}/{1}'.format(UNITY_PATH,cs)
            if not TEST:
                shutil.copyfile(cs, unitypath)
            print("copy *.cs to: ", unitypath)


    # copy py file to pyserver
    if PY_PATH:
        pyfiles = glob.glob('*.py')
        for py in pyfiles:
            pypath = '{0}/{1}'.format(PY_PATH,py)
            if not TEST:
                shutil.copyfile(py, pypath)
            print("copy *.py to: ", pypath)


    # copy JSON  to dist
    patter = '*' + SUFFIX
    binfiles = glob.glob(patter)
    for binf in binfiles:
        outputf = binf.rpartition('.')
        outputf = outputf[0]
        unitypath = '{0}/{1}{2}'.format(UNITY_PATH, outputf, SUFFIX)
        pypath = '{0}/{1}{2}'.format(PY_PATH, outputf, SUFFIX)
        if not TEST:
            if UNITY_PATH:
                shutil.copyfile(binf, unitypath)  # JSON file, path
                print('copy ', binf, ' to ', unitypath)
            elif PY_PATH:
                shutil.copyfile(binf, pypath)  # JSON file, path
                print('copy ', binf, ' to ', pypath)

    print("press any key to exit!")
    input()



