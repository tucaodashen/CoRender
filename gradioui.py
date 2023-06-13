import gradio as gr
import os
import command
import blender
import synthesis
blenderversion = os.listdir("blender")
project = os.listdir("project")

choseblender = [
    "2.83LTS",
    "2.93LTS",
    "3.3LTS",
    "3.5",
    "3.4",
    "3.3",
    "3.2",
    "3.1",
    "3.0",
    "2.9",
    "2.8",
]
fileso=[
    "TGA",
    "RAWTGA",
    "JPEG",
    "IRIS",
    "IRIZ",
    "AVIRAW",
    "AVIJPEG",
    "PNG",
    "BMP"
        ]
device=[
    "CUDA",
    "OPTIX",
    "CPU"
]
def interface():
    with gr.Blocks(theme=gr.themes.Soft()) as application:

        gr.Markdown("blender自动化云渲染WebUI")
        with gr.Tab("渲染"):
            with gr.Column():
                gr.Markdown("采用工程中的设置？这会导致下列设置中除线程，文件名，文件类型外所有设置失效")
                with gr.Row():
                    isdefult = gr.Checkbox(label="采用工程中设置？",)
                    ispreview = gr.Checkbox(label="开启预览？",info="不建议，会导致程序卡顿与判断错误" )
                with gr.Row():
                    ani = gr.Checkbox(label="渲染动画？")
                    fil = gr.Dropdown(blenderversion,label="选择渲染版本",value=blenderversion[0])
                    pro = gr.Dropdown(choices=project,value=project[0],label="选择工程文件")
                    filename = gr.Textbox(info="选择保存文件的文件名（不包含扩展名）",label="文件名")
                    filesort = gr.Dropdown(fileso,info="文件的可选类型,AVIRAW,AVIJPEG为视频格式",label="文件类型",value=fileso[2])
                    thread = gr.Slider(0,128,step=1,interactive=True,info="渲染线程，0为使用全部线程",label="渲染线程")

                    with gr.Row():
                        referesh = gr.Button(value="刷新", variant="primary")
                starframe = gr.Number(step=1,interactive=True, label="起始帧",info="渲染开始的帧数")
                endframe = gr.Number(step=1, interactive=True, label="结束帧",info="渲染结束的帧数")
                step = gr.Number(step=1, interactive=True, label="步长", info="默认为1")
                engine = gr.Dropdown(["CYCLES","BLENDER_EEVEE"],info="选择渲染引擎,注意！！！blender3.4以下版本无法使用EEVEE作为渲染引擎",label="渲染引擎",value="CYCLES")
                cuda = gr.Dropdown(device,info="用于渲染加速的设备（仅CYCLES下生效，EEVEE会自动选择，在不发生错误的情况下）", label="选择渲染设备",value=device[0])
            with gr.Row():
                start = gr.Button("启动")
            with gr.Row():
                with gr.Row():
                    preview = gr.Image()
                with gr.Row():
                    renderlog = gr.Textbox(info="原始日志",label="日志")
                    state = gr.Textbox(info="渲染器状态（准备/渲染）", label="渲染状态")
                    framenum = gr.Textbox(info="当前帧号", label="帧号")
                    solotime = gr.Textbox(info="单帧所用时间（秒）", label="单帧时间")
                    sumtime = gr.Textbox(info="渲染总用时(分钟)", label="总时间")

        with gr.Tab("Blender版本管理"):
            with gr.Row():
                with gr.Column():
                    gr.Markdown("可选版本")
                    with gr.Column():
                        version = gr.Dropdown(choseblender,label="Blender版本",)
                        with gr.Row():
                            vdownload = gr.Button("下载")
                        with gr.Column():
                            downlog = gr.TextArea(label="结果")
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("""自定义Blender版本
                                        """)
                            with gr.Row():

                                url = gr.Textbox(label="文件链接",info="请务必确定此链接不会被重定向且下载的的确为文件，否则可能会造成未知错误")
                                log = gr.TextArea(info="日志")
                                download = gr.Button("开始下载")
        with gr.Tab("合成"):
            with gr.Column():
                gr.Markdown("使用FFmpeg对输出的序列桢进行合成")
                audio = gr.Audio(label="音频",type="filepath",info="不上传默认无音频(MP3格式)")
                inputname=gr.Textbox(label="输入文件名",info="你渲染时保存的文件名（不带后缀）")
                inputsort=gr.Dropdown([".png",".jpg"],label="输入文件类型",info="你渲染时保存的文件类型")
                outname=gr.Textbox(label="输出文件名",info="自定义，不必带后缀")
                rate=gr.Number(value=30,step=1,label="视频输出帧率",info="应等与你渲染设置中的帧率")
                mbps=gr.Number(label="视频码率",info="单位为Mbps")
                sysst=gr.Button("开始")
                relog=gr.Textbox(label="输出",info="无报错则为成功")

        start.click(command.rendercommand,[fil,pro,starframe,endframe,step,filename,filesort,engine,thread,ani,isdefult,ispreview,cuda],[renderlog,state,solotime,sumtime,framenum,preview])

        def refreshdir(dirname="blender"): #获取版本
            global model
            blenderversion = os.listdir("blender")
            return fil.update(choices=blenderversion, value=blenderversion[0])
        referesh.click(fn=refreshdir,inputs=url,outputs=fil)
        vdownload.click(blender.preve,version,downlog)
        download.click(blender.manulpreve,[url],[log])
        sysst.click(synthesis.commandffmpeg,[inputname,mbps,outname,inputsort,rate,audio],[relog])
        application.queue()
        application.launch(share=True,server_port=6006,)