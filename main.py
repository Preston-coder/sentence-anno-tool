# coding=utf-8

import web
import os, sys, random
import json
import database
import urllib.request # to encode special characters in url


urls = (
    '/', 'index',
    '/dolabel', 'dolabel',
    '/browse', 'browse',
)
       
render = web.template.render('templates/')
config = json.load(open('config.json'))
collection = config['collection']
user_id = config['user_id'] #这个改成自己的。
PAGE_SIZE = config['page_size']
dbfile = './jobs/%s-%s.sql' % (collection, user_id)
assert(os.path.exists(dbfile)), 'dbfile *** %s *** not found' % dbfile


class index:
    
    def GET(self):
        raise web.seeother('/dolabel')

        input = web.input(query=None)
        resp = {'status':0, 'hits':0, 'random':[], 'tagrel':[]}
        resp['sent_id'] = '1000268201_693b08cb0e.jpg#0'
        resp['user_id'] = 'xirong'
        resp['eng'] = 'A black and white dog is running in a grassy garden surrounded by a white fence .'
        resp['baidu'] = '一只黑白相间的狗在一个长满草的花园里奔跑，被一个白色的栅栏围了起来 一只黑白相间的狗'

        if input.query:
            resp['status'] = 1
            resp['query'] = input.query

        return render.index(resp)


class dolabel:
    
    def GET(self):
        input = web.input(query=None)
        page = input.get("page",1)
        
        per_page = 1   #每页的数量
        records=database.read(dbfile,user_id)
        
        pages = Pagination(cur_page=page,per_page=per_page,total_data=len(records))  #分页类,
        #print(pages.offset)
        #查找当前的这个记录。
        cur_records = database.read_page(dbfile, user_id, limit=pages.offset,offset=per_page)
        #print(cur_records)
        
        todo = len([item for item in records if item['ischeck']=="false"])
        resp = {'user_id':user_id, 'todo':todo}
        resp['video_id'] = cur_records[0]['video_id']

        if todo:
            resp.update(cur_records[0])
            
        return render.dolabel(resp,pages)


    def POST(self):
        input = web.input()
        fullpath = web.ctx.env['HTTP_REFERER']
        if "page" not in fullpath:
            page=1
        else:
            page = int(fullpath.split("page")[-1].split("=")[-1])
        
        per_page = 1   #每页的数量
        records=database.read(dbfile,user_id)
        
        pages = Pagination(cur_page=page,per_page=per_page,total_data=len(records))  #分页类,
        max_page=pages.page_max
        
        video_id = input['video_id']
        #已经提交了，那ischeck是true
        info = {'video_id': video_id, 'cn_caption':input.cn_caption, 'en_caption':input.en_caption, 'flag':input.flag,'ischeck':"true"}
        database.update(dbfile, user_id, video_id, info)
        if page < max_page:

            raise web.seeother('/dolabel?page={}'.format(page+1))
        elif page == max_page:
            raise web.seeother('/dolabel?page={}'.format(page))


class browse:
    
    def GET(self):
        input = web.input(query=None,page=1)
        page = int(input.page)
        if input.query:
            records = database.read(dbfile, user_id, video_id=input.query)
        else:
            records = database.read(dbfile, user_id)
        #records.reverse()
        nr_hits = len(records)
        #print(nr_hits)
        nr_of_pages = int(nr_hits / float(PAGE_SIZE) + 0.5)
        start = (page-1) * PAGE_SIZE
        end = start + PAGE_SIZE 
        todo = len([item for item in records if item['ischeck']=="false"])
        resp = {'user_id':user_id, 'hits':nr_hits, 'todo':todo,'nr_of_pages':nr_of_pages, 'page':page, 'pagesize':PAGE_SIZE}
        resp['results'] = records[start:end]
        return render.browse(resp)


    def POST(self):
        input = web.input()
        raise web.seeother('/browse?query=%s' % urllib.request.quote(input.query))

class Pagination(object):
    '''
        分页类
        参数：
            per_page：每页数量
            total_data：总数目
            cur_page：当前页。
        用法：(flask，html中自定义css)
            py:
                page = int(request.args.get("page",1))  #获取args参数'page'
                per_page = 50   #每页的数量
                dsubAll = query_db("SELECT COUNT(id) AS C FROM dsub",one=True)["C"] #总数目
                pages = Pagination(cur_page=page,per_page=per_page,total_data=dsubAll)  #分页类
                dsub = query_db("SELECT * FROM dsub LIMIT ?,?",(pages.offset,pages.limit))  #取offset与limit进行分页
            html:
                <div>{{ pages.get_html() | safe }}</div>       
    '''
    def __init__(self,per_page=1,total_data=20,cur_page=1):
        import math
        self.size = per_page
        self.data_count = total_data
        self.page_current = int(cur_page)
        self.page_max = int(math.ceil(self.data_count * 0.1 * 10 / self.size ))

        self.page_current = 1 if self.page_current < 1 else self.page_current
        self.page_current = self.page_max if self.page_current > self.page_max else self.page_current
            
        self.offset = ( self.page_current - 1) * self.size
        self.limit = self.size
        
        #判断url中是否有其他参数，以及是否已有page参数
        _fullpath = web.ctx.fullpath
        if "?" in _fullpath:
            if "page" in _fullpath:
                self.url = _fullpath.split("page")[0]
            else:
                self.url = "{}&".format(_fullpath)
        else:
            self.url = "{}?".format(_fullpath)
        
    def get_html(self):
        self.page_pre = self.page_current - 1
        self.page_next = self.page_current + 1
        if self.page_max in (0,1) :
            html = '''
                <ul class="pagination">
                    <li><a>首页</a></li> 
                    <li><a>上一页</a></li> 
                    <li><a>下一页</a></li> 
                    <li><a>尾页</a></li>
            '''
        elif self.page_current <= 1:
            html = '''
                <ul class="pagination">
                    <li><a>首页</a></li> 
                    <li><a>上一页</a></li> 
                    <li><a href="{self.url}page={self.page_next}">下一页</a></li> 
                    <li><a href="{self.url}page={self.page_max}">尾页</a></li>
            '''.format(self=self)
        elif self.page_current >= self.page_max:
            html = '''
                <ul class="pagination">
                    <li><a href="{self.url}page=1">首页</a></li> 
                    <li><a href="{self.url}page={self.page_pre}">上一页</a></li> 
                    <li><a>下一页</a></li> 
                    <li><a>尾页</a></li>
                  
            '''.format(self=self)
        else:
            html = '''
                <ul class="pagination">
                    <li><a href="{self.url}page=1">首页</a></li> 
                    <li><a href="{self.url}page={self.page_pre}">上一页</a></li> 
                    <li><a href="{self.url}page={self.page_next}">下一页</a></li> 
                    <li><a href="{self.url}page={self.page_max}">尾页</a></li>
                
            '''.format(self=self)
        banner = '''
                        <li>
                            <a>第 <code>{self.page_current}</code> 页</a>
                        </li>
                        
                        <li>
                            <a>共 <code>{self.page_max}</code> 页</a>
                        </li>
                    </ul>
                  '''.format(self=self)
        html = '<div>{}</div>'.format(html + banner)
        
        if self.data_count > self.size:
            return html
        else:
            return ""


        
if __name__ == "__main__":
    app = web.application(urls, globals())

    app.run()
