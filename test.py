import os
def get_process_pid(processname):
    """获取进程号"""
    # 进程名称
    # 定义一个空列表，放置按空格切割split(' ')后的进程信息
    process_info_list = []
    # 命令行输入，获取进程信息
    process = os.popen('ps -A | grep %s'% processname)
    # 读取进程信息，获取字符串
    process_info = process.read()
    print(process_info)
    # 按空格切割split(" ")，
    for i in process_info.split(' '):
        # 判断不为空，添加到process_info_list中
        if i != "":
            process_info_list.append(i)
    print(process_info_list)
    # 列表第0位是字符串类型pid，转换成int类型，方便执行stop_process()
    pid = int(process_info_list[0])
    # 返回值是int类型pid
    return pid
