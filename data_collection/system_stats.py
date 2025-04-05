import psutil
import GPUtil
import datetime
import pynvml

pynvml.nvmlInit()

def get_system_stats():
    cpu_percent = psutil.cpu_percent(interval=1)
    per_core = psutil.cpu_percent(interval=1, percpu=True)
    ram = psutil.virtual_memory()
    net = psutil.net_io_counters()
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    gpus = GPUtil.getGPUs()
    gpu = gpus[0] if gpus else None

    try:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
    except:
        temp = None

    return {
        "time": datetime.datetime.now(),
        "cpu": cpu_percent,
        "cpu_per_core": per_core,
        "ram": ram.percent,
        "bytes_sent": net.bytes_sent,
        "bytes_recv": net.bytes_recv,
        "disk_percent": disk.percent,
        "disk_read": disk_io.read_bytes,
        "disk_write": disk_io.write_bytes,
        "gpu_load": gpu.load * 100 if gpu else None,
        "gpu_mem": gpu.memoryUtil * 100 if gpu else None,
        "gpu_temp": temp,
    }

