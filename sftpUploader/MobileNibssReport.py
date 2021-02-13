import os
import socket
import paramiko
import sys
import logging
import datetime
from time import sleep

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger('niupload')
hdlr = logging.FileHandler('D://Daily_backup//upload.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

hostname = 'xxxx.xxxx-plc.com.ng' #'.nssssss-plc.com'
username="qerweere"
password="6769tuyiyiuy"
port = 22
remotedest = '/users/GMPM/BANK/'


def nibsslogger():
    bankcode = '03'
    previous_date = datetime.datetime.today() - datetime.timedelta(days=1)
    conget = previous_date.strftime('%Y%m%d')
    #conget = int(get)-3
    getdate=(bankcode+'_'+(str(conget)))
    localpath = r'D:\\report\\NEW_REPORT\\' + getdate + '.txt'
    remotepath = remotedest + getdate + '.txt'

    logger.info("STARTING RENDITION FOR: %s", getdate )
    logger.debug("getdate: %s", getdate )

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.debug('Starting NIBSS Connection:')
        ssh.connect(hostname,port,username,password)
        transport= ssh.get_transport()
        #print(transport)
        logger.debug('transport: %s', transport)

    except (socket.error, paramiko.AuthenticationException) as message:
        print("ERROR: SSH connection to "+ hostname+" failed: " +str(message))
        logger.debug('Error: Unable to connect, %s', str(message))
        sys.exit(1)
        #if conn is None:
        #print("Successfully Authenticated")
    sftp = ssh.open_sftp()
    filedetails = str(getdate+'.txt')
    fn_list_local = os.stat(localpath)
    fn_list = (sftp.listdir_attr(remotedest))
    print('List of files @Local:', fn_list_local)
    localFileSize = [fn_list_local.st_size, ':', os.path.basename(localpath)]
    print('LocalFileSize:', localFileSize)
    print('Local File Size:', fn_list_local.st_size)
    #print('Remote File Size:', fn_list)

    def fileLoader():
        localpath = r'D:\\nibss_report\\NEW_REPORT\\' + filedetails
        remotepath = remotedest + filedetails
        uploader = sftp.put(localpath, remotepath)
        logger.debug('uploading_done: %s', (uploader, ':', filedetails))

    try:
        for info in fn_list:
            recentFile = (filedetails, info.filename, info.st_size)
            if filedetails == info.filename:
                logger.info('Loaded %s', filedetails)
            if recentFile[2] == fn_list_local.st_size:
                lo
                gger.info('File is the same size %s', (recentFile[2], ':', fn_list_local.st_size))
                break
        else:
            logger.info('Not loaded or File is not the same size %s', (recentFile[2], ':', fn_list_local.st_size))
            logger.info('Uploading in progress........ %s')
            fileLoader()

    except EOFError as e:
        print('Error:', e)
        logger.info(e)

    closesftp = sftp.close()
    closessh = ssh.close()
    print(closesftp, closessh, sep='<==>')
 
nibsslogger()