import os
if os.path.exists("blender"):
    pass
else:
    os.mkdir("blender")
if os.path.exists("unzip"):
    pass
else:
    os.mkdir("unzip")
if os.path.exists("project"):
    pass
else:
    os.mkdir("project")
if os.path.exists("project/out"):
    pass
else:
    os.mkdir("project/out")
import gradioui



gradioui.interface()


