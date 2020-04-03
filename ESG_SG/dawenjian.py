
import re
import sys
import datetime
import getopt

def calculate_dur(file_name, bfp_id):
    fh = open(file_name, 'r')
    start_dt = None
    stop_dt = None

    for line in fh.readlines():
        if start_dt is None:
            ret = re.match(".*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\D(\d{1,4}-0-\d{1,4}).*first time to decode", line)
            if ret is not None:
                if ret.group(2) == bfp_id:
                    print ret.string
                    start_dt = datetime.datetime.strptime(ret.group(1), '%Y-%m-%d %H:%M:%S')

            continue

        if stop_dt is None:
            ret = re.match(".*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).*\D(\d{1,4}-0-\d{1,4}).*begin to merge", line)
            if ret is not None:
                if ret.group(2) == bfp_id:
                    print ret.string
                    stop_dt = datetime.datetime.strptime(ret.group(1), '%Y-%m-%d %H:%M:%S')
                    break

    if start_dt is not None and stop_dt is not None:
        return (stop_dt - start_dt).total_seconds()
    else:
        print "start_dt is %s" % str(start_dt)
        print "stop_dt is %s" % str(stop_dt)
        return None


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hf:i:")
    file_name = None
    bfp_id = None

    for op, value in opts:
        if op == "-h":
            print "Usage:"
            print "python 4ziwei.py -f <file name> -i <ctsid-issid-fid>"

            exit(0)

        elif op == "-f":
            file_name = value
        elif op == "-i":
            bfp_id = value
        else:
            print "python 4ziwei.py -h to get the help info"
            exit(1)

    if file_name is None or bfp_id is None:
        print "please provide a valid paras"
    else:
        dur = calculate_dur(file_name, bfp_id)
        if dur is None:
            print "Something is wrong"
        else:
            print "Duration=%d seconds" % dur
            print "Duration=%d minutes" % (dur/60)