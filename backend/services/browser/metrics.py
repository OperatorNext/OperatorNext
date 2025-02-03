import psutil
from typing import Dict

class SystemMetricsCollector:
    """系统指标收集器"""
    def __init__(self, process):
        self.process = process

    def get_metrics(self) -> Dict:
        """获取系统资源使用指标"""
        try:
            # 获取进程的内存信息
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            
            # 获取CPU使用信息
            cpu_percent = self.process.cpu_percent(interval=0.1)
            cpu_times = self.process.cpu_times()
            
            # 获取系统总体信息
            system_memory = psutil.virtual_memory()
            system_cpu = psutil.cpu_percent(interval=0.1)
            
            return {
                "memory": {
                    "rss": memory_info.rss,  # 实际使用的物理内存
                    "vms": memory_info.vms,  # 虚拟内存大小
                    "percent": memory_percent,  # 内存使用百分比
                    "system_total": system_memory.total,
                    "system_available": system_memory.available,
                    "system_percent": system_memory.percent
                },
                "cpu": {
                    "process_percent": cpu_percent,  # 进程CPU使用率
                    "system_percent": system_cpu,    # 系统CPU使用率
                    "user_time": cpu_times.user,     # 用户空间CPU时间
                    "system_time": cpu_times.system, # 系统空间CPU时间
                    "threads": len(self.process.threads())  # 线程数
                }
            }
        except Exception as e:
            print(f"Warning - 获取系统指标时出错: {str(e)}")
            return {
                "memory": {"error": str(e)},
                "cpu": {"error": str(e)}
            } 