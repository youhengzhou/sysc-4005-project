import random
import os

# initialize csv file for getting data
if (os.path.exists('data.csv')):
    os.remove('data.csv')
header = "%s,%s\n" % ('arrival_time (miliseconds)', 'event_type')
with open("data.csv", "a") as f:
    f.write(header)

if (os.path.exists('buffer_data.csv')):
    os.remove('buffer_data.csv')
header = "%s,%s,%s\n" % ('arrival_time (miliseconds)', 'buffer_type', 'buffer_capacity')
with open("buffer_data.csv", "a") as f:
    f.write(header)

# function for appending to csv file
def appendToCSV(arrival_time, event_type):
    new_row = "\n%s,%s\n" % (str(arrival_time), event_type)
    with open("data.csv", "a") as f:
        f.write(new_row)

def appendToBufferCSV(arrival_time, buffer_type, buffer_capacity):
    new_row = "\n%s,%s,%s\n" % (str(arrival_time), buffer_type, str(buffer_capacity))
    with open("buffer_data.csv", "a") as f:
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

sim_states = {
    'components': {
        'c1_used': 0,
        'c2_used': 0,
        'c3_used': 0,
    },
    'inspectors': {
        'ins1': ['idle',0],
        'ins2': ['idle',0],
        'ins1_blocked_time': 0,
        'ins2_blocked_time': 0,
    },
    'buffers': {
        'c1_ws1': 0,
        'c1_ws2': 0,
        'c1_ws3': 0,
        'c2_ws2': 0,
        'c3_ws3': 0,
    },
    'workstations': {
        'ws1': ['idle',0],
        'ws2': ['idle',0],
        'ws3': ['idle',0],
        'ws1_work_time': 0,
        'ws2_work_time': 0,
        'ws3_work_time': 0,
    },
    'products': {
        'p1': 0,
        'p2': 0,
        'p3': 0
    },
}

fel = []

fel.append([0, 'ins1'])
fel.append([0, 'ins2'])

sim_time = 0

def handle_event(event_type, arrival_time, fel):
    global sim_states

    if event_type == 'ins1':
        return handle_ins1(arrival_time, fel)
    elif event_type == 'ins2':
        return handle_ins2(arrival_time, fel)
    elif event_type == 'ws1':
        return handle_ws1(arrival_time, fel)
    elif event_type == 'ws2':
        return handle_ws2(arrival_time, fel)
    elif event_type == 'ws3':
        return handle_ws3(arrival_time, fel)
    else:
        return fel

def handle_ins1(arrival_time, fel):
    global sim_states

    if sim_states['buffers']['c1_ws1'] <= sim_states['buffers']['c1_ws2'] and sim_states['buffers']['c1_ws1'] < 2:
        sim_states['buffers']['c1_ws1'] += 1
        sim_states['components']['c1_used'] += 1
        appendToBufferCSV(arrival_time,'c1_ws1',sim_states['buffers']['c1_ws1'])
        fel.append([arrival_time + random.choice(ins1_input), 'ins1'])
    elif sim_states['buffers']['c1_ws2'] <= sim_states['buffers']['c1_ws3'] and sim_states['buffers']['c1_ws2'] < 2:
        sim_states['buffers']['c1_ws2'] += 1
        sim_states['components']['c1_used'] += 1
        appendToBufferCSV(arrival_time,'c1_ws2',sim_states['buffers']['c1_ws2'])
        fel.append([arrival_time + random.choice(ins1_input), 'ins1'])
    elif sim_states['buffers']['c1_ws3'] < 2:
        sim_states['buffers']['c1_ws3'] += 1
        sim_states['components']['c1_used'] += 1
        appendToBufferCSV(arrival_time,'c1_ws3',sim_states['buffers']['c1_ws3'])
        fel.append([arrival_time + random.choice(ins1_input), 'ins1'])
    else:
        # inspectors state 1 is blocked, 0 is free
        print("inspector1 blocked")
        sim_states['inspectors']['ins1'] = [1,arrival_time]
    return fel

def handle_ins2(arrival_time, fel):
    global sim_states

    if random.randint(0,1) == 0:
        if sim_states['buffers']['c2_ws2'] < 2:
            sim_states['buffers']['c2_ws2'] += 1
            sim_states['components']['c2_used'] += 1
            appendToBufferCSV(arrival_time,'c2_ws2',sim_states['buffers']['c2_ws2'])
            fel.append([arrival_time + random.choice(ins22_input), 'ins2'])
        else:
            # if all buffers are full: start recording timer until any of the buffers are not at full capacity
            print("inspector2 blocked from buffer 2")
            sim_states['inspectors']['ins2'] = [2,arrival_time]
    else:
        if sim_states['buffers']['c3_ws3'] < 2:
            sim_states['buffers']['c3_ws3'] += 1
            sim_states['components']['c3_used'] += 1
            appendToBufferCSV(arrival_time,'c3_ws3',sim_states['buffers']['c3_ws3'])
            fel.append([arrival_time + random.choice(ins23_input), 'ins2'])
        else:
            # if all buffers are full: start recording timer until any of the buffers are not at full capacity
            print("inspector2 blocked from buffer 3")
            sim_states['inspectors']['ins2'] = [3,arrival_time]
    return fel

def handle_ws1(arrival_time, fel):
    global sim_states

    if sim_states['buffers']['c1_ws1'] > 0:
            sim_states['buffers']['c1_ws1'] -= 1
            # sim_states['components']['c1_used'] -= 1
            appendToBufferCSV(arrival_time,'c1_ws1',sim_states['buffers']['c1_ws1'])
            sim_states['products']['p1'] += 1
            if sim_states['inspectors']['ins1'][0] == 1:
                n_time = arrival_time - sim_states['inspectors']['ins1'][1]
                sim_states['inspectors']['ins1_blocked_time'] += n_time
                print('inspector1 blocked for ' + str(n_time))
                sim_states['inspectors']['ins1'] = [0,arrival_time]
            n_time = random.choice(ws1_input)
            sim_states['workstations']['ws1_work_time'] += n_time
            fel.append([arrival_time + n_time, 'ws1'])
    return fel

def handle_ws2(arrival_time, fel):
    global sim_states

    if sim_states['buffers']['c1_ws2'] > 0 and sim_states['buffers']['c2_ws2'] > 0:
            sim_states['buffers']['c1_ws2'] -= 1
            sim_states['buffers']['c2_ws2'] -= 1
            # sim_states['components']['c1_used'] -= 1
            # sim_states['c2_used'] -= 1
            appendToBufferCSV(arrival_time,'c1_ws2',sim_states['buffers']['c1_ws2'])
            appendToBufferCSV(arrival_time,'c2_ws2',sim_states['buffers']['c2_ws2'])
            sim_states['products']['p2'] += 1
            if sim_states['inspectors']['ins1'][0] == 1:
                n_time = arrival_time - sim_states['inspectors']['ins1'][1]
                sim_states['inspectors']['ins1_blocked_time'] += n_time
                print('inspector1 blocked for ' + str(n_time))
                sim_states['inspectors']['ins1'] = [0,arrival_time]
            if sim_states['inspectors']['ins2'][0] == 2:
                n_time = arrival_time - sim_states['inspectors']['ins2'][1]
                sim_states['inspectors']['ins2_blocked_time'] += n_time
                print('inspector2 sadf dsaf  blocked for ' + str(n_time))
                sim_states['inspectors']['ins2'] = [0,arrival_time]
            n_time = random.choice(ws2_input)
            sim_states['workstations']['ws2_work_time'] += n_time
            fel.append([arrival_time + n_time, 'ws2'])
    return fel

def handle_ws3(arrival_time, fel):
    global sim_states

    if sim_states['buffers']['c1_ws3'] > 0 and sim_states['buffers']['c3_ws3'] > 0:
            sim_states['buffers']['c1_ws3'] -= 1
            sim_states['buffers']['c3_ws3'] -= 1
            # sim_states['components']['c1_used'] -= 1
            # sim_states['c3_used'] -= 1
            appendToBufferCSV(arrival_time,'c1_ws3',sim_states['buffers']['c1_ws3'])
            appendToBufferCSV(arrival_time,'c3_ws3',sim_states['buffers']['c3_ws3'])
            sim_states['products']['p3'] += 1
            if sim_states['inspectors']['ins1'][0] == 1:
                n_time = arrival_time - sim_states['inspectors']['ins1'][1]
                sim_states['inspectors']['ins1_blocked_time'] += n_time
                print('inspector1 blocked for ' + str(n_time))
                sim_states['inspectors']['ins1'] = [0,arrival_time]
            if sim_states['inspectors']['ins2'][0] == 3:
                n_time = arrival_time - sim_states['inspectors']['ins2'][1]
                sim_states['inspectors']['ins2_blocked_time'] += n_time
                print('inspector2 afdssafd blocked for ' + str(n_time))
                sim_states['inspectors']['ins2'] = [0,arrival_time]
            n_time = random.choice(ws3_input)
            sim_states['workstations']['ws3_work_time'] += n_time
            fel.append([arrival_time + n_time, 'ws3'])
    return fel

while True:
    if len(fel) <= 0 or sim_time > 1000000:
        break
    
    fel.sort()
    sim_time, event_type = fel.pop(0)

    print(fel)
    # print(sim_states['buffers'])

    appendToCSV(sim_time, event_type)

    fel = handle_event(event_type, sim_time, fel)

    if (sim_states['buffers']['c1_ws1'] < 2 or sim_states['buffers']['c1_ws2'] < 2 or sim_states['buffers']['c1_ws3'] < 2) and not any(event[1] == 'ins1' for event in fel):
        fel.append([sim_time, 'ins1'])
    if (sim_states['buffers']['c2_ws2'] < 0 or sim_states['buffers']['c3_ws3'] < 2) and not any(event[1] == 'ins2' for event in fel):
        fel.append([sim_time, 'ins2'])

    if sim_states['buffers']['c1_ws1'] > 0 and not any(event[1] == 'ws1' for event in fel):
        fel.append([sim_time + random.choice(ws1_input), 'ws1'])
    if sim_states['buffers']['c1_ws2'] > 0 and sim_states['buffers']['c2_ws2'] > 0 and not any(event[1] == 'ws2' for event in fel):
        fel.append([sim_time + random.choice(ws2_input), 'ws2'])
    if sim_states['buffers']['c1_ws3'] > 0 and sim_states['buffers']['c3_ws3'] > 0 and not any(event[1] == 'ws3' for event in fel):
        fel.append([sim_time + random.choice(ws3_input), 'ws3'])

print('simulation end results: ')
print("simulation ran for: " + str(sim_time))
print("buffers: ")
print(sim_states['buffers'])
print("products created: ")
print(sim_states['products'])
print("Components Used: 1: " + str(sim_states['components']['c1_used']) + " , 2: " + str(sim_states['components']['c2_used'])  + " , 3: " + str(sim_states['components']['c3_used']))
print("Inspector Blocked Times: 1: " + str(sim_states['inspectors']['ins1_blocked_time']) + " , 2: " + str(sim_states['inspectors']['ins2_blocked_time']))
print("Workstation Active Times: 1: " + str(sim_states['workstations']['ws1_work_time']) + " , 2: " + str(sim_states['workstations']['ws2_work_time'])  + " , 3: " + str(sim_states['workstations']['ws3_work_time']))

