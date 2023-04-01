from decimal import *
import heapq
import math
import random
import os

# CLCG from milestone 2
def EXPDist_RVG(x1, x2, a1, m1, a2, m2, mean):
    for _ in range(300):
        x1 = (a1 * x1) % m1
        x2 = (a2 * x2) % m2
        xj = (x1 - x2) % (2147483562)
        if xj > 0:
            randomNumberForCycle = xj / 2147483563
        else:
            randomNumberForCycle = 2147483562 / 2147483563
        return -1/(1/mean) * math.log(1 - randomNumberForCycle)

# step 1
# seed1 = 100
# seed2 = 300
# a1 = 40014
# a2 = 40692
# m1 = 2147483563
# m2 = 2147483399
# mean = 10.35791
# EXPDist_RVG(100, 300, 40014, 2147483563, 40692, 2147483399, 10.35791)

# initialize csv files for getting data
if (os.path.exists('data.csv')):
    os.remove('data.csv')
header = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ('arrival_time (minutes)','event_type','p1 throughput','p2 throughput','p3 throughput','ins1 blocked time','ins2 blocked time','ws1 idle time','ws2 idle time','ws3 idle time','c1_ws1 occp','c1_ws2 occp','c1_ws3 occp','c2_ws2 occp','c3_ws3 occp','c1 used','c2 used','c3 used','ins1 state','ins2 state','c1_ws1 capacity','c1_ws2 capacity','c3_ws3 capacity','c2_ws2 capacity','c3_ws3 capacity','ws1 state','ws2 state','ws3 state','p1 produced','p1 produced','p3 produced')
with open("data.csv", "a") as f:
    f.write(header)

# function for appending to csv file
def appendToCSV(arrival_time, event_type):
    global p1_t,p2_t,p3_t,ins1_w,ins1_b,ins2_w,ins2_b,ws1_w,ws1_i,ws2_w,ws2_i,ws3_w,ws3_i,c1_ws1_o,c1_ws2_o,c1_ws3_o,c2_ws2_o,c3_ws3_o,c1_ws1_s,c1_ws1_o,c1_ws2_s,c1_ws2_o,c1_ws3_s,c1_ws3_o,c2_ws2_s,c2_ws2_o,c3_ws3_s,c3_ws3_o

    if not sim_time == 0:
        p1_t = Decimal(p1) / Decimal(sim_time)
        p2_t = Decimal(p2) / Decimal(sim_time)
        p3_t = Decimal(p3) / Decimal(sim_time)
    ins1_b = Decimal(sim_time) - Decimal(ins1_w)
    ins1_b = Decimal(sim_time) - Decimal(ins1_w)
    ws1_i = Decimal(sim_time) - Decimal(ws1_w)
    ws2_i = Decimal(sim_time) - Decimal(ws2_w)
    ws3_i = Decimal(sim_time) - Decimal(ws3_w)

    new_row = "\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(arrival_time),event_type,str(p1_t),str(p2_t),str(p3_t),str(ins1_b),str(ins2_b),str(ws1_i),str(ws2_i),str(ws3_i),str(c1_ws1_o),str(c1_ws2_o),str(c1_ws3_o),str(c2_ws2_o),str(c3_ws3_o),str(c1),str(c2),str(c3),str(ins1),str(ins2),str(c1_ws1),str(c1_ws2),str(c1_ws3),str(c2_ws2),str(c3_ws3),str(ws1),str(ws2),str(ws3),str(p1),str(p2),str(p3))
    with open("data.csv", "a") as f:
        f.write(new_row)

# read input files
def read_dat_files(file_name):
    data = open(file_name).read().splitlines()
    data = [i.strip() for i in data]
    data = list(filter(None, data))
    output = []
    for i in data:
        output.append((Decimal(i)))
    return output

ins1_input = read_dat_files('input files/servinsp1.dat')
ins22_input = read_dat_files('input files/servinsp22.dat')
ins23_input = read_dat_files('input files/servinsp23.dat')
ws1_input = read_dat_files('input files/ws1.dat')
ws2_input = read_dat_files('input files/ws2.dat')
ws3_input = read_dat_files('input files/ws3.dat')

# simulation states
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

# stats calculation states
p1_t = 0 # product throughput
p2_t = 0
p3_t = 0
ins1_w = 0 # work time
ins1_b = 0 # blocked time
ins2_w = 0
ins2_b = 0
ws1_w = 0 # work time
ws1_i = 0 # idle time
ws2_w = 0
ws2_i = 0
ws3_w = 0
ws3_i = 0
c1_ws1_s = 0 # buffer total sum
c1_ws1_o = 0 # buffer occupancy
c1_ws2_s = 0
c1_ws2_o = 0
c1_ws3_s = 0
c1_ws3_o = 0
c2_ws2_s = 0
c2_ws2_o = 0
c3_ws3_s = 0
c3_ws3_o = 0

sim_time = 0
fel = []
fel.append([0, 'ins1'])
fel.append([0, 'ins2'])
heapq.heapify(fel)

while True:
    if sim_time > 1000:
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

    prev_sim_time = sim_time

    print(fel)
    # pop min event from fel
    sim_time, event_type = heapq.heappop(fel)

    time_interval = sim_time - prev_sim_time

    c1_ws1_s += c1_ws1 * time_interval
    c1_ws2_s += c1_ws2 * time_interval
    c1_ws3_s += c1_ws3 * time_interval
    c2_ws2_s += c2_ws2 * time_interval
    c3_ws3_s += c3_ws3 * time_interval

    if not sim_time == 0:
        c1_ws1_o = Decimal(c1_ws1_s) / Decimal(sim_time)
        c1_ws2_o = Decimal(c1_ws2_s) / Decimal(sim_time)
        c1_ws3_o = Decimal(c1_ws3_s) / Decimal(sim_time)
        c2_ws2_o = Decimal(c2_ws2_s) / Decimal(sim_time)
        c3_ws3_o = Decimal(c3_ws3_s) / Decimal(sim_time)

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
        if c1_ws1 > 0:
            c1_ws1 -= 1
            appendToCSV(sim_time,'ws1 started')
        else:
            ws = 0
    elif event_type == 'ws1_done':
        ws1 = 0
        p1 += 1
        appendToCSV(sim_time,'ws1 end produce to p1')

    elif event_type == 'ws2':
        ws2 = 1
        if c1_ws2 > 0 and c2_ws2 > 0:
            c1_ws2 -= 1
            c2_ws2 -= 1
            appendToCSV(sim_time,'ws2 started')
        else:
            ws2 = 0
    elif event_type == 'ws2_done':
        ws2 = 0
        p2 += 1
        appendToCSV(sim_time,'ws2 end produce to p2')

    elif event_type == 'ws3':
        ws3 = 1
        if c1_ws3 > 0 and c3_ws3 > 0:
            c1_ws3 -= 1
            c3_ws3 -= 1
            appendToCSV(sim_time,'ws3 started')
        else:
            ws3 = 0
    elif event_type == 'ws3_done':
        ws3 = 0
        p3 += 1
        appendToCSV(sim_time,'ws3 end produce to p3')

print(f'simulation ran for: ', {sim_time}, ' seconds')
print(f'products created: p1: ', {p1}, ' p2: ', {p2}, ' p3: ', {p3})

print(f'c1_ws1 average occupancy: {c1_ws1_o}')
print(f'c1_ws2 average occupancy: {c1_ws2_o}')
print(f'c2_ws2 average occupancy: {c2_ws2_o}')
print(f'c1_ws3 average occupancy: {c1_ws3_o}')
print(f'c3_ws3 average occupancy: {c3_ws3_o}')
