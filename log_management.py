import json
import datetime
import time
from pprint import pprint

def make_the_log_list(log_file_path, microservice_name):
  with open(log_file_path, "r") as file:
      for line in file:
          if line[0]!='{':
            continue
          my_obj = json.loads(line)
          temp_list = {}
          temp_list["ts"]=my_obj['ts']
          s, ms = divmod(my_obj['ts'], 1000)  # (1236472051, 807)
          converted_time_stamp = '%s.%03d' % (time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
          temp_list["Time-Stamp"]=converted_time_stamp
          temp_list["Message"]=my_obj['msg']
          temp_list["MicroService"]=microservice_name
          temp_list["loglevel"]=my_obj['loglevel']
          if 'SRC_CLASS' in my_obj.keys():
            temp_list["src_class"]=my_obj['SRC_CLASS']
          else:
            temp_list["src_class"]='---'
          if 'SRC_METHOD' in my_obj.keys():
            temp_list["src_method"]=my_obj['SRC_METHOD']
          else:
            temp_list["src_method"]='---'
          if my_obj['ecid'] not in log_list.keys():
            log_list[my_obj['ecid']] = []
            ecid_list.append(my_obj['ecid'])
          log_list[my_obj['ecid']].append(temp_list)

log_list = {}
ecid_list = []

#set the path to these files appropriately
make_the_log_list("/Users/maheshabburi/Documents/Logs-tool/odalogs/bots-management-apis-7c6b67f97f-dvqxc.log","bots-management")
make_the_log_list("/Users/maheshabburi/Documents/Logs-tool/odalogs/bots-management-apis-7c6b67f97f-lpvkj.log","bots-management")
make_the_log_list("/Users/maheshabburi/Documents/Logs-tool/odalogs/bots-connectors-5f6f4f697f-9jscx.log","bots-connectors")
make_the_log_list("/Users/maheshabburi/Documents/Logs-tool/odalogs/bots-connectors-5f6f4f697f-cn2rr.log","bots-connectors")
make_the_log_list("/Users/maheshabburi/Documents/Logs-tool/odalogs/bots-sentry-service-76847ddd9-ddwbz.log","bots-sentry-service")
make_the_log_list("/Users/maheshabburi/Documents/Logs-tool/odalogs/bots-sentry-service-76847ddd9-mvp25.log","bots-sentry-service")

# sorting each key i.e. ecid based on time-stamp

for id in ecid_list:
  arr = log_list[id]
  for i in range(0, len(arr)):    
      for j in range(i+1, len(arr)):    
          if(arr[i]['Time-Stamp'] > arr[j]['Time-Stamp']):    
              temp = arr[i]   
              arr[i] = arr[j]    
              arr[j] = temp

log_list_final = {}
for id in ecid_list:
  arr = log_list[id]
  index = 1
  for i in range(0, len(arr)):
    if id not in log_list_final.keys():
      log_list_final[id]={}
    if index not in log_list_final[id].keys():
      log_list_final[id][index]=[]
    log_list_final[id][index].append(arr[i])
    if i+1==len(arr) or arr[i]["MicroService"]!=arr[i+1]["MicroService"]:
      index = index + 1   
#    print(id + " " + str(index))
# pprint(log_list_final['0000NjA2gCz7i4O5IjDCif1XEDq200074X'])

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

# set the content folder appropriately such that logs.html is contained in it
app = Flask(__name__,template_folder="/Users/maheshabburi/Desktop")

@app.route('/', methods=['GET'])
def main_page():
  return render_template('logs.html', log_list=log_list_final)

app.run()
