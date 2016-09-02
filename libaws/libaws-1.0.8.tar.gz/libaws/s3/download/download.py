#coding:utf-8
import os
import random
import datetime
from concurrent import futures
import functools
import Queue
from libaws.common.boto import *
from libaws.common import utils
from libaws.base import callback,utils as baseutils
from libaws.common.db import *
from libaws.common.logger import *
from libaws.common import config
from libaws.common import fileobj
from libaws.base import filerange
from libaws.common import const
from libaws.common.errorcode import *
import partdownloader

#获取下载数据库操作对象
s3_download_db = S3DownloadDb.get_db()

def download_range(download_range_id,file_range,s3_file_obj,download_file_obj,que,callback=None):

    '''
        下载文件某部分范围
    '''
    global s3_download_db

    #下载失败重试次数
    number_retry_count = config.DOWNLOAD_RETRY_TIMES
    #下载重试时上次重试下载的字节数，第一次时为-1
    last_range_download_size = -1
    #下载该部分时获取已经下载的字节数
    read_size = s3_download_db.get_range_download_size(download_range_id)
    #下载重试，如果第一次下载成功，则后面的几次不需要重试了，直接返回成功结果
    for i in range(number_retry_count):
        part_id = file_range.range_id
        start_byte = file_range.start
        #是否是最后一个分块
        is_last_part = file_range.is_last
        range_download_size = s3_download_db.get_range_download_size(download_range_id)
        #不是第一次重试时，获取此次重试已经下载的字节数
        if last_range_download_size != -1:
            #第n次重试下载的总字节数减去第n-1次重试下载的总字节数，为此次重试已经下载的字节
            last_range_read_size = range_download_size - last_range_download_size
            assert(last_range_read_size >=0)
            read_size += last_range_read_size

        last_range_download_size = s3_download_db.get_range_download_size(download_range_id)

        #开始下载的字节位置为已经下载的字节数
        start_byte += range_download_size
        #结束字节位置必须将该部分的结束字节位置-1
        end_byte = file_range.end - 1
        #根据HTTP分块下载协议，指定下载开始-结束字节范围
        if not is_last_part:
            range_str = 'bytes=%d-%d' % (start_byte,end_byte)
        else:
            #如果是最后一个分块，不需要指定结束字节位置
            range_str = 'bytes=%d-' % (start_byte)

        logger.debug('part_id:%d,rangestr:%s,attempt:%d range_download_size:%ld,read_size:%ld',part_id,range_str,i+1,range_download_size,read_size)
        try:
            respose = s3_file_obj.get(Range=range_str)
            part_body = respose['Body']
            #开始下载分块
            part_downloader = partdownloader.MultiPartDownloader(download_range_id,download_file_obj,s3_file_obj,file_range,que)
            #计算总的分块下载字节数
            read_size += part_downloader.download(part_body,callback)
            assert(read_size == file_range.size)
            return read_size
        except Exception,e:
            #下载失败重试第n次
            logger.debug("Retrying exception caught (%s),retrying request, (attempt %s / %s)", e, i+1,number_retry_count)
            continue
           
    #超过重试下载次数时抛出异常，并在上一级函数里面捕获该异常
    raise ValueError(ERROR_CODE_MESSAGES[EXCEED_MAX_DOWNLOAD_ATTEMPTS])

def store_download_parts(download_id,file_ranges):
    
    '''
        存储文件分块信息
    '''
    
    global s3_download_db

    datas = []
    for file_range in file_ranges:
        part_id = file_range.range_id
        block_size,start_byte,end_byte = file_range.size,file_range.start,file_range.end
        logger.debug('part_id:%d block_size:%ld,start_byte:%ld end_byte:%ld,is_last_block:%s',\
                        part_id,block_size,start_byte,end_byte,file_range.is_last)
        datas.append((part_id,block_size,start_byte,end_byte,download_id,file_range.is_last))

    sql = '''
        insert into range (range_id,range_size,start_byte,end_byte,download_id,is_last_range) values (?,?,?,?,?,?)
    '''
    s3_download_db.save(sql,datas)

def download_range_part(s3_file_obj,download_file_obj,callback,que,range_id):

    global s3_download_db
    sql = '''
            select * from range where id=%d
        ''' % (range_id)

    result = s3_download_db.fetchone(sql)

    part_id = result[1]
    start_byte = result[3]
    end_byte = result[6]
    block_size = result[2]
    is_last_range = result[10]
    file_range = filerange.FileRange(download_file_obj.path,part_id,start_byte,end_byte,block_size,is_last_range)
    try:
        read_size = download_range(range_id,file_range,s3_file_obj,download_file_obj,que,callback)
    except Exception,e:
        logger.error("%s",e)
        #下载失败
        s3_download_db.set_download_status(const.STATUS_DOWNLOAD_FAIL,download_file_obj.download_id)
        return 0,False

    return read_size,True

def download_key_parts(s3_file_obj,download_file_obj,f,download_thread_num,callback=None):
    '''
        下载文件分块
    '''

    global s3_download_db

    file_path = download_file_obj.path
    download_id = download_file_obj.download_id
    sql = '''
            select * from range where download_id=%d
        ''' % (download_id)

    #查询文件分块信息
    results = s3_download_db.fetchall(sql)
    part_num = s3_download_db.get_range_number(download_id)
    if len(results) != part_num:
        logger.error('file:%s download parts is damaged',file_path)
        return  
    
    total_download_size = 0
    range_ids = []
    que = Queue.Queue()
    #下载所有分块
    for row in results:
        download_range_id = row[0]
        range_id = row[1]
        is_download = row[5]
        block_size = row[2]
        start_time = row[8]
        range_download_size = row[11]
        #设置下载开始时间
        if start_time is None:
            update_sql = '''
                update range set start_time=? where id=?
            '''
            now_time = datetime.datetime.now()
            data = [(now_time,download_range_id),]
            s3_download_db.update(update_sql,data)
        #如果该分块已经下载过了，不需要再下载
        if is_download:
            total_download_size += block_size
            assert(block_size == range_download_size)
            logger.info('file:%s range:%d has already downloaded',file_path,range_id)
            continue
        range_ids.append(download_range_id)

    with futures.ThreadPoolExecutor(max_workers=2) as controller:

        download_parts_handler = functools.partial(download_part_as_future,s3_file_obj, download_file_obj,callback,que,range_ids,download_thread_num)
        parts_future = controller.submit(download_parts_handler)

        io_writer_handler = functools.partial(loop_on_io_writes, que,f,download_file_obj)
        io_future = controller.submit(io_writer_handler)

        results = futures.wait([parts_future, io_future],return_when=futures.FIRST_EXCEPTION)
        finished, unfinished = results
        for future in finished:
            future.result()

def loop_on_io_writes(que,f,download_file_obj):

    io_writer = partdownloader.IOLooper(que,download_file_obj)
    io_writer.loop_on_io(f)

def download_part_as_future(s3_file_obj, download_file_obj,callback,que,range_ids,thread_num):

    try:
        download_partial = functools.partial(download_range_part,s3_file_obj, download_file_obj,callback,que)
        with futures.ThreadPoolExecutor(max_workers=thread_num) as executor:
            for download_part in executor.map(download_partial,range_ids):
                pass
    finally:
        que.put(partdownloader.SHUTDOWN_SENTINEL)

def get_download_size(temp_file_path,dest_file_path):
    '''
        断点续传，获取已经下载的文件字节数,但是最终以数据库里面保存的下载字节数为准
    '''

    if os.path.exists(temp_file_path):
        return os.path.getsize(temp_file_path)
    
    if os.path.exists(dest_file_path):
        return os.path.getsize(dest_file_path)

    return 0

def get_tmp_filename(path,file_name):

    '''
        临时生成随机下载文件名
        临时文件名 = 原始文件名 + "." + 8位随机数字字母
    '''

    salt = "".join(random.sample(config.DOWNLOAD_SALT_SOURCE, 8))
    tmp_file_name = '%s.%s' % (file_name,salt)
    tmp_file_path = os.path.join(path,tmp_file_name)

    return tmp_file_path

def save_download_info(bucket,key,dest_path,file_obj):

    '''
        保存下载文件和文件分块信息
    '''

    global s3_download_db
    
    part_size = config.DOWNLAD_PART_LIMIT_SIZE
    #按固定默认分块大小，将该文件默认分成n快
    file_ranges = filerange.get_file_ranges_by_size(file_obj.path,part_size,file_obj.size)
    #分块个数
    range_number = len(file_ranges)
    sql = '''
        insert into download(bucket,key,filepath,filename,tmp_file_path,dest_path,file_size,etag,start_time,status,range_num) values(\
                ?,?,?,?,?,?,?,?,?,?,?)
    '''
    data = [(bucket,key,file_obj.path,file_obj.name,file_obj.tmp_file_path,dest_path,file_obj.size,\
                file_obj.etag,datetime.datetime.now(),const.STATUS_START_DOWNLOAD,range_number),]
    s3_download_db.save(sql,data)

    download_id = s3_download_db.get_download_id(bucket,key)
    store_download_parts(download_id,file_ranges)

def complete_download(bucket,key,download_file_obj):

    '''
        最终完成下载，设置下载状态为下载成功
        修改临时文件名为原始文件名
        校验下载文件的md5值，文件的一致性
    '''

    global s3_download_db

    dest_file_path = download_file_obj.path
    tmp_file_path = download_file_obj.tmp_file_path
    download_id = download_file_obj.download_id

    if os.path.exists(tmp_file_path):
        #如果存在原始文件，删除它
        if os.path.exists(dest_file_path):
            os.remove(dest_file_path)

        #重命名临时文件为原始文件
        os.rename(tmp_file_path,dest_file_path)

    now_time = datetime.datetime.now()
    update_sql = '''
        update download set is_download=?,end_time=?,download_percent=?,hash=?,status=? where id=?
    '''
    #获取下载文件的md5值
    download_file_obj.hash = download_file_obj.get_hash()
    #和服务器上的文件hash值进行比对是否一致,如果一致表示文件下载成功，反之下载失败
    if not download_file_obj.validate():
        #文件校验失败
        s3_download_db.set_download_status(const.STATUS_DOWNLOAD_FAIL,download_id)
        logger.error("download_id:%d md5 check sum is not match",download_id)
        return False

    #文件下载成功，设置下载状态为下载成功
    logger.debug('check download file %s md5 hash success',download_file_obj.path)
    s3_download_db.update(update_sql,[(True,now_time,'100%',download_file_obj.hash,const.STATUS_DOWNLOAD_SUCCESS,download_id)])
    logger.info('download elapse time %s',s3_download_db.get_download_time(download_id))

    return True

def init_file_obj(tmp_file_path):

    '''
        获取下载文件打开方式
    '''
    #如果临时文件存在,则采用读的方式打开
    if os.path.exists(tmp_file_path):
        #采用读，同时要支持写
        mode = "rb+"
    else:
        #否则采用写的方式,创建一个新的临时文件
        mode = "wb+"
    f = open(tmp_file_path,mode)
    return f

def download_zero_file(bucket,key,dest_path):

    logger.warn('file %s in bucket %s size is 0',key,bucket)
    try:
        file_obj = s3.Object(bucket,key)
        file_obj.download_file(dest_path)
    except Exception,e:
        logger.error('%s',e)
        return False

    return True

def check_download_size(download_id):

    global s3_download_db

    download_size = s3_download_db.get_download_size(download_id)
    range_download_size = s3_download_db.get_total_range_download_size(download_id)
    if download_size != range_download_size:
        logger.warn("download size %ld is not equal to range download size %ld",download_size,range_download_size)
        s3_download_db.reset_download_size(range_download_size,download_id)
    else:
        logger.debug("download size %ld ,range download size %ld",download_size,range_download_size)
    
def download_file(download_config):
    '''
        下载文件
    '''

    def init_download():
        #随机获取临时下载文件名,在原始文件名后加上8位随机字母数字
        tmp_file_path = get_tmp_filename(dest_path,file_name)
        return tmp_file_path,0,True

    global s3_download_db
    
    bucket,key,dest_path,file_name = download_config.bucket,download_config.key,download_config.dest_path,download_config.filename
    dest_file_path = os.path.join(dest_path,file_name)
    file_dir_path = os.path.dirname(dest_file_path)
    if not os.path.exists(file_dir_path):
        try:
            baseutils.mkdirs(file_dir_path)
        except Exception,e:
            logger.error("%s",e)
            return False
    
    #判断bucket是否存在
    try:
        if not utils.is_bucket_exists(bucket):
            logger.error("%s",ERROR_CODE_MESSAGES[BUCKET_NOT_EXISTS].format(bucket))
            return False
    except Exception,e:
        logger.error("%s",e)
        return False

    #判断bucket里面的文件是否存在
    if not utils.is_bucket_file_exists(bucket,key):
        logger.error("%s",ERROR_CODE_MESSAGES[BUCKET_FILE_NOT_EXISTS].format(key,bucket))
        return False

    s3_file_obj = s3.Object(bucket,key)
    file_size = s3_file_obj.content_length

    if 0 == file_size:
        return download_zero_file(bucket,key,dest_file_path)
    etag = s3_file_obj.e_tag

    #通过bucket和key查找是否有存在保存的下载信息
    download_id = s3_download_db.get_download_id(bucket,key)
    is_need_save = False
    #第一次下载，初始化下载信息
    if download_id is None:
        tmp_file_path,download_size,is_need_save = init_download()
    else:
        #获取保存的下载信息
        download_size,tmp_file_path,download_succ = s3_download_db.get_download_info(download_id)
        if not download_succ:
            file_download_size = get_download_size(tmp_file_path,dest_file_path)
            logger.debug('file download size is %d,db download size is %d',file_download_size,download_size)
        #如果是强制重新下载，则删除上次保存的下载信息，并新建下载信息
        if download_config.force_again_download:
            logger.debug('delete download:%d',download_id)
            s3_download_db.delete_download(download_id)
            tmp_file_path,download_size,is_need_save = init_download()

    #构建下载文件对象
    download_file_obj = fileobj.DownloadFileObj(dest_file_path,tmp_file_path,file_size,etag)

    #第一次或者强制重新下载时，保存下载信息
    if is_need_save:
        save_download_info(bucket,key,dest_path,download_file_obj)

    #获取下载id，并赋给下载文件对象
    download_id = s3_download_db.get_download_id(bucket,key)
    download_file_obj.download_id = download_id
    
    check_download_size(download_id)
    
    #判断上次下载状态是否时下载完成，如果是则不用再重新下载了，只需要更改临时下载文件名，并校验md5即可完成下载
    download_status = s3_download_db.get_download_status(download_file_obj.download_id)
    if const.STATUS_DOWNLOAD_FINISHED == download_status:
        return complete_download(bucket,key,download_file_obj)

    #如果上次下载成功，此次下载时提示是否需要强制重新下载，是则重新下载，反之则否
    elif const.STATUS_DOWNLOAD_SUCCESS == download_status:
        logger.error('%s',ERROR_CODE_MESSAGES[DOWNLOAD_AGAIN_FILE_SUCCESS].format(download_file_obj.path))
        return False

    #设置下载打开文件方式
    try:
        f = init_file_obj(tmp_file_path) 
    except Exception,e:
        logger.error("%s",e);
        return False

    #开始下载文件分块
    if config.LOGGER_DISABLED or not download_config.enable_debug_log:
        with callback.DownloadProgressPercentage(download_file_obj.path,download_file_obj.size,download_size) as cb:
            download_key_parts(s3_file_obj,download_file_obj,f,download_config.thread_num,cb)
    else:
        download_key_parts(s3_file_obj,download_file_obj,f,download_config.thread_num)
    f.close()

    #获取文件下载最终状态
    download_status = s3_download_db.get_download_status(download_file_obj.download_id)
    #下载完成时，执行最后一步完成下载操作
    if const.STATUS_DOWNLOAD_FINISHED == download_status:
        return complete_download(bucket,key,download_file_obj)
    else:
        return False

def start_download(download_config):

    dest_path,file_name = download_config.dest_path,download_config.filename
    dest_file_path = os.path.join(dest_path,file_name)
    if download_file(download_config):
        download_config.result = True
        logger.prompt('download file %s success',dest_file_path)
    else:
        logger.error('download file %s fail',dest_file_path)
