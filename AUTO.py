import requests
import bs4
import re
import pathlib
from PIL import Image
import time
file_=""
def creat_wjj(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)

def get_html():
    song_name=input("输入你想要查找的歌曲")
    url="https://www.tan8.com/search-2-1-0.php?keyword="+song_name
    head={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    resp=requests.get(url=url,headers=head)
    html=resp.text
    resp.close()
    return html

def get_href():
    html=get_html()
    soup=bs4.BeautifulSoup(html,"html.parser")
    all_ul=soup.find_all('ul',attrs={'class':"yuepuClassify_list_0422"})
    rule = re.compile(r'<a href="(?P<href>.*?)".*?<li>.*?<h3 class="title_color">.*?</i>(?P<name>.*?)<.*?</h3>.*?</a>',re.S)
    rew = rule.finditer(str(all_ul))
    dic={}
    num=1
    for link in rew:
        str_num=str(num)
        dic[str_num+link.group('name').strip()]=link.group('href').strip()
        num=num+1

    if num==1:
        return None
    else:
        return dic

def chose_obj():
    dic=get_href()
    global file_
    if dic==None:
        return None
    for key in dic:
        print(key)
    num=input("请输入你要的版本")
    for key in dic:
        if num in key:
            file_=key.replace(num,"")
            return dic[key]

def start():
    host="https://www.tan8.com"
    strs=chose_obj()
    if strs==None:
        print("未找到歌曲")
        return None
    url=host+strs
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    resp=requests.get(url=url,headers=head)
    html=resp.text
    resp.close()
    soup=bs4.BeautifulSoup(html,"html.parser")
    all_script=soup.find_all('script')
    rule=re.compile(r'.*?<!---->.*?:\[(?P<lr>.*?)].*?<!---->',re.S)
    rew=rule.finditer(str(all_script))
    list1=[]
    global file_
    file_path="E:\\重要文件\\·𝕲𝖀𝕴𝕿𝕬𝕽·\\谱子\\原版曲"+'\\'+file_
    creat_wjj(file_path)
    file_oder=1
    for script in rew:
        list1=script.group('lr').split(',')
    for lis in list1:
        url1=lis.replace('\\',"").replace('\"',"")
        pz_get(url1,file_path,str(file_oder)+'.png')
        file_oder=file_oder+1

def pz_get(url1,path,name):
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }
    resp=requests.get(url=url1,headers=head)
    with open(path+'\\'+name, 'wb') as f:
        f.write(resp.content)
    img=Image.open(path+'\\'+name)
    if img.mode == 'P':
        img = img.convert('RGBA')
    background = Image.new("RGB", img.size, (255, 255, 255))
    background.paste(img, mask=img.split()[3])  # 使用 alpha 通道进行粘贴
    background.save(path+'\\'+name,'JPEG')
    resp.close()

if __name__=="__main__":
    num=int(input("模式1:一次，模式2:多次"))
    if num==1:
        start()
    elif num==2:
        while True:
            start()
            time.sleep(1)
    else:
        print("没有该模式")