import argparse
import csv

from processo import Processo
import plotly.figure_factory as ff
import pandas as pd

def take_time(elem):
    return elem.dur


def take_ini(elem):
    return elem.ini


def take_ftime(elem):
    return elem.ini + elem.dur


def take_priority(elem):
    return elem.prior


parser = argparse.ArgumentParser(description='Simula Escalonador de Processos.')
parser.add_argument('filename')
parser.add_argument('-f', '--fcfs',
                    action='store_true')
parser.add_argument('-s', '--sjf',
                    action='store_true')
parser.add_argument('-r', '--roundrobin',
                    action='store_true')
args = parser.parse_args()

with open(args.filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 1
    processes = []
    for row in csv_reader:
        x = Processo(line_count, row[0], row[1], row[2])
        processes.append(x)
        line_count += 1
queue = []
order = []
time_count = 0
if args.fcfs:
    while processes or queue:
        if queue:
            if queue[0].time_left == 0:
                queue.remove(queue[0])
        for process in processes:
            if time_count >= process.ini:
                queue.append(process)
                processes.remove(process)
        if not queue and processes:
            order.append(0)
        elif queue:
            order.append(queue[0].n)
            queue[0].time_left -= 1
        time_count += 1
elif args.sjf:
    while processes or queue:
        for process in processes:
            if time_count >= process.ini:
                queue.append(process)
                processes.remove(process)
                queue.sort(key=take_time)
        if not queue and processes:
            order.append(0)
            time_count += 1
        elif queue:
            for i in range(queue[0].time_left):
                order.append(queue[0].n)
                time_count += 1
            queue.pop(0)
elif args.roundrobin:
    for process in processes:
        if time_count >= process.ini:
            queue.append(process)
            processes.remove(process)
    while processes or queue:
        if queue:
            if queue[0].time_left > 0:
                queue.append(queue[0])
            queue.pop(0)
        if not queue and processes:
            order.append(0)
            time_count += 1
            for process in processes:
                if time_count >= process.ini:
                    queue.append(process)
                    processes.remove(process)
        elif queue:
            for i in range(2):
                if queue[0].time_left > 0:
                    order.append(queue[0].n)
                    queue[0].time_left -= 1
                else:
                    break
                time_count += 1
                for process in processes:
                    if time_count >= process.ini:
                        queue.append(process)
                        processes.remove(process)
else:
    print('Algoritimo não selecionado!\n'
          'Selecione um algoritimo ao executar o programa:\n'
          'Shortest Job First: -s\n'
          'First Come First Served: -f\n'
          'Round-Robin: -r\n')
    exit()

df = pd.DataFrame(columns=['Task', 'Start', 'Finish', 'Resource'])
for i in range(len(order)):
    if order[i] != 0:
        df = df._append(dict(Task=str(order[i]), Start=i, Finish= i+1, Resource=str(order[i])),ignore_index=True)
fig = ff.create_gantt(df, index_col = 'Task',  bar_width = 0.4, show_colorbar=True, group_tasks= True)
fig.update_layout(xaxis_type='linear')
fig.show()