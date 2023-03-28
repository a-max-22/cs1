import tkinter as tk
import random

class Task:
    """
    A class to represent a task with its complexity measured in work units.
    """
    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity
    
    def is_finished(self):
        return self.complexity <= 0


class Worker:
    """
    A class to represent a worker with their name and productivity measured in work units per time unit.
    """
    def __init__(self, name, productivity):
        self.name = name
        self.productivity = productivity
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def work_task_piece(self):
        currentTask = self.get_current_task()
        if currentTask is None: return None

        currentTask.complexity -= self.productivity
        if currentTask.is_finished(): 
            self.remove_current_task()
            return currentTask
        return None

    def get_current_task(self):
        if len(self.tasks) == 0:
            return None
        current_task = self.tasks[0]
        if current_task is None and len(self.tasks) > 1:
            del self.tasks[0]
            return self.tasks[0]
        if current_task is None and len(self.tasks) == 1:
            del self.tasks[0]
            return None
        return current_task

    def remove_current_task(self):
        if len(self.tasks) == 0:
            return
        del self.tasks[0]

    def replace_current_task(self, task):
        if len(self.tasks) == 0:
            self.tasks.append(task)
            return None
        task_to_replace = self.tasks[0] 
        self.tasks[0] = task
        return task_to_replace


class RoundRobinModelling:
    def __init__(self, root):
        self.root = root
        self.tasks = []
        self.workers = []
        self.current_worker_index = 0
        self.finished_tasks_info = []
        self.num_finished_tasks_viewed = 0

        self.timer_interval = 1000
        self.timer_id = None
        self.is_paused = False
        self.modelling_cycle_num = 0

        # Create GUI elements
        self.new_button = tk.Button(root, text="New", command=self.start_session)
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_session)
        
        self.workers_listbox = tk.Listbox(root)
        self.workers_listbox.bind('<Button-1>', lambda event: self.view_tasks_for_currently_selected_worker())
        self.tasks_listbox = tk.Listbox(root)
        self.finished_tasks_listbox = tk.Listbox(root)

        # Place GUI elements
        self.new_button.grid(row=0, column=0)
        self.pause_button.grid(row=0, column=1)

        # add the listboxes to the grid
        self.workers_listbox.grid(row=1, column=0, sticky="nsew")
        self.tasks_listbox.grid(row=1, column=1, sticky="nsew")
        self.finished_tasks_listbox.grid(row=1, column=2, sticky="nsew")

        # configure the columns to expand
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        # configure the rows to expand
        self.root.grid_rowconfigure(1, weight=1)

    def start_session(self):
        self.generate_workers()
        self.generate_tasks()
        self.assign_tasks_to_workers()

        self.view_workers()
        self.reset_state()
        self.start_timer()

    def generate_workers(self):
        self.workers = []
        num_workers = random.randint(2, 10)
        for i in range(num_workers):
            name = "Worker {}".format(i+1)
            productivity = random.randint(1, 5)
            self.workers.append(Worker(name, productivity))

    def generate_tasks(self):
        self.tasks = []
        num_tasks = random.randint(5, 20)
        for i in range(num_tasks):
            name = "Task {}".format(i+1)
            complexity = random.randint(5, 50)
            self.tasks.append(Task(name, complexity))

    def assign_tasks_to_workers(self):
        for i, task in enumerate(self.tasks):
            worker = self.workers[i % len(self.workers)]
            worker.add_task(task)

    def start_timer(self):
        if self.timer_id is None:
            self.timer_id = self.root.after(self.timer_interval, self.on_timer)

    def reset_state(self):
        self.modelling_cycle_num = 0
        self.finished_tasks_info = []
    
    def advance_state(self):
        self.modelling_cycle_num += 1

    def pause_session(self):
        if self.timer_id is not None and not self.is_paused:
            self.root.after_cancel(self.timer_id)
            self.is_paused = True
            return
        
        if self.timer_id is not None and self.is_paused:
            self.is_paused = False
            self.timer_id = self.root.after(self.timer_interval, self.on_timer)

    def on_timer(self):
        self.work_task_pieces()
        if random.random() < 0.5:
            self.reassign_tasks()
        self.advance_state()
        self.update_view()
        self.timer_id = self.root.after(self.timer_interval, self.on_timer)

    def work_task_pieces(self):
        for worker in self.workers:
            finished_task = worker.work_task_piece()
            if finished_task is not None:
                cycle_num = self.modelling_cycle_num
                finished_task_info = (finished_task, worker, cycle_num)
                self.finished_tasks_info.append(finished_task_info)

    def reassign_tasks(self):
        tasks_to_reassign = [worker.get_current_task() for worker in self.workers]
        for i in range(len(self.workers)):
            worker = self.workers[i]
            next_worker = self.workers[(i + 1) % len(self.workers)]
            next_worker.replace_current_task(tasks_to_reassign[i])
    
    def get_selected_worker(self):
        selected_worker = self.workers_listbox.curselection()
        if selected_worker:
            return self.workers[selected_worker[0]]
        else:
            return None

    def view_workers(self):
        self.workers_listbox.delete(0, tk.END)
        for worker in self.workers:
            self.workers_listbox.insert(tk.END, worker.name)

    def view_tasks_for_currently_selected_worker(self):
        selected_worker = self.get_selected_worker()
        if selected_worker is None:
            return
        self.tasks_listbox.delete(0, tk.END)
        for task in selected_worker.tasks:
            if task is not None:
                self.tasks_listbox.insert(tk.END, task.name)

    def view_finished_tasks(self):
        self.finished_tasks_listbox.delete(0, tk.END)
        for task, worker, cycle_num in self.finished_tasks_info:
            msg = "%s finished by %s at %d-th cycle"%(task.name, worker.name, cycle_num)
            self.finished_tasks_listbox.insert(tk.END, msg)
        
    def update_view(self):
        self.view_tasks_for_currently_selected_worker()
        self.view_finished_tasks()



def launch_app():
    root = tk.Tk()
    app = RoundRobinModelling(root)
    root.mainloop()


if __name__ == "__main__":
    launch_app()