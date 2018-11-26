import random
import hashlib
import pandas as pd
import copy
def createPhone(n):
    prelist=["130","131","132","138","139","147","158","159","187","188"]
    x = random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
    lis = []
    for j in range(n):
        x = random.choice(prelist)+"".join(random.choice("0123456789") for i in range(8))
        lis.append(x)        
    return lis

def createName(n):
    a1=['张','金','李','王','赵','钱']
    a2=['玉','明','龙','芳','军','玲','建']
    a3=['','立','玲','明','国','']
    lis = []
    for i in range(n):
        name=random.choice(a1)+random.choice(a2)+random.choice(a3)
        lis.append(name)       
    return lis

def createAge(n):
    lis = []
    for j in range(n):
        x = random.choice(range(15,60))
        lis.append(x)
    return lis
  
def createGender(n):
    lis = []
    for j in range(n):
        x = random.choice(['F','M'])
        lis.append(x)
    return lis



cus = pd.DataFrame({'phone':createPhone(10),'name':createName(10),'age':createAge(10),'gender':createGender(10)})


def MD5(code):
    md = hashlib.md5()
    md.update(code.encode(encoding='utf-8'))
    return md.hexdigest()
    

New_cus = copy.deepcopy(cus)
New_cus['phone'] = New_cus['phone'].apply(lambda x:MD5(x))
New_cus['name'] = New_cus['name'].apply(lambda x:MD5(x))
