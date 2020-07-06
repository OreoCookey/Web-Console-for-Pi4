import time
import json
import subprocess
from datetime import datetime


#cleaning the graph data
with open('static/data.json') as f:

                data = json.load(f)
                g_data = []
                data["graph_data"] = g_data

with open("static/data.json", 'w') as json_file:
                json.dump(data, json_file)

while True:

    now = datetime.now()
    millis = int(round(time.time() * 1000))


    #using a bash command to read the file containing temperature
    out = subprocess.Popen(['cat', '/sys/class/thermal/thermal_zone0/temp',], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    #converting from bytes to string
    temperature = str(stdout, "utf-8")

    #converting temp into more readble format
    temperature = int(temperature)/1000
    temperature = round(temperature, 2)

    #getting the cpu  usage
  #  out = subprocess.Popen(['iostat', '-c',], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                                                                                                                        stdout, stderr = out.communicate()
   # stdout, stderr = out.communicate()
                                                                                                                                                                                                                    #converting from bytes to string
   # data = str(stdout, "utf-8")                                                                                                                                                                                        data = data.split()
    #cpu_load = data[14]

    #getting the cpu load
    out = subprocess.Popen(['iostat', '-c',], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    #converting from bytes to string
    cpu_load = str(stdout, "utf-8")

    cpu_load  = cpu_load.split()
    cpu_load = cpu_load[14]
    cpu_load = cpu_load.strip()
    cpu_load = float(cpu_load)

    #getting the memory usage
    out = subprocess.Popen(['vmstat', '-s',], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    #converting to string                                                                                                                                                                                              data = str(stdout, "utf-8")
    data = str(stdout, "utf-8")
    #getting the memory info
    data = data.split()
    memory_used = data[4]
    memory_total = data[0]

    memory_usage = (int(memory_used)/int(memory_total))*100
    memory_usage = round(memory_usage, 2)

    #get process
    out = subprocess.Popen(['sh', 'scripts/proc.sh',], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    #converting from bytes to string
    processess = str(stdout, "utf-8")
    processess = int(processess)


    #get ip address
    out = subprocess.Popen(['sh', 'scripts/get_ip.sh',], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()

    #converting from bytes to string
    local_ip = str(stdout, "utf-8")
    local_ip = local_ip.strip()


    #getting the data from json file

    with open('static/data.json') as f:

            data = json.load(f)

            #updating the dictionary
            data['temperature'] = temperature
            data['cpu_usage'] = cpu_load
            data['local_ip'] = local_ip
            data['memory_usage'] = memory_usage
            data['processes'] = processess


	    #updating the graph stats
            g_data = data["graph_data"]
            data_point = {"timestamp": millis, "temp": temperature}
            g_data.append(data_point)

            if len(g_data) > 50:
            	del g_data[0]

            data["graph_data"] = g_data

    with open("static/data.json", 'w') as json_file:
            json.dump(data, json_file)

    time.sleep(0.2)
