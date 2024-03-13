from utils import db
from models import TaskModels, DomainModels, IPModels, SiteModels, ToolConfModels
from modules.tools import out_file_cmd_exec
# import config
import json
import os
import IPy
import netaddr


def scaninfo_module(task_id):
    print(f'[+] scaninfo_module正在运行，任务ID: {task_id}')
    scaninfo_conf = ToolConfModels.query.filter_by(
        tool_name='scaninfo').first()
    scaninfo_cmd = scaninfo_conf.tool_cmd
    scaninfo_log_path = scaninfo_conf.tool_log_path
    scaninfo_result_path = scaninfo_conf.tool_result_path
    scaninfo_update_sh = scaninfo_conf.tool_update_sh
    scaninfo_portscan_range = json.loads(scaninfo_conf.tool_others)

    scaninfo_task = TaskModels.query.filter_by(task_id=task_id).first()

    try:
        scan_ports = scaninfo_portscan_range[scaninfo_task.task_portscan_range]
    except:
        scan_ports = scaninfo_task.task_portscan_range

    ip_list = []
    c_duan = []

    if scaninfo_task.task_target_type != "ip":
        print(f'[-] 任务：{task_id} 不是ip，无须进行端口扫描，正在查找是否存在可以扫描的子域名IP')
    else:
        print("[+] 任务：{} 开始进行C段整理".format(task_id))
        ip_list.append(scaninfo_task.task_target)
        # 将目标ip加入c段列表
        for ip in ip_list:
            # print(ip)
            if '-' in ip:
                c_duan.append(
                    str(IPy.IP(ip.split('-')[0]).make_net('255.255.255.0')))
            elif '/' in ip:
                c_duan.append(ip)
            else:
                c_duan.append(str(IPy.IP(ip).make_net('255.255.255.0')))

    # 查一查有无子域名扫描结果的ip，也加入c段和ip列表
    subdomain_ips = DomainModels.query.filter_by(task_id=task_id)
    # print(subdomain_ip.count())
    # 输入目标的c段计数，如果c段过多的话，在下面的scaninfo模块就需要分段进行，及时保存结果
    # count_target_c_duan = 0
    if subdomain_ips.count() > 0:
        subdomain_ips = subdomain_ips.all()
        for subdomain_ip in subdomain_ips:
            try:
                if netaddr.IPNetwork(subdomain_ip.domain_record):
                    c_duan.append(
                        str(
                            IPy.IP(subdomain_ip.domain_record).make_net(
                                '255.255.255.0')))
                    ip_list.append(subdomain_ip.domain_record)
            except Exception as e:
                # CNAME不管了
                continue

    # 列表去重
    c_duan = list(set(c_duan))
    ip_list = list(set(ip_list))

    if ip_list == []:
        print(f"[-] 任务{task_id}不存在需要扫描的IP，跳过scaninfo模块")
        return

    # c段数据入库
    try:
        task_db = TaskModels.query.filter_by(task_id=scaninfo_task.task_id)
        task_db.update({"task_c_duan": json.dumps(c_duan)})
        db.commit()
    except Exception as e:
        print("[!] 任务：{} 的scaninfo模块C段整理入库失败".format(task_id))
        raise

    # print(ip_list)
    print("[+] 任务：{} 的C段整理和ip去重工作完成，开始运行scaninfo".format(task_id))

    # scaninfo模块的日志和结果文件是一个
    result_file = os.path.join(scaninfo_result_path, "portscan_result")
    os.system("echo '' > {}.txt".format(result_file))
    for ip in ip_list:
        # 开始scaninfo模块任务
        # 清空结果文件
        os.system("echo '' > {}.txt".format(result_file))
        print("[+] IP：{} 开始使用scaninfo扫描".format(ip))
        cmd = scaninfo_cmd.format(target_ip=ip,
                                  ports=scan_ports,
                                  result_file=result_file)
        cmd_result = out_file_cmd_exec(cmd, '/dev/null')
        # cmd_result = 0
        if cmd_result == 0:
            print("[+] IP:{} scaninfo扫描完成，开始读取结果".format(ip))
            scaninfo_result = []
            with open(result_file + ".txt", 'r', encoding='utf-8') as f:
                for i in f.readlines():
                    scaninfo_result.append(json.loads(i))
            # 将结果插入数据库
            if len(scaninfo_result) == 0:
                print("[!] IP：{} 的scaninfo扫描完成，但没有发现开放端口".format(ip))
                continue

            for result in scaninfo_result:
                if 'ip' in result:
                    try:
                        target_db = IPModels(
                            task_id=scaninfo_task.task_id,
                            ip=result['ip'],
                            port=result['port'],
                            service=result['service'],
                            banner=result['Banner'],
                        )
                        db.add(target_db)
                        db.commit()
                    except Exception as e:
                        print("[!] IP:{} 的scaninfo扫描结果入库失败".format(ip))
                        raise
                elif 'url' in result:
                    try:
                        target_db = SiteModels(
                            task_id=scaninfo_task.task_id,
                            url=result['url'],
                            ip=result['url'].replace("http://", "").replace(
                                "https://", "").split("/")[0],
                            status_code=result['StatusCode'],
                            title=result['Title'],
                            finger=result['HeaderDigest'] + "\n" +
                            result['KeywordFinger'] + "\n" +
                            result['HashFinger'],
                        )
                        db.add(target_db)
                        db.commit()
                    except Exception as e:
                        print("[!] IP：{} 的scaninfo扫描结果入库失败".format(ip))
                        raise
            print("[+] IP：{} scaninfo模块结果入库完成".format(ip))
        else:
            print("[!] IP：{} 的scaninfo模块失败，scaninfo模块期间出现错误，subprocess返回值不为0".
                  format(ip))
            continue
