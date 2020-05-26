from collections import namedtuple
from prettytable import PrettyTable

DEFAULT_LIST_SIZE = 15
DEFAULT_FILE_NAME = 'task_db'

Task = namedtuple('Task', 'name desc due assignee status')
tasks_cache = {}

def load_tasks(filepath=DEFAULT_FILE_NAME):
  file = None
  i = 0
  try:
    file = open(filepath, 'r')
    for line in file:
      row = line.split('\t')
      tasks_cache[row[0].strip()] = Task(row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip().strip('\n'))
      # add sorting -> due date, then open, then someday/maybe
  finally:
      if file != None:
        file.close()

def list_tasks(n=DEFAULT_LIST_SIZE):
  i = 0
  tasks = []
  for val in tasks_cache.values():
    tasks.append(val)
    i += 1
    if i == n:
      break   
  return tasks

def display_tasks(tasks):
  print("################################################################")
  print("0.Exit; 1.Add; 2.Delete; 3.Delegate; 4.Complete; 5.Set Due Date") # todo add someday/maybe
  print("################################################################")
  table = PrettyTable()
  table.field_names = ["Name", "Description", "Due", "Assignee", "Status"]
  for task in tasks:
    table.add_row([task.name, task.desc, task.due, task.assignee, task.status])
  print(table)

# todo : write all edits to file after cache update
def delete_task(name):
  tasks_cache.pop(name, None)

def add_task(task):
  if task.name not in tasks_cache:
    tasks_cache[task.name] = task

def delegate_task(name, assignee):
  if name in tasks_cache and assignee:
    task = tasks_cache[name]
    tasks_cache[name] = Task(task.name, task.desc, task.due, assignee, 'Delegated')

def due_task(name, due):
  if name in tasks_cache and due:
    task = tasks_cache[name]
    tasks_cache[name] = Task(task.name, task.desc, due, task.assignee, task.status)

def complete_task(name):
  delete_task(name)

def main():
  load_tasks()
  inp = -1 
  while inp != 0:
    display_tasks(list_tasks())
    print("?: ", end=""),
    inp = int(input()) # todo validate input
    # todo parse task from input
    if inp == 1:
      add_task(Task('example20', 'example task 20', '', 'Nishikar', 'Open'))
    elif inp == 2:
      delete_task('example5')
    elif inp == 3:
      delegate_task('example2', 'chetan')
    elif inp == 4:
      complete_task('example6')
    elif inp == 5:
      due_task('example20', '2020-06-21')

if __name__ == '__main__':
  main() 
