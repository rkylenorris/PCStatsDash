import psutil
import GPUtil
import datetime

def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    net = psutil.net_io_counters()
    gpus = GPUtil.getGPUs()
    gpu = gpus[0] if gpus else None

    return {
        "time": datetime.datetime.now(),
        "cpu": cpu_percent,
        "ram": ram.percent,
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "gpu_load": gpu.load * 100 if gpu else None,
        "gpu_mem": gpu.memoryUtil * 100 if gpu else None,
    }
