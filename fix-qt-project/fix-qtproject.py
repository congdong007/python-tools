import os

from header.replheader import *


def repl(path):
    tmp_list = []
    try:
        f = open(path)              
        lines = f.readlines()      #读取全部内容 ，并以列表方式返回
        for line in lines:
            save_line = ''
            tmp_line = ''
            if '#include' in line:
                tmp_line = line.split(' ')
                tmp_str = tmp_line[1].replace('\n','')
                if '<' in tmp_str:
                    if tmp_str in dict_rep:
                        pt_str = '{}:{}'.format(tmp_str,dict_rep.get(tmp_str))
                        value = dict_rep.get(tmp_str)
                        print(pt_str)
                        #dict_rep.get(tmp_line[1])
                        tmp_str = "#include {}\n".format(value)
                        line = tmp_str        

            tmp_list.append(line)
        f.close() 

        os.remove(path) 

        with open(path, mode='a',encoding='utf-8') as filename:
            for line1 in tmp_list:
                filename.write(line1)   

    except FileNotFoundError:
        print('无法打开指定的文件!')
    except LookupError:
        print('指定了未知的编码!')
    except UnicodeDecodeError:
        print('读取文件时解码错误!')
    finally:
        if f:
            f.close()


if __name__ == "__main__":
    path = r'E:\111'
    files = os.walk(path)      
    for path1,dir_list,file_list in files:  
        for file_name in file_list:  
            if '.h' in file_name or '.cpp' in file_name:
                if 'qrc_' in file_name or 'ui_' in file_name or 'moc_' in file_name or '.html' in file_name:
                    pass
                else:
                    tmp_path = os.path.join(path1, file_name)
                    print(tmp_path)
                    repl(tmp_path)
            
            if '.sln' in file_name or '.suo' in file_name or '.vcproj' in file_name or '.vcxproj' in file_name :
                tmp_path = os.path.join(path1, file_name)
                print("delete this file :{}\n".format(tmp_path))
                os.remove(tmp_path)