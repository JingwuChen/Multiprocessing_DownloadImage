#coding=utf-8
import requests
import re
import os
import time
import random
import threading
import multiprocessing
#定义头文件
headers={'Accept-Language':'zh-CN,zh;q=0.8','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36','Cookie':'remember=0; DIDA642a4585eb3d6e32fdaa37b44468fb6c=lv2id4n8sdpldu4b8r84s9q9m0; time=MTEzNTI2LjIxNjM0Mi4xMDI4MTYuMTA3MTAwLjExMTM4NC4yMDc3NzQuMTE5OTUyLjExMTM4NC4xMDQ5NTguMTExMzg0LjExNzgxMC4xMTk5NTIuMTE1NjY4LjEwMjgxNi4xMTEzODQuMTE3ODEwLjExNzgxMC4xMDI4MTYuMA%3D%3D; \
Hm_lvt_e71d0b417f75981e161a94970becbb1b=1477797693,1478598212,1478598271; Hm_lpvt_e71d0b417f75981e161a94970becbb1b=1478604796'}

# Lock=threading.Lock()#获取线程锁
def get_url(start, end):
    "获取多页链接"
    urls = []
    for i in range(start, end):
        urls.append('http://58921.com/alltime?page={}'.format(str(i)))
    return urls
picpath = 'D:\\Box_ImageDownload'  # 下载到的本地目录
if not os.path.exists(picpath):  # 路径不存在时创建一个
    os.makedirs(picpath)
def get_content(url):
    "获取每一个网页的内容"
    web_data=requests.get(url,headers=headers)
    find_title = r'<td><a href="/film/\d+".*?>(.*?)</a></td>'
    find_rank=r'<td>(\d+?)</td>'
    find_image=r'<img src="(http://.*?\.png)"'
    titles=re.findall(find_title,web_data.content,re.S|re.M)
    rank=re.findall(find_rank,web_data.content,re.S|re.M)
    year_rank=[]
    history_rank=[]
    if len(rank) % 3:
        for i in range(2, len(rank), 3):
            if re.match(r'\d{4}', rank[i]):
                pass
            else:
                del rank[i]
    for i in range(0,len(rank),3):
        year_rank.append(rank[i])
        history_rank.append(rank[i+1])
    images_link=re.findall(find_image,web_data.content,re.S|re.M)
    content={'titles':titles,'year_rank':year_rank,'history_rank':history_rank,'images_link':images_link}
    return content
def save_Image(url):
    "下载文件函数"
    content=get_content(url)
    for index, imgurl in enumerate(content['images_link']):
        time.sleep(random.random()*8)
        r=requests.get(imgurl,stream=True)
        target = picpath + '\\%s-%s.png' % (content['history_rank'][index],unicode(content['titles'][index],'utf-8'))
        with open(target,'wb') as png:
            png.write(r.content)
            png.flush()

def DownloadMultiThread(end):
    ts=time.time()
    task_threads = []  # 存储线程
    for url in get_url(90, end):
        t=threading.Thread(target=save_Image,args=(url,))
        task_threads.append(t)
    for task in task_threads:
        task.start()#启动线程
        task.join()#阻塞主进程
    print 'it takes %s seconds' % (time.time() - ts)
def DownloadMultiprocessing(end):
    pool = multiprocessing.Pool(processes=20)#使用Pool方法，创建进程池，有个非常牛叉的电脑，32个核心
    for url in get_url(90, end):
        pool.apply_async(save_Image,(url,))#这里使用的是apply_async，多个进程异步执行；如果调用apply，就变成阻塞版本了。 
    pool.close()
    pool.join()

if __name__=='__main__':
    ts = time.time()
    DownloadMultiprocessing(127)
    print 'it takes %s seconds' % (time.time() - ts)
    print 'Search Over'