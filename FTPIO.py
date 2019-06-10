import threading, requests, time
import sys
import ftplib
import os
from ftplib import FTP

# FTP 계정 설정
_password = ""
_addr = "" 
_user = ""

# 다운받아질 디렉토리
_DirName = "./"       # ./대상폴더

# FTP서버의 디렉토리
_FtpDirName = "./"   # ./대상폴더/

########################################################
# FTP 유틸리티 함수
########################################################

KOKO = 0                    # 스레드 갯수 체크 변수

# 단발 다운로드
def FtpDown(Num, NAME, IP, ID, PW, DownloadedDIR, PORT = 21):
  
    global KOKO             # 스레드 갯수 체크 변수를 글로벌 변수로 만듬
    KOKO = KOKO + 1         # 작업에 들어가면 스래드 갯수 제한을 위해 변수를 하나 더함
    filename = NAME
    ftp=ftplib.FTP()
    ftp.connect(_addr,PORT)
    ftp.login(_user,_password)
    ftp.cwd(_FtpDirName)
    fd = open(DownloadedDIR + filename,'wb')
    ftp.retrbinary("RETR " + filename, fd.write)
    fd.close()
    KOKO = KOKO - 1         # 작업이 종료되면 체크 변수를 다음 스레드를 위해 하나 뺌
    return Num
  
def FtpDownSingle(IP, user, password, NAME, DownloadedDIR, ftpDIR,  PORT = 21):
    filename = NAME
    ftp=ftplib.FTP()
    ftp.connect(IP,PORT)
    ftp.login(user,password)
    ftp.cwd(ftpDIR)
    fd = open(DownloadedDIR + filename,'wb')
    ftp.retrbinary("RETR " + filename, fd.write)
    fd.close()
  
# 멀티 다운로드 모듈
def FtpMultiDown(_FileInfo, Thread=10):

    global KOKO

    # 쓰레드의 총 수
    NNNN = Thread

    for sss in range(len(_FileInfo)):
        
        if(NNNN > KOKO):
          
            lst = threading.Thread(target=FtpDown, args=(_FileInfo[sss][0], 
                                                         _FileInfo[sss][4], 
                                                         _addr, _user, _password, _DirName))
            lst.start()
        
        elif(NNNN <= KOKO):
            
            while (1):
                
                time.sleep(1)            
                
                if(NNNN > KOKO):
                  
                    lst = threading.Thread(target=FtpDown, 
                                           args=(_FileInfo[sss][0], 
                                                 _FileInfo[sss][4], 
                                                 _addr, _user, _password, _DirName))
                    lst.start()

                    break
            

    # 모든 스레드가 끝날때까지 기다림
    while(1):
      
        time.sleep(1)
        
        if(KOKO==0):
            break
  
# 파일 목록
def FtpFileListRead(FolderName, addr, user, password):
    """
    폴더 단위로는 작업을 실행하지 못함\n
    FolderName의 최상단에 파일들이 모조리 있어야함\n
    \n
    ex) FolderName file1.ex \n
                   file2.ex \n
                   file3.ex \n
                   file4.ex \n
    \n
    이것은 안됨\n
    ex) FolderName Afolder/file1.ex \n
                   Afolder/file2.ex \n
                   Afolder/file3.ex \n
                   Afolder/file4.ex \n

    """
    
    DataLoad = ftplib.FTP(addr, user, password)       # FTP Server Login
    DataLoad.cwd(FolderName)                          # change directory
    FileList = []
    DataLoad.retrlines('MLSD', FileList.append)
    DataLoad.close()  
    
    FileInfo = []               # 파일 정보를 담아둠 [n][번호, 파일타입, 수정시간, 크기, 이름]

    Num = 0                     # 파일 정보의 번호를 카운트 하는 변수
    
    for entry in FileList:
        FileNum_buffer = Num
        FileType_buffer = entry.split(";")[0].lstrip()
        FileModi_buffer = int(entry.split(";")[1].lstrip().split("=")[1])
        FileSize_buffer = int(entry.split(";")[2].lstrip().split("=")[1])
        FileName_buffer = entry.split(";")[3].lstrip()
        
        FileInfo_buffer = [Num, 
                           FileType_buffer, 
                           FileModi_buffer, 
                           FileSize_buffer, 
                           FileName_buffer]
        
        FileInfo.append(FileInfo_buffer)
        
        Num = Num + 1
    
    FileType_buffer = []        # 버퍼를 비워둠
    FileModi_buffer = []        #
    FileSize_buffer = []        #
    FileName_buffer = []        #
    FileInfo_buffer = []        #
    
    return FileInfo

def FtpSetting(ip, user, _pass):
    
    # FTP 계정 설정
    global _password 
    global _addr 
    global _user 

    _password = _pass
    _addr = ip
    _user = user

def FtpDirectory(FTP_dir, PC_dir):

    # 다운받아질 디렉토리
    global _DirName
    _DirName = PC_dir
    
    # FTP서버의 디렉토리
    global _FtpDirName
    _FtpDirName = FTP_dir

def Start(ThreadNum = 10):

    try:
        os.makedirs(os.path.join(_DirName))     # 폴더를 생성
        print("Ok")
    except FileExistsError:                   # 파일이 존재함
        print("Exist")

    a323 = FtpFileListRead(_FtpDirName, _addr, user=_user, password= _password)

    for accs in a323:
        print(accs)

    FtpMultiDown(a323, ThreadNum)
