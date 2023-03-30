from __future__ import print_function
import sys
import os
import time
import sqlite3
import logging

logger = logging.getLogger(__file__)
logging.basicConfig(
    format="[%(asctime)s - %(filename)s:line %(lineno)s] %(message)s",
    datefmt='%d %b %H:%M:%S')
logger.setLevel(logging.INFO)


def create(dbfile, tablename):
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    c.execute('''Create table "%s"
     (video_id text PRIMARY KEY, cn_caption text, en_caption text, flag text, ischeck text, date text)''' % tablename)
    #check表示是否已经标注了。
    conn.commit()
    c.close()
    conn.close()

def insert(dbfile,tablename,info):
    time_stamp = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    conn = sqlite3.connect(dbfile)
    c=conn.cursor()
    c.execute('INSERT INTO ' + '"' + tablename + '"' + 'VALUES (?,?,?,?,?,?)',(info['video_id'], info['cn_caption'], info['en_caption'], info['flag'], info['ischeck'],time_stamp))
    conn.commit()
    c.close()
    conn.close()

def read(dbfile, tablename, video_id=None): #就是只能用videoid查看。
    #logger.info('read table %s from %s', tablename, dbfile)
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    
    if video_id:
        c.execute('select * from ' + '"' + tablename + '"' + ' where video_id=?', (video_id))
    else:
        c.execute('select * from ' + '"' + tablename + '"')

    results = []
    for row in c:
        results.append({'video_id':row[0], 'cn_caption':row[1], 'en_caption':row[2], 'flag':row[3], 'ischeck':row[4], 'date':row[5]})
    c.close()
    conn.close()

    return results

def read_page(dbfile, tablename, limit=None,offset=None): #就是只能用videoid查看。
    #logger.info('read table %s from %s', tablename, dbfile)
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    
    c.execute('select * from ' + '"' + tablename + '"' + " limit "+str(limit)+" ," + str(offset))

    results = []
    for row in c:
        results.append({'video_id':row[0], 'cn_caption':row[1], 'en_caption':row[2], 'flag':row[3], 'ischeck':row[4], 'date':row[5]})
    c.close()
    conn.close()

    return results
        
 
def update(dbfile, tablename, video_id, info):
    time_stamp = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
    conn = sqlite3.connect(dbfile)
    
    c = conn.cursor()
    c.execute('update ' + '"' + tablename + '"' + ' set video_id=?, cn_caption=?, en_caption=?, flag=?,ischeck=?, date=? where video_id=?', 
              (info['video_id'], info['cn_caption'], info['en_caption'], info['flag'], info['ischeck'], time_stamp, video_id))

    if c.rowcount < 1:
        print("error")
        #error
    else:
        #success
        print("success")
    conn.commit()
    c.close()
    conn.close()


if __name__ == "__main__":
    collection = 'test'
    user = ''
    dbfile = "./jobs/%s-%s.sql" % (collection, user)
    #dbfile = "/Users/wangziyuan/Desktop/jobs/test-dongchengbo.sql"
    tablename = user

    #create(dbfile, tablename)    

    record = read(dbfile, tablename)
    print (len(record))
    count = 0
    for item in record:
        if item['flag'] == "unsure":
            count += 1
    print(count)

    #把txt里的导入
    '''with open("./id_en_cn.txt",'r') as tf:
        lines = tf.readlines()
        print(len(lines))
    for line in lines:
        #print(line)
        video_id = line.split("\t")[0]
        cn = line.split("\t")[1]
        en = line.strip("\n").split("\t")[2]
        info={'video_id':video_id,'cn_caption':cn,'en_caption':en,'ischeck':"false",'flag':"false"}
        #print(info)
        insert(dbfile,tablename,info)'''
    
    record = read(dbfile, tablename)
    print (record[0:20])

   

