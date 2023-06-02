import os
import shlex
import subprocess
import config
import time


def out_file_cmd_exec(cmd, file_path='log/tool.log'):
    '''执行命令并输出到文件
    :param cmd: 命令
    :param file_path: 文件路径
    :return: 返回执行结果
    '''
    with open(file_path, 'w') as f:
        if os.name == 'nt':
            pass
        else:
            cmd = shlex.split(cmd)
        p = subprocess.Popen(cmd, stdout=f, stderr=f).wait()
        return p


def tail(filepath, n):
    return os.popen("tail -n {} {}".format(n, filepath)).read()


def clear_oneforall_results():
    '''清除oneforall结果'''
    try:
        if os.name == 'nt':
            os.system('del /s /q /a ' + config.ONEFORALL_RESULTS_PATH)
        else:
            os.system('rm -rf ' + config.ONEFORALL_RESULTS_PATH)
    except Exception as e:
        print(e)
        return False

def kill_oneforall():
    os.system(r"ps -ef |grep oneforall |grep -v grep |awk '{print $2}'|xargs kill -9")
    os.system(r"ps -ef |grep massdns |grep -v grep |awk '{print $2}'|xargs kill -9")

def kill_httpx():
    os.system(r"ps -ef |grep httpx |grep -v grep |awk '{print $2}'|xargs kill -9")

def kill_scaninfo():
    os.system(r"ps -ef |grep scaninfo |grep -v grep |awk '{print $2}'|xargs kill -9")

def kill_xray():
    os.system(r"ps -ef |grep xray |grep -v grep |awk '{print $2}'|xargs kill -9")
    time.sleep(1)
    os.system(r"ps -ef |grep xray |grep -v grep |awk '{print $2}'|xargs kill -9")

def kill_crawlergo():
    os.system(r"ps -ef |grep crawlergo |grep -v grep |awk '{print $2}'|xargs kill -9")
    os.system(r"ps -ef |grep chrome |grep -v grep |awk '{print $2}'|xargs kill -9")
    time.sleep(1)
    os.system(r"ps -ef |grep crawlergo |grep -v grep |awk '{print $2}'|xargs kill -9")
    os.system(r"ps -ef |grep chrome |grep -v grep |awk '{print $2}'|xargs kill -9")

def kill_xray_crawlergo():
    kill_xray()
    kill_crawlergo()
    
    