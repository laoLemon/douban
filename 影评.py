# 1、导入需要的库
import urllib.request
from bs4 import BeautifulSoup
# 时间库
import time
# 表格库
import csv

# 2、分多个浏览器访问豆瓣网，防止访问多页时被拒绝
# 每个浏览器在请求数据的时候，请求头是不一样
# 计算机命名规则：驼峰命名法
# url：传值过来的访问地址
def getRequest(url):
    # 谷歌浏览器
    header1 = {
        "Cookie":'douban-fav-remind=1; gr_user_id=be29ac29-c04c-44a5-bbac-5a574b9394c5; bid=Jz8kcqcQrk8; ll="108296"; viewed="35606606"; dbcl2="271848686:KOYPdmk9oAs"; ck=_jFU; push_noty_num=0; push_doumail_num=0; frodotk_db="dc33bf8cb29df16d949b3ea617d9d447"; ap_v=0,6.0',
        "Host":"movie.douban.com",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
    }
    # 用一个请求头，开始访问地址
    req = urllib.request.Request(url=url,headers=header1)
    # 返回结果
    return req


# 封装函数，爬取数据
def getData(url,commentAll):
    # 获取处理后的请求
    req = getRequest(url)
    # 打开网址
    html = urllib.request.urlopen(req)
    # 读取数据(data得到所有数据)
    data = html.read()
    # 输出爬取到的所有数据，进制形式显示
    # print(data)
    # 定义soup对象，解析网页
    soup = BeautifulSoup(data,"html.parser")
    # 找到装有所有评论的id名为comments的div
    # ["数据"]  数组里只有一个元素----数据
    comments = soup.select("#comments")[0]
    # print(comments)
    # 读取到每一条评论，div的class名为comment-item
    items = comments.select(".comment-item")
    # print(items)
    # 循环遍历每一条评论
    for i in items:
        # 找到装着用户名和星级的span标签，class名为comment-info
        info = i.select(".comment-info")[0]
        # print(info)
        # 读出用户名的a标签里面的字符串用户名 [<a></a>]
        # author = info.select("a")[0].string  数据在列表里
        author = info.find("a").string
        # print(author)


        # 取星级，找到装着星级的span标签，读取title值
        # ["看过"，星级，时间]
        star = info.select("span")[1]["title"]
        if (star=="很差"):
            star = 1
        elif (star=="较差"):
            star = 2
        elif (star=="还行"):
            star = 3
        elif (star=="推荐"):
            star = 4
        elif (star=="力荐"):
            star = 5
        # print(star)

        comment_time = ''
        try:
            comment_time = info.select("span")[2]["title"][5:10]
        except KeyError:
            comment_time = "dateerror"
        #print(comment_time)

        # 取评论，找到class名为short的p标签
        short = i.select(".short")[0].string
        # print(short)
        # 将 用户名、星级、评论 装入在字典里面
        talk = {"author":author,"star":star,"short":short,"time":comment_time}
        # print(talk)
        # 将字典类型的数据，加到列表里面
        commentAll.append(talk)
    # 返回整个列表
    return commentAll

# 封装函数，把数据装入表格中
def writeInto(commentAll):
    # 打开表格  as从命名 file
    # 参数1：表格名称
    # 参数2："a+"追加模式  "w"写入模式   "r"读取模式
    # w：writer   r：read  a：append
    # wb二进制，不带b就是文本
    # 参数3：数据格式为utf-8
    # 参数4：newline 新行，空行
    with open("douban.csv","w",encoding="utf-8",newline="") as file:
        # 向表格写入数据
        writer = csv.writer(file)
        # 数据在commentAll列表，循环遍历列表，读取数据
        for i in commentAll:
            # 读取每一个字段  用户名、星级、评论
            info = [i["author"],i["star"],i["short"],i["time"]]
            # 把数据写入表格
            writer.writerow(info)
        # 关闭表格
        file.close()

# 函数的入口
# 直接输入main，有提示
if __name__ == '__main__':
    # 初始化一个空列表,将得到的所有数据
    commentAll = []
    # range()产生序列 0.1.2,爬取3页
    for i in range(0,30):
        # 爬取的网页地址
        # limit=20 每一页读取20条数据
        # start = 80  从第几条读取数据 20-39  40-59  60-79 80-99
        if (i==0):
            url = "https://movie.douban.com/subject/26266893/comments?status=P"
        else :
            start = str(i*20)
            url = ("https://movie.douban.com/subject/26266893/comments?start="+start+"&limit=20&status=P&sort=new_score")
        print(i)
        # 调用函数，爬取数据
        getData(url,commentAll)
        # 每爬取一个页面数据，休息5秒，防止被封号
        time.sleep(5)
    # 调用函数，爬取完数据，装入表格
    writeInto(commentAll)

    # 将表格用 记事本 打开，另存为ANSI格式
    # 如果你要操作数据，还要转回utf-8