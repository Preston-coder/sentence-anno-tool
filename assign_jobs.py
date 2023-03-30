from __future__ import print_function
import sys, os
import logging
import sqlite3

import database

logger = logging.getLogger(__file__)
logging.basicConfig(
    format="[%(asctime)s - %(filename)s:line %(lineno)s] %(message)s",
    datefmt='%d %b %H:%M:%S')
logger.setLevel(logging.INFO)

ROOT_PATH = "./id_cn_en_chunjiang.txt"
#DEFAULT_USERS = 'chenaozhu,chenxinru,dongchengbo,hufan,huruohan,linhailan,liujiazhen,tiankaibin,wangzihan,lixirong,wuyue,zhaoruixiang'
#DEFAULT_USERS='weiqijie,wangziyue'
DEFAULT_USERS='chunjiang'
LEN_AVG=500

def add_to_db(infos, user_id, resfile):
    try:
        database.create(resfile, user_id)
    except sqlite3.OperationalError:
        logger.info(sqlite3.OperationalError) 
        #logger.info('delete the table or the db file, and try again')
        #return

    conn = sqlite3.connect(resfile)
    c = conn.cursor()
    
    inserted = 0
    for info in infos:
        try:
            database.insert(resfile,user_id,info)
            inserted += 1
        except:
            print("fail")
    conn.commit()
    c.close()
    conn.close()

    logger.info('%d records inserted into %s', inserted, resfile) 


'''def process(options, collection):
    rootpath = options.rootpath
    users = options.users.split(',')
    logger.info('%d users: %s', len(users), ', '.join(users))
    assert(len(users) == len(set(users)))
    nr_of_users = len(users)
    imset_file = os.path.join(rootpath, collection, 'ImageSets', '%s.txt'%collection)
    imset = map(str.strip, open(imset_file).readlines())
    logger.info('assign %d images to %d users', len(imset), nr_of_users)

    jobs = [[] for i in range(nr_of_users)]
    for i,img_id in enumerate(imset):
    	job_idx = i%nr_of_users
    	jobs[job_idx].append(img_id)

    re_collected = []
    for j,user_id in enumerate(users):
    	logger.info('%s gets %d images', user_id, len(jobs[j]))
    	re_collected += jobs[j]
    	resfile = '%s-%s.sql' % (collection, user_id)
    	add_to_db(jobs[j], user_id, resfile)
    
    assert(len(re_collected) == len(set(re_collected)))
    assert(len(set(re_collected).intersection(set(imset))) == len(imset))'''

def process(options):
    #分配任务
    rootpath = options.rootpath
    users = options.users.split(',')
    jobs_avg=options.jobs
    logger.info('%d users: %s', len(users), ', '.join(users))
    assert(len(users) == len(set(users)))

    with open(rootpath,'r') as tf:
        lines = tf.readlines()
    
    idx=0
    for i in range(0,len(lines),jobs_avg):
        infos=[]
        for line in lines[i:i+jobs_avg]:
        #print(line)
            video_id = line.split("\t")[0]
            cn = line.split("\t")[1]
            en = line.strip("\n").split("\t")[2]
            info={'video_id':video_id,'cn_caption':cn,'en_caption':en,'ischeck':"false",'flag':"false"}
            infos.append(info)
        user_id = users[idx]
        dbfile="./jobs/test-{}.sql".format(user_id)

        add_to_db(infos,user_id,dbfile)
        idx+=1
        if idx >= len(users):
            break

    return True


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    from optparse import OptionParser
    parser = OptionParser(usage="""usage: %prog [options] collection""")
    parser.add_option("--rootpath", default=ROOT_PATH, type="string", help="root path where collection is stored (default: %s)" % ROOT_PATH)
    parser.add_option("--users", default=DEFAULT_USERS, type="string", help="list of annotators (default: %s)" % DEFAULT_USERS)
    parser.add_option("--jobs",default=LEN_AVG,type="int", help="Number of tasks assigned to each person (default: %s)" % LEN_AVG)
    #parser.add_option("--overwrite", default=0, type="int", help="overwrite existing file (default=0)")
    
    (options, args) = parser.parse_args(argv)
    
    #if len(args) < 1:
    #    parser.print_help()
    #    return 1
    
    return process(options)

    
if __name__ == "__main__":
    sys.exit(main())
