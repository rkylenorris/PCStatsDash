import platform
import socket
import psutil
import datetime

def get_system_info():
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime = datetime.datetime.now() - boot_time

    uptime_seconds = uptime.total_seconds()
    uptime_str = str(uptime).split('.')[0]

    # Determine style class for uptime
    if uptime_seconds > 5 * 24 * 3600:
        uptime_class = "text-danger"
    elif uptime_seconds > 3 * 24 * 3600:
        uptime_class = "text-warning"
    else:
        uptime_class = "text-success"

    return {
        "Hostname": {"value": socket.gethostname(), "class": "text-light"},
        "OS": {"value": f"{platform.system()} {platform.release()}", "class": "text-light"},
        "Processor": {"value": platform.processor(), "class": "text-light"},
        "Uptime": {"value": uptime_str, "class": uptime_class},
    }
