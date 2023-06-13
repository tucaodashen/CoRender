import os
import subprocess
def commandffmpeg(
        filename="",
        mbps="10",
        outname="output",
        filesort=".jpg",
        framerate=30,
        audio="1",
):
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    if audio!=None:
        comm="ffmpeg -threads 2 -y -r "+str(framerate)+" -f image2 -i "+str(current_file_path)+"/project/out/"+str(filename)+"%04d"+str(filesort)+" -i "+str(audio)+" -b:v "+str(mbps)+"M "+str(outname)+".mp4"
        print(comm)
    else:
        comm="ffmpeg -threads 2 -y -r "+str(framerate)+" -f image2 -i "+str(current_file_path)+"/project/out/"+str(filename)+"%04d"+str(filesort)+" -b:v "+str(mbps)+"M "+str(outname)+".mp4"
    cmd=comm
    code="utf8"
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            print(line.decode(code, 'ignore'))
            log=str(line.decode(code, 'ignore'))
            yield log