import csv
import random
import os

# initialize csv file for getting data
if (os.path.exists('data.csv')):
    os.remove('data.csv')
header = "%s,%s\n" % ('arrival_time (miliseconds)', 'event_type')
with open("data.csv", "a") as f:
    f.write(header)

# function for appending to csv file
def appendToCSV(arrival_time, event_type):
    new_row = "\n%s,%s\n" % (str(arrival_time), event_type)
    with open("data.csv", "a") as f:
        f.write(new_row)

# read input files
def read_dat_files(file_name):
    data = open(file_name).read().splitlines()
    data = [i.strip() for i in data]
    data = list(filter(None, data))
    output = []
    for i in data:
        output.append(int(float(i)*1000))
    return output

ins1_input = read_dat_files('input files/servinsp1.dat')
ins22_input = read_dat_files('input files/servinsp22.dat')
ins23_input = read_dat_files('input files/servinsp23.dat')
ws1_input = read_dat_files('input files/ws1.dat')
ws2_input = read_dat_files('input files/ws2.dat')
ws3_input = read_dat_files('input files/ws3.dat')

print(ins1_input)
print(ins22_input)
print(ins23_input)
print(ws1_input)
print(ws2_input)
print(ws3_input)

inspectors = {
    'ins1': 0,
    'ins2': 0,
}

buffers = {
    'c1_ws1': 0,
    'c1_ws2': 0,
    'c1_ws3': 0,
    'c2_ws2': 0,
    'c3_ws3': 0,
}

workstations = {
    'ws1': 0,
    'ws2': 0,
    'ws3': 0,
}

products = {
    'p1': 0,
    'p2': 0,
    'p3': 0
}

fel = []

sim_time = 0

def handle_event(event, fel):
    if event == 'ins1':
        return handle_ins1(event, fel)

def handle_ins1(event, fel):
    pass

def handle_ins2(event, fel):
    pass

def handle_ws1(event, fel):
    pass

def handle_ws2(event, fel):
    pass

def handle_ws3(event, fel):
    pass

while True:
    if len(fel) <= 0 or sim_time > 1000000:
        break
    
    fel.sort()
    sim_time, event = fel.pop(0)
    fel = handle_event(sim_time, event)
