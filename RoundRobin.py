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


class Names:
    worker_names    = ['Alan', 'Alex', 'Noah', 'William', 'Jacob', 'Oliver', 'Alexander']
    worker_surnames = ['Andreas', 'Demetriou', 'Floros', 'Contos', 'Nazarian', 'Danchev', 'Ognyanov']

    tasks_title_verb = ['Accept', 'Guess', 'Achieve', 'Harass', 'Add', 'Hate', 'Admire','Hear', 'Admit', 'Help', 'Adopt', 'Hit'] 
    tasks_title_adj = ['Abrupt', 'Deep', 'Disturbed', 'Filthy', 'Filthy', 'Thankful', 'Tricky','Wacky', 'Zealous', 'Tiny']
    tasks_title_noun = ['Hamburger', 'Balloon', 'Banana', 'Australia', 'Branch', 'King', 'China','Teacher', 'Tomato', 'Napkin']

def gen_worker_name():
    ind1 = random.randint(0, len(Names.worker_names) - 1)
    ind2 = random.randint(0, len(Names.worker_surnames) - 1)
    name = Names.worker_names[ind1] + ' ' + Names.worker_surnames[ind2]
    return name

def gen_task_name():
    ind1 = random.randint(0, len(Names.tasks_title_verb) - 1)
    ind2 = random.randint(0, len(Names.tasks_title_adj) - 1)
    ind3 = random.randint(0, len(Names.tasks_title_noun) - 1)
    name = Names.tasks_title_verb[ind1] + ' ' + Names.tasks_title_adj[ind2] + ' ' +  Names.tasks_title_noun[ind3] 
    return name


class Model:
    def __init__(self, settings):
        self.settings = settings
        self.tasks = []
        self.workers = []
        self.current_worker_index = 0
        self.finished_tasks_info = []
        self.num_finished_tasks_viewed = 0

        self.timer_interval = 1000
        self.timer_id = None
        self.is_paused = False

        self.modelling_cycle_num = 0

    def generate_workers(self):
        print("workers:", self.settings.min_workers_count, self.settings.max_workers_count)
        self.workers = []
        num_workers = random.randint(self.settings.min_workers_count, self.settings.max_workers_count)
        for i in range(num_workers):
            name = "Worker {}".format(gen_worker_name())
            productivity = random.randint(1, 5)
            self.workers.append(Worker(name, productivity))

    def generate_tasks(self):
        self.tasks = []
        num_tasks = random.randint(self.settings.min_tasks_count, self.settings.max_tasks_count)
        for i in range(num_tasks):
            name = 'Task {} "{}"'.format(i+1, gen_task_name())
            complexity = random.randint(self.settings.min_complexity, self.settings.max_complexity)
            self.tasks.append(Task(name, complexity))

    def assign_tasks_to_workers(self):
        for i, task in enumerate(self.tasks):
            worker = self.workers[i % len(self.workers)]
            worker.add_task(task)
            
    def start_session(self):
        self.generate_workers()
        self.generate_tasks()
        self.assign_tasks_to_workers()
        self.reset_state()

    def reset_state(self):
        self.modelling_cycle_num = 0
        self.finished_tasks_info = []
    
    def advance_state(self):
        self.modelling_cycle_num += 1
    
    def reassign_tasks(self):
        tasks_to_reassign = [worker.get_current_task() for worker in self.workers]
        for i in range(len(self.workers)):
            next_worker = self.workers[(i + 1) % len(self.workers)]
            next_worker.replace_current_task(tasks_to_reassign[i])

    def execute_tasks(self):
        for worker in self.workers:
            finished_task = worker.work_task_piece()
            if finished_task is not None:
                cycle_num = self.modelling_cycle_num
                finished_task_info = (finished_task, worker, cycle_num)
                self.finished_tasks_info.append(finished_task_info)
                

class AppSettings:
    def __init__(self):
        self.time_interval = 1000

        self.min_workers_count = 3
        self.max_workers_count = 10
        self.min_tasks_count = 6
        self.max_tasks_count = 18

        self.min_complexity = 16
        self.max_complexity = 100

    def are_borders_valid(self, min, max):
        return min <= max
    
    def get_borders_from_str(self, min_str, max_str):
        if min_str.isdigit() and max_str.isdigit():
            return int(min_str), int(max_str)
        else:
            return None 
    
    def set_workers_count(self, min_str, max_str):
        borders = self.get_borders_from_str(min_str, max_str)
        if borders is None:
            return
        if self.are_borders_valid(borders[0], borders[1]):
            self.min_workers_count, self.max_workers_count = borders

    def set_tasks_count(self, min_str, max_str):
        borders = self.get_borders_from_str(min_str, max_str)
        if borders is None:
            return
        if self.are_borders_valid(borders[0], borders[1]):
            self.min_tasks_count, self.max_tasks_count = borders

    def set_complexity(self, min_str, max_str):
        borders = self.get_borders_from_str(min_str, max_str)
        if borders is None:
            return
        if self.are_borders_valid(borders[0], borders[1]):
            self.min_complexity, self.max_complexity = borders

    def set_time_interval(self, interval):
        if not interval.isdigit(): return
        if int(interval) > 0:
            self.time_interval = int(interval)


class RoundRobinModelling:
    def __init__(self, root):
        self.settings = AppSettings()
        self.model = Model(self.settings)

        self.timer_interval = 1000
        self.timer_id = None
        self.is_paused = False

        # Create GUI elements
        self.root = root
        self.new_button = tk.Button(root, text="New", command=self.start_session)
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_session)
        self.settings_button = tk.Button(root, text='Settings', command=self.open_settings_window)
        
        self.workers_listbox = tk.Listbox(root)
        self.workers_listbox.bind('<Button-1>', lambda event: self.view_tasks_for_currently_selected_worker())
        self.tasks_listbox = tk.Listbox(root)
        self.finished_tasks_listbox = tk.Listbox(root)

        # Place GUI elements
        self.new_button.grid(row=0, column=0)
        self.pause_button.grid(row=0, column=1)
        self.settings_button.grid(row=0, column=2)

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
        self.model.start_session()
        self.view_workers()
        self.start_timer()

    def start_timer(self):
        if self.timer_id is None:
            self.timer_id = self.root.after(self.timer_interval, self.on_timer)
    
    def pause_session(self):
        if self.timer_id is not None and not self.is_paused:
            self.root.after_cancel(self.timer_id)
            self.is_paused = True
            return
        
        if self.timer_id is not None and self.is_paused:
            self.is_paused = False
            self.timer_id = self.root.after(self.timer_interval, self.on_timer)

    def on_timer(self):
        self.model.execute_tasks()
        if random.random() < 0.5:
            self.model.reassign_tasks()
        self.model.advance_state()
        self.update_view()
        self.timer_id = self.root.after(self.timer_interval, self.on_timer)


    def get_selected_worker(self):
        selected_worker = self.workers_listbox.curselection()
        if selected_worker:
            return self.model.workers[selected_worker[0]]
        else:
            return None

    def view_workers(self):
        self.workers_listbox.delete(0, tk.END)
        for worker in self.model.workers:
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
        for task, worker, cycle_num in self.model.finished_tasks_info:
            msg = "%s finished by %s at %d-th cycle"%(task.name, worker.name, cycle_num)
            self.finished_tasks_listbox.insert(tk.END, msg)
        
    def update_view(self):
        self.view_tasks_for_currently_selected_worker()
        self.view_finished_tasks()


    def save_settings_on_close(self, settings_window, entries):
        min_workers_val = entries['min_workers'].get()
        max_workers_val = entries['max_workers'].get()
        self.settings.set_workers_count(min_workers_val, max_workers_val)

        min_tasks_val = entries['min_tasks'].get()
        max_tasks_val = entries['max_tasks'].get()
        self.settings.set_tasks_count(min_tasks_val, max_tasks_val)
        
        time_interval_val = entries['time_interval'].get()
        self.settings.set_time_interval(time_interval_val)

        min_complexity_val = entries['min_complexity'].get()
        max_complexity_val = entries['max_complexity'].get()
        self.settings.set_complexity(min_complexity_val, max_complexity_val)

        settings_window.destroy()

    def open_settings_window(self):
        # create settings window
        settings_window = tk.Toplevel(self.root)
        settings_window.title('Settings')

        # create input widgets for settings
        min_workers_entry = tk.Entry(settings_window)
        max_workers_entry = tk.Entry(settings_window)
        min_tasks_entry = tk.Entry(settings_window)
        max_tasks_entry = tk.Entry(settings_window)
        time_interval_entry = tk.Entry(settings_window)
        min_complexity_entry = tk.Entry(settings_window)
        max_complexity_entry = tk.Entry(settings_window)

        # add labels to input widgets
        tk.Label(settings_window, text='Minimum Workers Count').grid(row=0, column=0)
        min_workers_entry.grid(row=0, column=1)
        tk.Label(settings_window, text='Maximum Workers Count').grid(row=1, column=0)
        max_workers_entry.grid(row=1, column=1)
        tk.Label(settings_window, text='Minimum Tasks Count').grid(row=2, column=0)
        min_tasks_entry.grid(row=2, column=1)
        tk.Label(settings_window, text='Maximum Tasks Count').grid(row=3, column=0)
        max_tasks_entry.grid(row=3, column=1)
        tk.Label(settings_window, text='Time Interval').grid(row=4, column=0)
        time_interval_entry.grid(row=4, column=1)
        tk.Label(settings_window, text='Minimum Task Complexity').grid(row=5, column=0)
        min_complexity_entry.grid(row=5, column=1)
        tk.Label(settings_window, text='Maximum Task Complexity').grid(row=6, column=0)
        max_complexity_entry.grid(row=6, column=1)

        entries = {}
        entries['min_workers'] = min_workers_entry
        entries['max_workers'] = max_workers_entry
        entries['min_tasks'] = min_tasks_entry
        entries['max_tasks'] = max_tasks_entry
        entries['time_interval'] = time_interval_entry
        entries['min_complexity'] = min_complexity_entry
        entries['max_complexity'] = max_complexity_entry

        # add button to close settings window
        close_button = tk.Button(settings_window, text='Save And Close', command = lambda : self.save_settings_on_close(settings_window, entries))
        close_button.grid(row=7, column=1)


def launch_app():
    mainView = tk.Tk()
    RoundRobinModelling(mainView)
    mainView.mainloop()


if __name__ == "__main__":
    launch_app()
