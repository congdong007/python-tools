import os

header_path = os.getcwd() + r'\header'

if not os.path.exists(header_path):
    os.makedirs(header_path)

header_path = header_path + r'\replheader.py'
    
if os.path.exists(header_path):
    os.remove(header_path)

if __name__ == "__main__":

    path = r'D:\Qt\Qt5.14.2\5.14.2\msvc2017_64\include'

    with open(header_path, mode='a') as filename:
        filename.write('dict_rep = {\n')
        files = os.walk(path)     
        for path1,dir_list,file_list in files:  
            for file_name in file_list: 
                tmp = os.path.join(path1, file_name)
#                print(tmp)
                if '.h' not in tmp:
                    tmp_path = path + '\\'
                    tmp = tmp.replace(tmp_path,r'<')+r'>'
                    tmp = tmp.replace('\\','/')
                    print(tmp)
                    str1 = '\'<{}>\' : \'{}\','.format(file_name,tmp)
                    filename.write(str1+'\n')
        filename.write('None:None\n}\n')