# -*- coding: utf-8 -*-  
import os  
import time

def listdir_only_file(path):  #传入存储的list
    list_name = []
    for file in os.listdir(path):  
        file_path = os.path.join(path, file)  
        if os.path.isdir(file_path):  
            continue
        else:  
            list_name.append(file_path)
    return list_name


def get_article_id_and_title_and_content(path):
    # get content
    f = open(path)
    content = f.read()
    f.close()
    
    # get id
    rev_path = path[::-1]
    Id = rev_path.find('.')
    rev_path = rev_path[Id+1:]
    Id = rev_path.find('_')
    Id_2 = rev_path[:Id][::-1]

    # get title
    rev_path = rev_path[Id+1:]
    Id = rev_path.find('/')
    if Id == -1:
        title = rev_path[::-1]
    else:
        title = rev_path[:Id][::-1]

    return Id_2, title, content

ans = listdir_only_file("/home/articles/")
# print(ans)

# for item in ans:
#    time.sleep(0.1)
#    Id, title, content = get_article_id_and_title_and_content(item)
#    print(Id)
#    print(title)
#    print(content)
