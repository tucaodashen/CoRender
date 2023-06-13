import os
import subprocess
from  subprocess import check_output
import numpy as np
from PIL import Image
import re

metkey = ["Fra","帧号"]



def is_field_in_list(source_data, field_list):
  for field in field_list:
    if field in source_data:
      return True
  return False


def get_pid(name):
    try:
        pidl = list(map(int, check_output(["pidof", name]).split()))
        return pidl[0]
    except:
        return 0
def rendercommand(
        blenderdir=None,
        porjectfile="test.blend",

        startframe=0,
        endframe=250,
        framestep=1,
        filename="#####",
        filesort="PNG",
        engline="BLENDER_EEVEE",
        threads=0,
        amine=True,
        defult=True,
        ispreview=False,
        device="CUDA"
):
    tim = ""
    sumtime = ""
    framenumber = ""
    imagepath=""
    read=False
    for file in os.listdir('project/out/'):
        os.remove(os.path.join('project/out/', file))
    image_arr = np.zeros((1,1),np.uint8)
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    if amine:#确认渲染格式
        suffix=" -a,"
    else:
        suffix=" -f"+" "+str(int(startframe))
    head=str(current_file_path)+"/blender/"+str(blenderdir).replace("\\","/")+"/"+"blender"+" -b"
    if defult:
        backpart =" -t "+str(threads)+" -o"+" "+"//"+"out/"+str(filename)+" -F"+" "+filesort+" -x 1"
    else:
        if False:
            pass
            #backpart = " -E" + " " + engline + " -s" + " " + str(startframe) + " -S" + " " + str(scene) + " -e" + " " + str(endframe) + " -t" + " " + str(threads) + " -o" + " " + "//" + "out/" + str(filename) + " -F" + " " + filesort + " -x 1"
        else:
            backpart = " -E" + " " + engline + " -s" + " " + str(int(startframe)) + " -e" + " " + str(int(endframe)) + " -t" + " " + str(int(threads)) + " -o" + " " + "//" + "out/" + str(filename) + " -F" + " " + filesort + " -x 1"
    if framestep !=1:
        backpart= backpart+" -j"+" "+str(framestep)
    front = " "+str(current_file_path)+"/project/"+str(porjectfile)
    comline = str(head)+str(front)+str(backpart)+str(suffix)
    if engline=="CYCLES":
        if device!="CPU":
            comline = comline + " -- --cycles-device " + device
        else:
            comline=comline
    else:
        comline = comline
    cmd = comline.replace(",","")
    code = "utf8"
    if amine != True:
        solo=True
    else:
        solo=False
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            ana = str(line.decode(code, 'ignore'))
            matresult = is_field_in_list(ana, metkey)
            state = ""

            if matresult:
                state = "渲染中"
                if is_field_in_list(ana, ["帧号"]):
                    startindex = ana.find("帧号")
                    endindex = ana.find("| 内存")
                    framenumber = int(ana[startindex + 3:endindex])
                else:
                    startindex = ana.find("Fra")
                    endindex = ana.find("Mem")
                    framenumber = int(ana[startindex+4:endindex])
            else:
                state = str("准备中")
                end=ana+"114514"
                if is_field_in_list(ana,["Saved"]):
                    imagepath = ana[int(ana.find("Saved: '")) + 9:end.find("114 514")]
                    imagepath = "/"+imagepath
                    read = os.path.exists(imagepath)
                    if read and ispreview:
                        preview = Image.open(imagepath)
                        image_arr = np.array(preview)
                if is_field_in_list(ana, ["Time", "Saving"]):

                    minute = int(ana[6:8])
                    secone = float(ana[9:14])
                    tim = secone + 60 * minute

                    if solo:
                        sumtime = tim
                    else:
                        sumtime = (tim * (endframe - startframe)) / 60



            while True:

                if get_pid("blender")==0:
                    state="渲染完成"
                    yield ana, state, tim, sumtime, framenumber, image_arr
                    break
                else:


                    print(line.decode(code, 'ignore'), matresult, state, tim, sumtime, framenumber,read)
                    print(imagepath)
                    yield ana, state, tim, sumtime, framenumber,image_arr

                    break
