import multiprocessing as mp

from models.order import Order


def put_order_to_queue(order: Order, queue: mp.Queue) -> None:
    queue.put(order)
    
def get_approximate_time_to_delivery(order: Order) -> int:
    return len(order.order_list) * 10

# def info(task_queue: mp.Queue):
#     sleep_time = random.randint(1, 10)
    
#     while True:
#         task = task_queue.get()
#         if task is None:
#             # Shutdown signal
#             break
    
#         print(f"""
#             {sleep_time=}
#             {task_queue.qsize()=}
#             {os.getpid()=}
#             {os.getppid()=}
#             {mp.current_process()=}
#             {datetime.datetime.now().isoformat()=}
#             """)
#         time.sleep(sleep_time)
# def main():
#     # mp.set_start_method('spawn')
    
#     num_workers = 4
#     task_queue = mp.Queue()
#     workers = []
    
#     for i in range(num_workers):
#         task_queue.put(f"task {i}")
    
#     for _ in range(num_workers):
#         p = mp.Process(target=info, args=(task_queue,))
#         p.start()
#         workers.append(p)
        
#     for i in range(num_workers**2):
#         task_queue.put(f"task {i}")