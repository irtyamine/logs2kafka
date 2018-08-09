import time
import datetime
import socket
import json
from mykafka import MyKafka


def parse_log_line(line):
    strptime = datetime.datetime.strptime
    hostname = socket.gethostname()
    time = line.split(' ')[3][1::]
    entry = {}
    entry['datetime'] = strptime(
        time, "%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M")
    entry['source'] = "{}".format(hostname)
    entry['type'] = "www_access"
    entry['log'] = "'{}'".format(line.rstrip())
    return entry


def show_entry(entry):
    temp = ",".join([
        entry['datetime'],
        entry['source'],
        entry['type'],
        entry['log']
    ])
    log_entry = {'log': entry}
    temp = json.dumps(log_entry)
    print("{}".format(temp))
    return temp


def follow(syslog_file):
    syslog_file.seek(0, 2)
    #pubsub = MyKafka(["mslave2.admintome.lab:31000"])
    ubsub = MyKafka(["192.168.1.240:9092"])
    while True:
        line = syslog_file.readline()
        if not line:
            time.sleep(0.1)
            continue
        else:
            entry = parse_log_line(line)
            if not entry:
                continue
            json_entry = show_entry(entry)
            pubsub.send_page_data(json_entry, 'www_logs')


f = open("/var/log/apache2/access.log", "rt")
follow(f)
