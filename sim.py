import heapq
import random
import os

# initialize csv files for getting data
if (os.path.exists('data.csv')):
    os.remove('data.csv')
header = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ('arrival_time (miliseconds)','event_type','c1','c2','c3','ins1','ins2','c1_ws1','c1_ws2','c3_ws3','c2_ws2','c3_ws3','ws1','ws2','ws3','p1','p1','p3')
with open("data.csv", "a") as f:
    f.write(header)

# function for appending to csv file
def appendToCSV(arrival_time, event_type):
    new_row = "\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(arrival_time),event_type,str(c1),str(c2),str(c3),str(ins1),str(ins2),str(c1_ws1),str(c1_ws2),str(c1_ws3),str(c2_ws2),str(c3_ws3),str(ws1),str(ws2),str(ws3),str(p1),str(p2),str(p3))
    with open("data.csv", "a") as f:
        f.write(new_row)

# read input files
def read_dat_files(file_name):
    data = open(file_name).read().splitlines()
    data = [i.strip() for i in data]
    data = list(filter(None, data))
    output = []
    for i in data:
        output.append(int((float(i)*1000)))
    return output

ins1_input = read_dat_files('input files/servinsp1.dat')
ins22_input = read_dat_files('input files/servinsp22.dat')
ins23_input = read_dat_files('input files/servinsp23.dat')
ws1_input = read_dat_files('input files/ws1.dat')
ws2_input = read_dat_files('input files/ws2.dat')
ws3_input = read_dat_files('input files/ws3.dat')

c1 = 0
c2 = 0
c3 = 0

ins1 = 0
ins2 = 0

c1_ws1 = 0
c1_ws2 = 0
c1_ws3 = 0
c2_ws2 = 0
c3_ws3 = 0

ws1 = 0
ws2 = 0
ws3 = 0

p1 = 0
p2 = 0
p3 = 0

sim_time = 0
fel = []
fel.append([0, 'ins1'])
fel.append([0, 'ins2'])
heapq.heapify(fel)

while True:
    if sim_time > 1000000:
        break
    
    # check states, create events to be handled
    # if entity is 0, create start event
    # if entity is 1, create end event
    if ins1 == 0 and (c1_ws1 < 2 or c1_ws2 < 2 or c1_ws3 < 2) and not any(event[1] == 'ins1' for event in fel):
        heapq.heappush(fel,([sim_time, 'ins1']))
    if ins1 == 1 and (c1_ws1 < 2 or c1_ws2 < 2 or c1_ws3 < 2) and not any(event[1] == 'ins1_done' for event in fel):
        heapq.heappush(fel,([sim_time + random.choice(ins1_input), 'ins1_done']))
    
    if ins2 == 0 and (c2_ws2 < 0 or c3_ws3 < 2) and not any(event[1] == 'ins2' for event in fel):
        heapq.heappush(fel,([sim_time, 'ins2']))
    if ins2 == 1 and (c2_ws2 < 0 or c3_ws3 < 2) and not any(event[1] == 'ins2_done' for event in fel):
        if random.randint(0,1) == 0:
            heapq.heappush(fel,([sim_time + random.choice(ins22_input), 'ins22_done']))
        else:
            heapq.heappush(fel,([sim_time + random.choice(ins23_input), 'ins23_done']))

    if ws1 == 0 and c1_ws1 > 0 and not any(event[1] == 'ws1' for event in fel):
        heapq.heappush(fel,([sim_time, 'ws1']))
    if ws1 == 1 and c1_ws1 > 0 and not any(event[1] == 'ws1_done' for event in fel):
        heapq.heappush(fel,([sim_time + random.choice(ws1_input), 'ws1_done']))
    
    if ws2 == 0 and c1_ws2 > 0 and c2_ws2 > 0 and not any(event[1] == 'ws2' for event in fel):
        heapq.heappush(fel,([sim_time, 'ws2']))
    if ws2 == 1 and c1_ws2 > 0 and c2_ws2 > 0 and not any(event[1] == 'ws2_done' for event in fel):
        heapq.heappush(fel,([sim_time + random.choice(ws2_input), 'ws2_done']))
    
    if ws3 == 0 and c1_ws3 > 0 and c3_ws3 > 0 and not any(event[1] == 'ws3' for event in fel):
        heapq.heappush(fel,([sim_time, 'ws3']))
    if ws3 == 1 and c1_ws3 > 0 and c3_ws3 > 0 and not any(event[1] == 'ws3_done' for event in fel):
        heapq.heappush(fel,([sim_time + random.choice(ws3_input), 'ws3_done']))

    # pop min event from fel
    sim_time, event_type = heapq.heappop(fel)
    print(fel)

    # handle events, change state
    # "start events" toggle entity state to 1
    # "end events" check if product queue is free, then produce product, then toggle entity state to 0
    if event_type == 'ins1':
        ins1 = 1
        appendToCSV(sim_time,'ins1 started')

    elif event_type == 'ins1_done':
        ins1 = 0
        if c1_ws1 <= c1_ws2 and c1_ws1 < 2:
            c1 += 1
            c1_ws1 += 1
            appendToCSV(sim_time,'ins1 end produced to c1_ws1')
        elif c1_ws2 <= c1_ws3 and c1_ws2 < 2:
            c1 += 1
            c1_ws2 += 1
            appendToCSV(sim_time,'ins1 end produce to c1_ws2')
        elif c1_ws3 < 2:
            c1 += 1
            c1_ws3 += 1
            appendToCSV(sim_time,'ins1 end produce to c1_ws3')
        else:
            ins1 = 1

    elif event_type == 'ins2':
        ins2 = 1
        appendToCSV(sim_time,'ins2 started')
        
    elif event_type == 'ins22_done':
        ins2 = 0
        if c2_ws2 < 2:
            c2 += 1
            c2_ws2 += 1
            appendToCSV(sim_time,'ins2 end produce to c2_ws2')
        else:
            ins2 = 1

    elif event_type == 'ins23_done':
        ins2 = 0
        if c3_ws3 < 2:
            c3 += 1
            c3_ws3 += 1
            appendToCSV(sim_time,'ins2 end produce to c3_ws3')
        else:
            ins2 = 1
    
    elif event_type == 'ws1':
        ws1 = 1
        appendToCSV(sim_time,'ws1 started')

    elif event_type == 'ws1_done':
        ws1 = 0
        if c1_ws1 > 0:
            c1_ws1 -= 1
            p1 += 1
            appendToCSV(sim_time,'ws1 end produce to p1')
        else:
            ws1 = 1

    elif event_type == 'ws2':
        ws2 = 1
        appendToCSV(sim_time,'ws2 started')

    elif event_type == 'ws2_done':
        ws2 = 0
        if c1_ws2 > 0 and c2_ws2 > 0:
            c1_ws2 -= 1
            c2_ws2 -= 1
            p2 += 1
            appendToCSV(sim_time,'ws2 end produce to p2')
        else:
            ws2 = 1

    elif event_type == 'ws3':
        ws3 = 1
        appendToCSV(sim_time,'ws3 started')

    elif event_type == 'ws3_done':
        ws3 = 0
        if c1_ws3 > 0 and c3_ws3 > 0:
            c1_ws3 -= 1
            c3_ws3 -= 1
            p3 += 1
            appendToCSV(sim_time,'ws3 end produce to p3')
        else:
            ws3 = 1

print('simulation end results: ')
print("simulation ran for: " + str(sim_time))
print("buffers: ")
print(c1_ws1)
print(c1_ws2)
print(c1_ws3)
print("products created: ")
print(p1)
print(p2)
print(p3)
