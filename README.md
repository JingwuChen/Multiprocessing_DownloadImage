# Multiprocessing_DownloadImage
由于之前电影分析，需要获取上千部电影的票房数据，而电影票房这个网址的票房是图片，所以需要先下载下来然后进行图像识别。为了加快速度当然选择线程或进程来下载。所以这里介绍python多线程和多进程下载方法。
## 1.爬虫下载文件方法
爬虫下载图片的方法比较简单，使用`open`函数即可，代码如下
```python
r=requests.get(imgurl,stream=True)
        #设置存储路径target
        target = picpath + '\\%s-%s.png' % (content['history_rank'][index],unicode(content['titles'][index],'utf-8'))
        with open(target,'wb') as png:
            png.write(r.content)
            png.flush()
```
注意requests最好设置`stream`为`True`,因为默认情况下，当你进行网络请求后，响应体会立即被下载。你可以通过 stream 参数覆盖这个行为，推迟下载响应体直到访问 Response.content 属性，最后最好用flush一下，这样基本保障下载是完整。

## 2.使用多线程
python threading模块可以创建多个线程，不过由于GIL锁的存在，Python在多线程里面其实是快速切换。详情可参考[这篇博文](https://www.cnblogs.com/tkqasn/p/5700281.html)
使用threading模块创建线程，有两种方法可以重写Thread类，也可以直接用Thread方法：
```python
threading.Thread(group=None, target=None, name=None, args=(), kwargs={})
```
target传入函数，后面跟上函数的需要参数即可
```python
task_threads = []  # 存储线程
    for url in get_url(90, end):
        t=threading.Thread(target=save_Image,args=(url,))
        task_threads.append(t)
    for task in task_threads:
        task.start()#启动线程
        task.join()#阻塞主进程
```

### 3.使用多进程
由于GIL（全局解释锁）的问题，python多线程并不能充分利用多核处理器。如果想要充分地使用多核CPU的资源，在python中大部分情况需要使用多进程。`multiprocessing`可以给每个进程赋予单独的Python解释器，这样就规避了全局解释锁所带来的问题。
设计多任务时最好用`multiprocessing`的进程池`Pool`方法，非常简单，函数解释如下:
* apply_async(func[, args[, kwds[, callback]]]) 它是非阻塞，apply(func[, args[, kwds]])是阻塞的
* close()    关闭pool，使其不在接受新的任务。
* terminate()    结束工作进程，不在处理未完成的任务。
* join()    主进程阻塞，等待子进程的退出， join方法要在close或terminate之后使用
示例代码如下
```python
pool = multiprocessing.Pool(processes=20)#使用Pool方法，创建进程池，有个非常牛叉的电脑，32个核心
    for url in get_url(90, end):
        pool.apply_async(save_Image,(url,))#这里使用的是apply_async，多个进程异步执行；如果调用apply，就变成阻塞版本了。 
    pool.close()
    pool.join()
```