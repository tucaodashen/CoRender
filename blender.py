import bz2
import lzma
import os
import tarfile
import shutil
import download
import  command
url=[
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender2.83/blender-2.83.20-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender2.93/blender-2.93.18-linux-x64.tar.xz",
    "http://mirrors.aliyun.com/blender/release/Blender3.3/blender-3.3.6-linux-x64.tar.xz?spm=a2c6h.25603864.0.0.48a728f1HScmFm",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender3.5/blender-3.5.1-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender3.4/blender-3.4.1-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender3.3/blender-3.3.7-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender3.2/blender-3.2.2-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender3.1/blender-3.1.2-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender3.0/blender-3.0.1-linux-x64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender2.90/blender-2.90.1-linux64.tar.xz",
    "https://mirrors.tuna.tsinghua.edu.cn/blender/blender-release/Blender2.80/blender-2.80rc3-linux-glibc217-x86_64.tar.bz2",
]
#构建工作目录
def prepare(filename,unzipdir="unzip",destdir="blender"):
    if filename=="":
        return False
    else:
        try:
            if command.is_field_in_list(filename,[".tar.bz2"]):
                esidirname = "/" + filename.replace(".tar.bz2", "")
            else:
                esidirname = "/" + filename.replace(".tar.xz", "")  # 避免重复解压
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
                if command.is_field_in_list(filename,["tar.bz2"]):
                    decompress_tar(tar_bz2_process(filename),unzipdir)
                else:
                    decompress_tar(tar_xz_process(filename), unzipdir)#解压文件
            files = destdir+esidirname
            sorce = unzipdir+esidirname
            print(sorce,files)
            if os.path.exists(files):
                shutil.rmtree(files)
            shutil.move(sorce, files)
            if os.path.exists("project"):
                pass
            else:
                os.mkdir("project")
            if os.path.exists("project/out"):
                pass
            else:
                os.mkdir("project/out")

            return True
        except:
            return False
#解压文件
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


def tar_bz2_process(save_file_path):
   """.tar.bz2 文件处理"""
   tar_file_path = save_file_path.replace(".tar.bz2", ".tar")
   bz2_obj = bz2.BZ2File(save_file_path)
   with open(tar_file_path, "wb") as f:
       f.write(bz2_obj.read())
   bz2_obj.close()
   return tar_file_path

def preve(version):
    if version=="2.83LTS":
        dourl=url[0]
    elif version=="2.93LTS":
        dourl=url[1]
    elif version=="3.3LTS":
        dourl=url[2]
    elif version=="3.5":
        dourl=url[3]
    elif version=="3.4":
        dourl = url[4]
    elif version=="3.3":
        dourl = url[5]
    elif version=="3.2":
        dourl = url[6]
    elif version=="3.1":
        dourl=url[7]
    elif version=="3.0":
        dourl = url[8]
    elif version=="2.9":
        dourl = url[9]
    elif version=="2.8":
        dourl = url[10]
    try:
        filename = download.download(dourl)
        prepare(filename)
        return "准备就绪"
    except:
        return "出现错误，请查看命令行输出"
def manulpreve(dourl):
    try:
        filename = download.download(dourl)
        prepare(filename)
        return "准备就绪"
    except:
        return "出现错误，请查看命令行输出"
