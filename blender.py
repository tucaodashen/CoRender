import requests
from faker import Faker
import sys
import lzma
import os
import tarfile
import shutil

#下载函数
def downlowdBl(url,filename):
    uas = Faker()
    ua = uas.user_agent()
    headers1 = {'user-agent': ua}
    #随机UA
    res = requests.get(url, stream=True,headers=headers1)

    print(res.status_code, res.headers,ua)

    with open(filename, "wb") as file:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
def prepare(filename,unzipdir="unzip",destdir="blender"):
    esidirname = "/" + filename.replace(".tar.xz", "")#避免重复解压
    #创建必要目录
    if os.path.exists(unzipdir):
        pass
    else:
        os.mkdir(unzipdir.replace("/",""))
    if os.path.exists(destdir):
        pass
    else:
        os.mkdir(destdir)
    if os.path.exists(unzipdir +esidirname):
        pass
    else:
        decompress_tar(tar_xz_process(filename), unzipdir)#解压文件
    files = destdir+esidirname
    sorce = unzipdir+esidirname
    print(sorce,files)
    if os.path.exists(files):
        shutil.rmtree(files)
    shutil.move(sorce, files)
def tar_xz_process(save_file_path):
   # xz 解压
   tar_file_path = save_file_path.replace(".tar.xz", ".tar")
   with lzma.open(save_file_path, "rb") as input_:
       with open(tar_file_path, "wb") as f:
           shutil.copyfileobj(input_, f)
   return tar_file_path
def decompress_tar(tar_file_name, dir_name):

    try:
        if not os.path.exists(tar_file_name):
            return False
        tar = tarfile.TarFile(tar_file_name)
        names = tar.getnames()
        #print(names)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        else:
            shutil.rmtree(dir_name)
            os.mkdir(dir_name)
        for name in names:
            tar.extract(name, dir_name)
        tar.close()
        return True
    except Exception as e:
        print(f"文件tar 解压异常。{e} - {tar_file_name}")
    return False
def preparenve(version):
    if version:
        pass

