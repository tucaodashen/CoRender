import os
os.mkdir("blender")
os.mkdir("unzip")
os.mkdir("project")
os.mkdir("project/out")
import gradioui

try:

    gradioui.interface()
except:
    print("启动失败")

