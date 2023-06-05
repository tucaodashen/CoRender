import os
import sys
import subprocess
co = "F:/Users/27698/PycharmProjects/corender/blender/blender.exe -b D:\March7th\March7th.blend -o F:\SteamLibrary\steamapps\common\Blender/frame_##### -F OPEN_EXR -a -E BLENDER_EEVEE -t 1"

#@staticmethod
def __external_cmd(cmd, code="utf8"):
  print(cmd)
  process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  while process.poll() is None:
    line = process.stdout.readline()
    line = line.strip()
    if line:
      print(line.decode(code, 'ignore'))
s

#出自https://www.php1.cn/detail/Python3_ZhiXingX_7aa05b05.html
#感谢大佬