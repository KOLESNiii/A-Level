import random
import time
import os

QUANTUM = 2
TIMEGAP = 1
class Task:
    def __init__(self, pid):
        self.burst  = random.randrange(1, 20)
        self.pid = pid
        self.state = "Ready"
    
    def Service(self):
        self.state = "Serviced"
        self.burst -= 1
        if self.burst == 0:
            self.state = "Completed"
            return True
        return False
        
    
    def Suspend(self):
        if self.state != "Completed":
            self.state = "Suspended"
        
    def PrintState(self):
        str = " "*5 + str(self.pid) + " "*13 + str(self.burst) + " "*11 + self.state
        print(f"Process ID ------ Burst ------ Process State\n{str}\n---------------------------------------------", end="\r")
        
def CreateTasks(count):
    tasks = []
    for pid in range(count):
        tasks.append(Task(pid))
    return tasks

def PrintState(tasks):
    cls()
    lines = [" "*5 + str(task.pid) + " "*13 + str(task.burst) + " "*11 + task.state for task in tasks]
    s = "\n".join(lines)
    print("Process ID ------ Burst ------ Process State\n"+s+"\n---------------------------------------------", end="\r")

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
    
def RoundRobin(tasks):
    while sum([task.burst for task in tasks]) != 0:
        for task in tasks:
            if task.burst != 0:
                for _ in range(QUANTUM):
                    ended = task.Service()
                    PrintState(tasks)
                    time.sleep(TIMEGAP)
                    if ended:
                        break
                task.Suspend()

def FCFS(tasks):
    for task in tasks:
        while task.burst != 0:
            ended = task.Service()
            PrintState(tasks)
            time.sleep(TIMEGAP)
            if ended:
                break

def STR(tasks):
    while sum([task.burst for task in tasks]) != 0:
        tasks.sort(key=lambda x: x.burst)
        tempTasks = [task for task in tasks if task.burst != 0]
        task = tempTasks[0]
        tasks.sort(key=lambda x: x.pid)
        for _ in range(QUANTUM):
            ended = task.Service()
            PrintState(tasks)
            time.sleep(TIMEGAP)
            if ended:
                break
        task.Suspend()

def SJF(tasks):
    while sum([task.burst for task in tasks]) != 0:
        tasks.sort(key=lambda x: x.burst)
        task = tasks[0]
        tasks.sort(key=lambda x: x.pid)
        while task.burst != 0:
            task.Service()
            PrintState(tasks)
            time.sleep(TIMEGAP)

def main():
    tasks = CreateTasks(5)
    FCFS(tasks.copy())

main()

