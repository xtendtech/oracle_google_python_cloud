import datetime
import time
from flask import Flask
from flask import render_template
import psutil
 

app=Flask(__name__)
@app.route("/")
def hello():
    cpu_percent=psutil.cpu_times_percent(interval=2)
                                         

    mem_percent=psutil.virtual_memory().percent
 
    disk_percent=psutil.disk_usage("/").percent
    cpu_cores=psutil.cpu_count()
    counters=psutil.net_io_counters()
    print(counters)
    uptime = time.time() - psutil.boot_time()
    uptime=datetime.datetime.fromtimestamp(uptime).strftime("%H:%M:%S")
    
  
    net=psutil.net_io_counters()
    bytes_sent=net.bytes_sent/1024/1024
    bytes_recv=net.bytes_recv/1024/1024
    process_count=len(psutil.pids())
    partitions=psutil.disk_partitions()
    swap_percent=(psutil.virtual_memory().total )/1024/1024 
    message=None

    return  render_template("index.html",
                            cpu_percent=cpu_percent,
                            mem_percent=mem_percent,
                            disk_percent=disk_percent,
                            cpu_cores=cpu_cores,
                            uptime=uptime,
                            bytes_sent=bytes_sent,
                            bytes_recv=bytes_recv,
                            process_count=process_count,
                            swap_percent=swap_percent,
                            message=message
                            )

   


if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

