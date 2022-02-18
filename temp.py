import os, datetime, subprocess

'''
这个程序能运行额外的系统指令，只需要将要运行的系统指令保存在cmd_cmd文件中
以utf-8编码，例如：
cmd_cmds:
    git add --all
    git commit -m ""
    git push
然后运行该程序，就能借由运行上述的系统指令了。
如果想在运行中对这些指令进行二次处理，譬如，往git commit -m ""这的双引号
添加信息，可以另做cmd_sec_operate_script.py文件，将所要对指令处理的操作
写在里面。
cmd_sec_operate_script.py(框架)：
    if len(sys.argv) >= 2:
        cmd = ' '.join(sys.argv[1:]).strip() # 取出指令
        cmd = operate_cmd(cmd) # 对指令进行二次操作    
        print(cmd) # 要通过print将处理完的指令传回去
'''

def operate_command_with_outer_script(cmd):
    script = 'cmd_sec_operate_script.py'
    if os.path.exists(script):
        cmd = subprocess.Popen("python %s %s"%(script, cmd), encoding='utf-8', shell=True, stdout=subprocess.PIPE)
        cmd.wait()
        return cmd.stdout.read()
    return cmd

def operate_command():
    with open('cmd_cmds', 'r', encoding='utf-8') as f:
        cmds = f.readlines()
    for cmd in cmds:
        cmd = cmd.strip()
        if cmd:
            cmd = operate_command_with_outer_script(cmd)
            print("更改后的命令", cmd)
            os.system(cmd)

if __name__ == '__main__':
    starttime = datetime.datetime.now()
    localpath = os.path.abspath('./')
    print("当前路径是", localpath)
    operate_command()

    endtime = datetime.datetime.now()
    print("耗时：", (endtime - starttime).seconds, '秒')