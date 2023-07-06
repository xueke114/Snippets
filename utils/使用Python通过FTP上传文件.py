from pathlib import Path
from ftplib import FTP

target_ip = "192.168.67.56"
username = "xueke"
password = "12138"
with FTP(host=target_ip, user=username, passwd=password) as ftp:
    # 切换到目标目录
    ftp.cwd("test-ftp")
    # 列出目标目录的文件
    ftp.retrlines('LIST')

    # 上传
    print("======== 上传一些文件 ========")
    for file in Path("C:/RSDatasets/SMAP-L3-SPL3SMA/201505").glob("*.txt"):
        print(file.name)
        with open(file, "rb") as fp:
            ftp.storbinary(cmd=f"STOR {file.name}", fp=fp)
    print("======== 上传后的目录 =========")
    ftp.retrlines('LIST')
