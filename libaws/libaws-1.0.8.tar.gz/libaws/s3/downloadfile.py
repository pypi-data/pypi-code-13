#coding:utf-8
import os
import argparse
from libaws.common import config
from libaws.common.logger import logger,enable_debug_log
from libaws.s3.download import download
from libaws.s3 import daemonize
from libaws.s3.bucket import list_as_dir

def main():
    parser = argparse.ArgumentParser()
    #指定下载的bucket,必须参数
    parser.add_argument("-b", "--bucket", type=str, dest="bucket",help='dest bucket to download file',required=True)
    #指定下载bucket中的文件,必须参数
    parser.add_argument("-k", "--key", type=str, dest="key", help = 'bucket file to download',required=True)
    #指定下载路径,默认为当前路径
    parser.add_argument("-p", "--path", type=str, dest="path", help = 'file download path to save',default = './',required=False)
    #指定下载文件名,默认和key一致
    parser.add_argument("-f", "--filename", type=str, dest="filename", help = 'download file name',default = None,required=False)
    #是否强制重新下载某个文件,默认为否
    parser.add_argument("-force", "--force-again-download", action='store_true', dest="force_again_download",help='need to download again when download is exists',default = False)
    #是否开启日志调试模式
    parser.add_argument("-debug", "--enable-debug-log", action='store_true', dest="enable_debug_log",help='enable debug log or not',default = config.ENABLE_DEBUG_LOG)
    parser.add_argument("-d", "--daemon", action='store_true', dest="is_daemon_run",help='indicate this process is run in daemon or not',default = False)
    parser.add_argument("-t", "--thread", type=int, dest="thread_num",help='thread number to download file part',default=config.DEFAULT_THREAD_SIZE)
    args = parser.parse_args()
    bucket = args.bucket
    key = args.key
    
    filename = os.path.basename(key)
    if args.filename is not None:
        filename = args.filename

    dest_path = os.path.abspath(args.path)
    extra_args = {
        'force_again_download':args.force_again_download,
        'enable_debug_log':args.enable_debug_log,
        'thread_num':args.thread_num
    }
    if args.is_daemon_run:
        daemonize()
    download_config = config.DownloadConfig(bucket,key,dest_path,filename,**extra_args)
    enable_debug_log(args.enable_debug_log)
    dest_file = os.path.join(dest_path,filename)
    logger.info('start download file %s',dest_file)

    if key.endswith("/"):
        total_file_count = 0
        total_success_count = 0
        total_fail_count = 0
        dir_keys = list_as_dir(bucket,key)
        for dkey in dir_keys:
            download_config.filename = dkey
            download_config.key = dkey
            download.start_download(download_config)
            total_file_count += 1
            if download_config.result:
                total_success_count += 1
            else:
                total_fail_count += 1
        logger.info("total download file count %d,success download count %d,fail download count %d",total_file_count,total_success_count.total_fail_count)
    else:
        download.start_download(download_config)
    logger.info('end download file %s',dest_file)
    
    
