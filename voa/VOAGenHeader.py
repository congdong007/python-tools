import os

header_path = os.getcwd() + r'\header'
print(header_path)

if not os.path.exists(header_path):
    os.makedirs(header_path)

header_path = header_path + r'\replheader.py'
    
if os.path.exists(header_path):
    os.remove(header_path)

if __name__ == "__main__":

    path = r'E:\voa'

    with open(header_path, mode='a') as filename:
        filename.write('dict_rep = [\n')
        files = os.walk(path)     
        for path1,dir_list,file_list in files:  
            for file_name in file_list:
                filename.write('\'{}\',\n'.format(file_name))               
                
        filename.write('None\n]\n')