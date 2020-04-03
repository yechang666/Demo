
# -- coding: utf-8 --
import sys
import os
import getopt
import json
import datetime
import time
from collections import defaultdict
import paramiko


class ExecShellBySSH(object):
    def __init__(self, hostIp):
        self.hostIp = hostIp
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.load_system_host_keys()
        self.client.connect(self.hostIp)

    def __del__(self):
        self.client.close()

    def execCmd(self, cmd):
        stdin, stdout, stderr = self.client.exec_command(cmd)
        stdin.close()

        ret_stdput = stdout.read()
        ret_stderr = stderr.read()

        print "stdout: %s" % ret_stdput
        print "stderr: %s" % ret_stderr

        return ret_stdput


def store(file_name, data):
    with open(file_name, 'w') as json_file:
        json_file.write(json.dumps(data, indent=2))


def load(file_name):
    with open(file_name) as json_file:
        data = json.load(json_file)
        return data


# def convert_datetime_to_str(dt):
#     dt_str = "%d-%02d-%02dT%02d:%02d:%02d+08:00" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
#     return dt_str


def update_config(file_name):
    data = load(file_name)

    # 计算valid_duration的时间区间
    # vd_start = datetime.datetime.strptime(data["bfpworkers_config"]["valid_duration"]["start"], '%Y-%m-%dT%H:%M:%S+08:00')
    # vd_stop  = datetime.datetime.strptime(data["bfpworkers_config"]["valid_duration"]["stop"], '%Y-%m-%dT%H:%M:%S+08:00')
    # valid_duration = vd_stop - vd_start
    #
    # # 更新valid_duration
    # new_vd_start = d_start
    # new_vd_stop  = new_vd_start + valid_duration
    #
    # data["bfpworkers_config"]["valid_duration"]["start"] = convert_datetime_to_str(new_vd_start)
    # data["bfpworkers_config"]["valid_duration"]["stop"] = convert_datetime_to_str(new_vd_stop)

    # 更新每个pid下的每个fid中的start和duration
    for pid in data["bfpworkers_config"]["pids"]:
        conf = pid_durs[str(pid["pid"])]
        fid_init_val = 1
        for fid in pid["tids"][0]["fids"]:
            fid["fid"] = fid_init_val
            fid_init_val += 1

        # if pid["pid"] not in conf["continue_pids"]:     # pid下面的fid的推送时间不连续
        #     for fid in pid["tids"][0]["fids"]:
        #         if str(fid["fid"]) in conf: # 单独指定了这个fid中的各个条目的duration
        #             i = 0
        #             if len(fid["carousel_info"]) != len(conf[str(fid["fid"])]):
        #                 print "在PID=%d,FID=%d的carousel_info中有%d个条目，但是指定的duration个数是%d" % \
        #                       (pid["pid"], fid["fid"], len(fid["carousel_info"]), len(conf[str(fid["fid"])]))
        #                 return
        #
        #             for carousel in fid["carousel_info"]:
        #                 c_start = datetime.datetime.strptime(carousel["start"], '%Y-%m-%dT%H:%M:%S+08:00')
        #                 new_c_start = new_vd_start + (c_start - vd_start)
        #                 carousel["start"] = convert_datetime_to_str(new_c_start)
        #                 carousel["duration"] = conf[str(fid["fid"])][i]
        #                 i += 1
        #         else:
        #             for carousel in fid["carousel_info"]:
        #                 c_start = datetime.datetime.strptime(carousel["start"], '%Y-%m-%dT%H:%M:%S+08:00')
        #                 new_c_start = new_vd_start + (c_start - vd_start)
        #                 carousel["start"] = convert_datetime_to_str(new_c_start)
        #                 carousel["duration"] = conf["default"]
        # else:   # pid下面的fid的推送时间连续
        #     last_start = None
        #     last_duration = None
        #
        #     for fid in pid["tids"][0]["fids"]:
        #         if str(fid["fid"]) in conf: # 单独指定了这个fid中的各个条目的duration
        #             i = 0
        #             for carousel in fid["carousel_info"]:
        #                 if last_start is None:
        #                     c_start = datetime.datetime.strptime(carousel["start"], '%Y-%m-%dT%H:%M:%S+08:00')
        #                     new_c_start = new_vd_start + (c_start - vd_start)
        #                     carousel["start"] = convert_datetime_to_str(new_c_start)
        #                     carousel["duration"] = conf[str(fid["fid"])][i]
        #                     last_start = new_c_start
        #                     last_duration = conf[str(fid["fid"])][i]
        #                     i += 1
        #                 else:
        #                     new_c_start = last_start + datetime.timedelta(seconds=last_duration)
        #                     carousel["start"] = convert_datetime_to_str(new_c_start)
        #                     last_start = new_c_start
        #                     last_duration = conf[str(fid["fid"])][i]
        #                     i += 1
        #
        #         else:
        #             for carousel in fid["carousel_info"]:
        #                 if last_start is None:
        #                     c_start = datetime.datetime.strptime(carousel["start"], '%Y-%m-%dT%H:%M:%S+08:00')
        #                     new_c_start = new_vd_start + (c_start - vd_start)
        #                     carousel["start"] = convert_datetime_to_str(new_c_start)
        #                     carousel["duration"] = conf["default"]
        #                     last_start = new_c_start
        #                     last_duration = conf["default"]
        #                 else:
        #                     new_c_start = last_start + datetime.timedelta(seconds=last_duration)
        #                     carousel["start"] = convert_datetime_to_str(new_c_start)
        #                     carousel["duration"] = conf["default"]
        #                     last_start = new_c_start
        #                     last_duration = conf["default"]


    store(file_name, data)

# {
# 	'1002': {
# 		'default': 3600
# 	},
# 	'1001': {
# 		'default': 3600,
# 		'1': [300,
# 		500],
# 		'2': [300,
# 		500]
# 	}
# }

# def generate_durs( pid_durs, continue_pids ):
#     para_list = pid_durs.split()
#
#     c_pids = []
#     if continue_pids is not None:
#         continue_pids_list = continue_pids.split(",")
#         for pid in continue_pids_list:
#             c_pids.append(int(pid))
#
#     result = {}
#
#     for para in para_list:
#         item_list = para.split(":")
#         if len(item_list) == 2:     #未指定fid
#             if item_list[0] in result:
#                 result[item_list[0]]["default"] = int(item_list[1])
#                 result[item_list[0]]["continue_pids"] = c_pids
#
#             else:
#                 result[item_list[0]] = {}
#                 result[item_list[0]]["default"] = int(item_list[1])
#                 result[item_list[0]]["continue_pids"] = c_pids
#         else:
#             dur_list = item_list[2].split(",")
#             for dur in dur_list:
#
#                 if item_list[0] not in result:
#                     result[item_list[0]] = {}
#
#                 if item_list[1] in result[item_list[0]]:
#                     result[item_list[0]][item_list[1]].append(int(dur))
#                 else:
#                     result[item_list[0]][item_list[1]] = []
#                     result[item_list[0]][item_list[1]].append(int(dur))
#
#     # verify the json format
#     for pid, info in result.items():
#         if "default" not in info:
#             print "lost default duration for pid %s" % pid
#             return None
#
#     return result


# def clean_all_db_file():
#
#     # get all db file names
#     # shell = ExecShellBySSH(woker_serv_ip)
#     # file_names = shell.execCmd("cd /opt/fes/conf/; ls -l *.db | awk '{print $9}'")
#     # file_names = file_names.strip().split("\n")
#     #
#     # for file_name in file_names:
#     #     full_file_name = "/opt/fes/conf/" + file_name
#     #
#     #     ctsid = file_name.split(".")[0].split("_")[0]
#     #
#     #     db_content = """{\"ctsId\" : %s,\"issId\" : 0,\"runInfo\" : []}""" % ctsid
#     #
#     #     shell.execCmd("echo '%s' > %s" % (db_content, full_file_name))
#
#     for root, dirs, files in os.walk("/opt/fes/conf/"):
#
#         for filename in files:
#             print filename
#             if not filename.endswith(".db"):
#                 continue
#             ctsid = filename.split(".")[0].split("_")[0]
#             fullname = os.path.join(root, filename)
#
#             print fullname
#
#             fopen = open(fullname, 'w')
#             fopen.write("""{\"ctsId\" : %s,\"issId\" : 0,\"runInfo\" : []}""" % ctsid)
#             fopen.close()



if __name__ == "__main__":

    print "#"*16
    print "NOTE: please stop all of bfpworkers and bfpscheduler before running this script"
    print "#" * 16

    # set default value
    d_start = ""
    pid_durs = ""
    file_name = ""
    time_continue_pids = ""
    # bianliang = ['-f','C:/Users/Administrator/Desktop/bigfile_test/bfpscheduler.json','--d_start','2018-10-18 17:00:00','--pid_durs','1001:7200 1002:7200','--time_continue','1001,1002']
    # opts, args = getopt.getopt(sys.argv[1:], "hf:", ["d_start=", "pid_durs=", "time_continue="])
    opts, args = getopt.getopt(bianliang, "hf:", ["d_start=", "pid_durs=", "time_continue="])
    for op, value in opts:
        if op == "-h":
            print "Usage:"
            print "python updatebfpscheduler-3.1.py [options]"
            print "-h   显示该帮助信息"
            print "--d_start   设置bfp总体的开始推送日期和时间， 例如  --d_start '2017-12-22 09:00:00',引号是必须的"
            print "--pid_durs   每个pid下的所有fid的duration。 当一个carousel_info中有多个条目，如果所有条目的中duration相" \
                  "同则不需要特殊处理。如果条目间的duration不同，则需要为每个条目提供单独的duration。" \
                  "例子 " \
                  " '1001:3600' 所有fid下的所有条目duration都是3600" \
                  " '1001:3600 1001:1:300,500' 对于pid 1001下的所有fid都使用3600duration，除了fid 1. fid 1，拥有2个条目，" \
                  "第一个条目的duration是300， 第二个条目的duration是500"
            print "--time_continue  指定那些pid中，所有fid的推送都是连续的，中间没有空档期， 例子： --time_continue 1001,1002"

            exit(0)
        elif op == "-f":
            file_name = value
        # elif op == "--d_start":
        #     d_start = value
        # elif op == "--pid_durs":
        #     pid_durs = value
        # elif op == "--time_continue":
        #     time_continue_pids = value
        else:
            print "Run python updatebfpscheduler-3.1.py -h to get the help info"
            exit(1)

    # if d_start != "":
    #     d_start = datetime.datetime.strptime(d_start, '%Y-%m-%d %H:%M:%S')
    # else:
    #     print "Please provide the d_start"
    #     exit(2)
    #
    # if pid_durs != "":
    #     if time_continue_pids != "":
    #         pid_durs = generate_durs(pid_durs, time_continue_pids)
    #     else:
    #         pid_durs = generate_durs(pid_durs, None)
    # else:
    #     print "Please provide the pid_dur"
    #     exit(3)


    if file_name == "":
        print "Please provide the file_name"
        exit(2)

    # if pid_durs is None:
    #     print "The input parameter about pid_durs lost the default duration"
    #     exit(5)

    # update_config(file_name, d_start, pid_durs)
        update_config(file_name)
    # clean_all_db_file()

