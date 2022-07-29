# @Time :  2022-7-28 10:45:49
# @Author : YFen4nt0ren
# @Software : PyCharm
import sys

import requests
import re
import time
import os
#https://tvax1.sinaimg.cn/wap800/007YLcQ6ly1h4cohy1d2vj31hc0u0jw3   F
#https://tvax4.sinaimg.cn/large/007YLcQ6ly1h4cohy1d2vj31hc0u0jw3    T

#bing serlvet地址
BING_IMGURL = "https://www.todaybing.com/web/api"
#bing 地址
BING_URL = "https://www.todaybing.com/"
#原始图片地址
IMGURL = "https://tvax4.sinaimg.cn/large/"

#安装路径
imgDownlaodFilePath = "C:\\images\\"

HEARDES = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "referer": BING_URL,
}



def downloadImg(paged = 5):
            sum = 0  
            title = ""
            img_titles = []

            for  i in range(1,paged):


                params = {
                    "append": "list-home",
                    "paged": i,
                    "action": "ajax_load_posts"
                }
                
                result_JsonData = requests.post(url=BING_IMGURL,headers=HEARDES,params=params)
                if result_JsonData.status_code == 200 :

                    result_Data=result_JsonData.json()['data'] 
                    #去除转换符
                    result_handelData = re.compile(r"\\").sub("",result_Data)

                    #print(result_handelData)
                    #获取所有图片名称   
                    titles = re.compile('title="(.*?)"').findall(result_handelData)
                    #获取所有图片链接
                    urls = re.compile('style="background-image: url\(https://tvax1.sinaimg.cn/wap800/(.*?)\)"').findall(result_handelData)


                    #将重复title及点个赞呗 去除
                    for i in titles :
                        if i != "点个赞呗" and i != title: 
                            title = i
                            img_titles.append(title) 

                    for i in range(0, 7):
                        imgData = requests.get(url=IMGURL+urls[i], headers=HEARDES)
                        if imgData.status_code == 200:
                            #下载
                            if not os.path.exists(f"{imgDownlaodFilePath}{img_titles[i]}.jpg"):
                                with open(f"{imgDownlaodFilePath}{img_titles[i]}.jpg", "wb") as f:
                                    print(f"正在下载{img_titles[i]}", end="")
                                    f.write(imgData.content)
                                    print("=====下载完成=====")
                                    sum = sum+1
                            else:
                                print(f"{imgDownlaodFilePath}{img_titles[i]}.jpg #当前文件已存在")
                        else:
                            print("无法完成下载,图片错误代码:",imgData.status_code)
                            time.sleep(5)
                            sys.exit()
                        imgData.close()
                    img_titles.clear()
                else :
                    print("无法完成下载,数据错误代码:", result_JsonData.status_code)
                    time.sleep(5)
                    sys.exit()
                    #print(img_titles)
                result_JsonData.close()
            print("共完成下载:",sum)


if __name__ == '__main__':
    if not os.path.exists(imgDownlaodFilePath):  # 是否存在这个文件夹
        print("未发现文件夹 正在创建文件夹",end="")
        os.makedirs(imgDownlaodFilePath)  # 如果没有这个文件夹，那就创建一个
        print(f"####文件夹{imgDownlaodFilePath}创建成功!")
    downloadImg(5)# 下载页数
