
import os
import json


data_dir = os.path.join('mysite','static\\balloon\\data\\')
print(data_dir)
file_name = os.path.join(data_dir, 'map_table')

Dict= {}

with open(file_name+'.txt','r') as ff:
    Id = 1
    for line in ff:
        Dict[line[0:-1]] = Id
        Id+=1

with open(file_name+'.json', 'w') as f:
    json.dump(Dict, f)
