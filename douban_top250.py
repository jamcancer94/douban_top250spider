# -*- coding:utf-8 -*-
import time
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#参数是网址输入，返回一个decode的页面，可直接用于正则表达式找出关键字
def code_page(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    mypage = response.read().decode("utf-8")
    return mypage
#参数基网址输入，返回值是一个元素是[电影名，电影网址]的列表
def get_html():
    load_result = []
    for i in range(1):
        url_top = 'https://movie.douban.com/top250?start=' + str(i*25) + '&filter='
        myhtml = code_page(url_top)

        #url不要和“”一起输出
        result = re.findall('<div class="info">.*?<a href="(.*?)" class="">.*?'
                            '<span class="title">(.*?)</span>.*?</div>.*?<div class="bd">.*?'
                            '<p class="">(.*?)</p>.*?<span class="rating_num" property="v:average">'
                            '(.*?)</span>', myhtml, re.S)
        #容易出错点。
        for i in result:
            load_result.append(i)
    return load_result
#返回电影名字
def get_name():
    movie_name = []
    load_result = get_html()
    for i in load_result:
        movie_name.append(i[1])
    #print('top %d, movie name : %s, link:%s' % (movie_num,movie_name,movie_html))
    return movie_name
#评分
def get_star():
    movie_star = []
    load_result = get_html()
    for i in load_result:
        movie_star.append(i[3])
    return movie_star
#导演信息
def get_bd():
    movie_bd = []
    load_result = get_html()
    for i in load_result:
        movie_bd.append(i[2].replace(' ', '').replace('<br>', '').\
                        replace('\t', '').replace('\n', '').replace('&nbsp;', '').replace(' ', ''))
    return movie_bd
#返回一个电影网址的列表
def get_link():
    movie_html = []
    #调用get_html函数
    load_result = get_html()
    for i in load_result:
        movie_html.append(i[0])
        #print('top %d, movie name : %s, link:%s' % (movie_num,movie_name,movie_html))
    return movie_html

#返回元素是每个电影评论的列表
def get_content():
    content_load = []
    error_show = '    网页被删除！'
    get_links = get_link()
    for link in get_links:
        url = link
        #返回pagecontent是解码过的html页面,若页面不存在，存入错误显示
        try:
            pagecontent = code_page(url)
            comment = re.findall('<span property="v:summary".*?>(.*?)</span>', pagecontent, re.S)
            for i in comment:
                content_load.append(i)
        except:
            content_load.append(error_show)
    return content_load
#写入文件
def data_write():
    f = file("豆瓣top250.txt", "w")
    top_num = 1
    for name,star,bd,comment in zip(get_name(),get_star(),get_bd(),get_content()):
        f.write('TOP_%d  ' % (top_num))
        f.write(name + '    ' + star + '\n' + bd + '\n简介：' + \
                comment.replace(' ', '').replace('<br/>', '').replace('\t', '').replace('\n', ''))
        f.write('\n-------------------------------------------------------------------------------\n')
        print('第%d 个写入完成！' % (top_num))
        top_num += 1
    print('完成！')
    f.close()

if __name__ == '__main__':
    #计时
    time_start = time.time()
    data_write()
    time_end = time.time()
    print('finished:%d s'%(time_end-time_start))
