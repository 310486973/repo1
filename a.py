[root@10 /home/oicq/argus/CapServer]# cat cap.py
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#私有化本地抓包工具

import os,time,sys,subprocess
import getopt
import datetime
import json

VER = "2.0"


def usage():
    print("""Usage: {0} OPTS [OPTS]...
        OPTS:
            --help,-h           #显示帮助
            --num,-n  <count>   #指定抓包数量,默认10000
            --time,-t <second>  #指定抓包时常,默认600
            --exp,-e  <exp>     #使用行选择组件表达式过滤,默认为空
            --srcip   <ip>      #指定源ip,    默认为所有ip都会抓取
            --srcport <port>    #指定源端口,  默认为所有端口都会抓取
            --dstip   <ip>      #指定目标ip,  默认为所有ip都会抓取
            --dstport <port>    #指定目标端口,默认为所有端口都抓取
            --ipv     <int>     #指定IP协议版本,默认4

            所有参数都是可选的,但是至少指定一种参数,所有参数都是并且的关系.
        EXAMPLES:
            1. 过滤源ip为10.0.1.2的所有包
                {0} --srcip 10.0.1.2

            2. 过滤源ip为10.0.1.2 并且 目的ip为10.0.3.3 的包
                {0} --srcip 10.0.1.2 --dstip 10.0.3.3

            3. 过滤源ip为10.0.1.2 并且 目的ip为10.0.3.3 的包 抓1000个包
                {0} --srcip 10.0.1.2 --dstip 10.0.3.3 --num 10000

            4. 过滤源ip为10.0.1.2 并且 目的端口80 的包 抓100个包
                {0} --srcip 10.0.1.2 --dstport 80 --num 100

            5. 抓源ip为10.0.1.2 或者源ip为 10.0.2.2 的包
                {0}  --exp 'ip.src=167772418||ip.src=167772674'
        NOTES:
            脚本会调用CapServer抓包,抓包文件路径为/data/ids_pcap/
        VERSION: {1}
    """.format(sys.argv[0], VER))


def get_default_opts(taskId):
    opts = {
        "num": "10000",
        "timeout": "600",
        "srcip": "",
        "srcport": "0",
        "dstip": "",
        "dstport": "0",
        "ipv": "IPV4",
        "online": "1",
        "proto": "ALL",
        "floodtype": "MANUAL",
        "timestamp": int(taskId),
        "taskid": taskId,
        "idsip": "10.26.232.35",
    }

    return opts


def main():
    opts = None

    try:
        opts, _a = getopt.getopt(sys.argv[1:],
                                 "hn:t:e:",
                                 ["help","num=","time=","exp=","srcip=","srcport=","dstip=","dstport=","timestamp=","ipv="])
    except Exception as e:
        print("Bad cmd, {}\n".format(e))
        usage()
        exit(1)
    if len(opts) < 1:
        usage()
        exit(0)

    taskId = str(int(time.time()))
    args = get_default_opts(taskId)

    for n, v in opts:
        if n in ["-h", "--help"]:
            usage()
            exit(0)
        elif n in ["-n", "--num"]:
            args["num"] = v
        elif n in ["-t","--time"]:
            args["timeout"] = v
        elif n in ["-e","--exp"]:
            args["floodtype"] = "CUSTOMEXP"
            args["exp"] = v
        elif n == "--srcip":
            args["srcip"] = v
        elif n == "--srcport":
            args["srcport"] = v
        elif n == "--dstip":
            args["dstip"] = v
        elif n == "--dstport":
            args["dstport"] = v
        elif n == "--timestamp":
            args["timestamp"] = int(v)
            args["taskid"] = str(v)
        elif n == "--ipv":
            if int(v) == 4:
                args["ipv"] = "IPV4"
            elif int(v) == 6:
                args["ipv"] = "IPV6"
            else:
                print("Unknown ipv:{}".format(v))
                usage()
                exit(0)
        else:
            print("Unknown opts:{}".format(n))
            usage()

    print(args)
    os.system("mkdir -p /data/ids_pcap")
    subprocess.call(['/home/oicq/argus/CapServer/bin/CapServer',
                     '-i',
                     json.dumps(args),
                     '-f',
                     '/home/oicq/argus/CapServer/conf/CapServer.conf',
                     '-n'])


if __name__ == '__main__':
    main()
