from decimal import *
import heapq
import math
import random
import os

# CLCG from milestone 2
def EXPDist_RVG(mean):
    global x1,x2
    # x1 = 18943
    # x2 = 30084
    
    a1 = 40014
    a2 = 40692
    m1 = 2147483563
    m2 = 2147483399
    
    x1 = (a1 * x1) % m1
    x2 = (a2 * x2) % m2
    xj = (x1 - x2) % (2147483562)
    if xj > 0:
        randomNumberForCycle = xj / 2147483563
    else:
        randomNumberForCycle = 2147483562 / 2147483563
    return Decimal(-1/(1/mean) * math.log(1 - randomNumberForCycle))

# function for appending to csv file
# def appendToCSV(arrival_time, event_type):
#     global sim_time
#     global c1_t,c2_t,c3_t,p1_t,p2_t,p3_t,ins1_w,ins1_b,ins2_w,ins2_b,ws1_w,ws1_i,ws2_w,ws2_i,ws3_w,ws3_i,c1_ws1_o,c1_ws2_o,c1_ws3_o,c2_ws2_o,c3_ws3_o,c1_ws1_s,c1_ws1_o,c1_ws2_s,c1_ws2_o,c1_ws3_s,c1_ws3_o,c2_ws2_s,c2_ws2_o,c3_ws3_s,c3_ws3_o

#     if not sim_time == 0:
#         c1_t = Decimal(c1) / Decimal(sim_time)
#         c2_t = Decimal(c2) / Decimal(sim_time)
#         c3_t = Decimal(c3) / Decimal(sim_time)
#         p1_t = Decimal(p1) / Decimal(sim_time)
#         p2_t = Decimal(p2) / Decimal(sim_time)
#         p3_t = Decimal(p3) / Decimal(sim_time)
#     if Decimal(sim_time) - Decimal(ins1_w) >= 0 and ins1 == 0:
#         ins1_b = Decimal(sim_time) - Decimal(ins1_w)
#     if Decimal(sim_time) - Decimal(ins2_w) >= 0 and ins2 == 0:
#         ins2_b = Decimal(sim_time) - Decimal(ins2_w)
#     ws1_i = Decimal(sim_time) - Decimal(ws1_w)
#     ws2_i = Decimal(sim_time) - Decimal(ws2_w)
#     ws3_i = Decimal(sim_time) - Decimal(ws3_w)

#     new_row = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (str(arrival_time),event_type,str(c1_t),str(c2_t),str(c3_t),str(p1_t),str(p2_t),str(p3_t),str(ins1_b),str(ins2_b),str(ws1_i),str(ws2_i),str(ws3_i),str(c1_ws1_o),str(c1_ws2_o),str(c1_ws3_o),str(c2_ws2_o),str(c3_ws3_o),str(c1),str(c2),str(c3),str(ins1),str(ins2),str(c1_ws1),str(c1_ws2),str(c1_ws3),str(c2_ws2),str(c3_ws3),str(ws1),str(ws2),str(ws3),str(p1),str(p2),str(p3))
#     with open("data.csv", "a") as f:
#         f.write(new_row)

def appendToCSV(arrival_time, event_type):
    global sim_time
    global c1_t,c2_t,c3_t,p1_t,p2_t,p3_t,ins1_w,ins1_b,ins2_w,ins2_b,ws1_w,ws1_i,ws2_w,ws2_i,ws3_w,ws3_i,c1_ws1_o,c1_ws2_o,c1_ws3_o,c2_ws2_o,c3_ws3_o,c1_ws1_s,c1_ws1_o,c1_ws2_s,c1_ws2_o,c1_ws3_s,c1_ws3_o,c2_ws2_s,c2_ws2_o,c3_ws3_s,c3_ws3_o

    if not sim_time == 0:
        c1_t = Decimal(c1) / Decimal(sim_time)
        c2_t = Decimal(c2) / Decimal(sim_time)
        c3_t = Decimal(c3) / Decimal(sim_time)
        p1_t = Decimal(p1) / Decimal(sim_time)
        p2_t = Decimal(p2) / Decimal(sim_time)
        p3_t = Decimal(p3) / Decimal(sim_time)
    if Decimal(sim_time) - Decimal(ins1_w) >= 0 and ins1 == 0:
        ins1_b = Decimal(sim_time) - Decimal(ins1_w)
    if Decimal(sim_time) - Decimal(ins2_w) >= 0 and ins2 == 0:
        ins2_b = Decimal(sim_time) - Decimal(ins2_w)
    ws1_i = Decimal(sim_time) - Decimal(ws1_w)
    ws2_i = Decimal(sim_time) - Decimal(ws2_w)
    ws3_i = Decimal(sim_time) - Decimal(ws3_w)

    new_row = "%s,%s,%s,%s\n" % (str(arrival_time),str(p1),str(p2),str(p3))
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

# simulation states
# simulation time for event sorting
sim_time = 0
# future event list, a priority queue
fel = []
# global states for CLCG x1 and x2
x1 = 0
x2 = 0

# factory states
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
c1_l = 0 # little's law L numerator
c2_l = 0
c3_l = 0
c1_s = 0 # little's law lambda numerator
c2_s = 0
c3_s = 0
c1_t = 0 # component take in rate
c2_t = 0
c3_t = 0
c1_s = 0 # component in system (total)
c2_s = 0
c3_s = 0
c1_o = 0 # component in system (average)
c2_o = 0
c3_o = 0
c1_w = 0
c2_w = 0
c3_w =0
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
c1_ws1_s = 0 # buffer time interval sum
c1_ws1_o = 0 # buffer occupancy
c1_ws1_t = 0 # buffer total count
c1_ws2_s = 0
c1_ws2_o = 0
c1_ws2_t = 0
c1_ws3_s = 0
c1_ws3_o = 0
c1_ws3_t = 0
c2_ws2_s = 0
c2_ws2_o = 0
c2_ws2_t = 0
c3_ws3_s = 0
c3_ws3_o = 0
c3_ws3_t = 0

def sim(clcg_x1, clcg_x2):
    global sim_time, fel, x1, x2
    global c1,c2,c3,ins1,ins2,c1_ws1,c1_ws2,c1_ws3,c2_ws2,c3_ws3,ws1,ws2,ws3,p1,p2,p3
    global c1_l,c2_l,c3_l,c1_ws1_t,c1_ws2_t,c1_ws3_t,c2_ws2_t,c3_ws3_t,c1_w,c2_2,c3_w,c1_s,c2_s,c3_s,c1_o,c2_o,c3_o,p1_t,p2_t,p3_t,ins1_w,ins1_b,ins2_w,ins2_b,ws1_w,ws1_i,ws2_w,ws2_i,ws3_w,ws3_i,c1_ws1_o,c1_ws2_o,c1_ws3_o,c2_ws2_o,c3_ws3_o,c1_ws1_s,c1_ws1_o,c1_ws2_s,c1_ws2_o,c1_ws3_s,c1_ws3_o,c2_ws2_s,c2_ws2_o,c3_ws3_s,c3_ws3_o
    global c1_ws1_times,c1_ws2_times,c1_ws3_times,c2_ws2_times,c3_ws3_times,c1_ws1_times_c,c1_ws2_times_c,c1_ws3_times_c,c2_ws2_times_c,c3_ws3_times_c,c1_ws1_times_w,c1_ws2_times_w,c1_ws3_times_w,c2_ws2_times_w,c3_ws3_times_w

    # initialize csv files for getting data
    if (os.path.exists('data.csv')):
        os.remove('data.csv')
    # header = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % ('arrival_time (minutes)','event_type','c1 average input rate','c2 average input rate','c3 average input rate','p1 throughput','p2 throughput','p3 throughput','ins1 blocked time','ins2 blocked time','ws1 idle time','ws2 idle time','ws3 idle time','c1_ws1 occp','c1_ws2 occp','c1_ws3 occp','c2_ws2 occp','c3_ws3 occp','c1 used','c2 used','c3 used','ins1 state','ins2 state','c1_ws1 capacity','c1_ws2 capacity','c3_ws3 capacity','c2_ws2 capacity','c3_ws3 capacity','ws1 state','ws2 state','ws3 state','p1 produced','p2 produced','p3 produced')
    # with open("data.csv", "a") as f:
    #     f.write(header)
    
    header = "%s,%s,%s,%s\n" % ('arrival_time (minutes)','p1 throughput','p2 throughput','p3 throughput')
    with open("data.csv", "a") as f:
        f.write(header)

    # take in seeds for clcg
    x1 = clcg_x1
    x2 = clcg_x2

    while True:
        if sim_time > 10000:
            break

        # check states, create events to be handled
        # if entity is 0, create start event
        # if entity is 1, create end event

        # check if ins1 start and finish events can be created
        if ins1 == 0 and (c1_ws1 < 2 or c1_ws2 < 2 or c1_ws3 < 2) and not any(event[1] == 'ins1' for event in fel):
            heapq.heappush(fel,([sim_time, 'ins1']))
        if ins1 == 1 and (c1_ws1 < 2 or c1_ws2 < 2 or c1_ws3 < 2) and not any(event[1] == 'ins1_done' for event in fel):
            work_time = EXPDist_RVG(10.35791)
            ins1_w += work_time
            heapq.heappush(fel,([sim_time + work_time, 'ins1_done']))
        
        # check if ins2 start and finish events can be created
        if ins2 == 0 and (c2_ws2 < 0 or c3_ws3 < 2) and (not any(event[1] == 'ins22' for event in fel)) and (not any(event[1] == 'ins23' for event in fel)):
            if random.randint(0,1) == 0:
                heapq.heappush(fel,([sim_time, 'ins22']))
            else:
                heapq.heappush(fel,([sim_time, 'ins23']))
        if ins2 == 2 and (c2_ws2 < 2) and not any(event[1] == 'ins22_done' for event in fel):
            work_time = EXPDist_RVG(15.53690333)
            ins2_w += work_time
            heapq.heappush(fel,([sim_time + work_time, 'ins22_done']))
        if ins2 == 3 and (c3_ws3 < 2) and not any(event[1] == 'ins23_done' for event in fel):
            work_time = EXPDist_RVG(20.63275667)
            ins2_w += work_time
            heapq.heappush(fel,([sim_time + work_time, 'ins23_done']))

        # check if ws1 start and finish events can be created
        if ws1 == 0 and c1_ws1 > 0 and not any(event[1] == 'ws1' for event in fel):
            heapq.heappush(fel,([sim_time, 'ws1']))
        if ws1 == 1 and c1_ws1 > 0 and not any(event[1] == 'ws1_done' for event in fel):
            work_time = EXPDist_RVG(4.604416667)
            ws1_w += work_time
            heapq.heappush(fel,([sim_time + work_time, 'ws1_done']))

        # check if ws2 start and finish events can be created
        if ws2 == 0 and c1_ws2 > 0 and c2_ws2 > 0 and not any(event[1] == 'ws2' for event in fel):
            heapq.heappush(fel,([sim_time, 'ws2']))
        if ws2 == 1 and c1_ws2 > 0 and c2_ws2 > 0 and not any(event[1] == 'ws2_done' for event in fel):
            work_time = EXPDist_RVG(11.09260667)
            ws2_w += work_time
            heapq.heappush(fel,([sim_time + work_time, 'ws2_done']))
        
        # check if ws3 start and finish events can be created
        if ws3 == 0 and c1_ws3 > 0 and c3_ws3 > 0 and not any(event[1] == 'ws3' for event in fel):
            heapq.heappush(fel,([sim_time, 'ws3']))
        if ws3 == 1 and c1_ws3 > 0 and c3_ws3 > 0 and not any(event[1] == 'ws3_done' for event in fel):
            work_time = EXPDist_RVG(8.79558)
            ws3_w += work_time
            heapq.heappush(fel,([sim_time + work_time, 'ws3_done']))
        
        # find prev_sim_time for average buffer occupancy calculations
        prev_sim_time = sim_time
        
        # pop min event from fel
        sim_time, event_type = heapq.heappop(fel)

        # calculate average buffer occupancies
        time_interval = sim_time - prev_sim_time

        # time interval of component in the buffer
        c1_ws1_s += c1_ws1 * time_interval
        c1_ws2_s += c1_ws2 * time_interval
        c1_ws3_s += c1_ws3 * time_interval
        c2_ws2_s += c2_ws2 * time_interval
        c3_ws3_s += c3_ws3 * time_interval

        # time interval of component in the facility
        c1_l += c1_s * time_interval
        c2_l += c2_s * time_interval
        c3_l += c3_s * time_interval

        if not sim_time == 0:
            c1_ws1_o = Decimal(c1_ws1_s) / Decimal(sim_time)
            c1_ws2_o = Decimal(c1_ws2_s) / Decimal(sim_time)
            c1_ws3_o = Decimal(c1_ws3_s) / Decimal(sim_time)
            c2_ws2_o = Decimal(c2_ws2_s) / Decimal(sim_time)
            c3_ws3_o = Decimal(c3_ws3_s) / Decimal(sim_time) 

            c1_o = Decimal(c1_l) / Decimal(sim_time)
            c2_o = Decimal(c2_l) / Decimal(sim_time)
            c3_o = Decimal(c3_l) / Decimal(sim_time)

        # handle events, change state
        # "start events" toggle entity state to 1
        # "end events" check if product queue is free, then produce product, then toggle entity state to 0
        
        # handle ins1 start and done events
        if event_type == 'ins1':
            ins1 = 1
            c1 += 1
            c1_s += 1
            appendToCSV(sim_time,'ins1 started')
        elif event_type == 'ins1_done':
            buffers = []
            buffers.append([c1_ws1,'c1_ws1'])
            buffers.append([c1_ws2,'c1_ws2'])
            buffers.append([c1_ws3,'c1_ws3'])
            buffers.sort()
            if buffers[0][0] < 2:
                ins1 = 0
                if buffers[0][1] == 'c1_ws1':
                    c1_ws1 += 1
                    c1_ws1_t += 1
                    appendToCSV(sim_time,'ins1 end produce to c1_ws1')
                elif buffers[0][1] == 'c1_ws2':
                    c1_ws2 += 1
                    c1_ws2_t += 1
                    appendToCSV(sim_time,'ins1 end produce to c1_ws2')
                else:
                    c1_ws3 += 1
                    c1_ws3_t += 1
                    appendToCSV(sim_time,'ins1 end produce to c1_ws3')
        
        # handle ins2 start and done events
        # ins22 is for component 2
        # ins23 is for component 3
        elif event_type == 'ins22':
            ins2 = 2
            c2 += 1
            c2_s += 1
            appendToCSV(sim_time,'ins2 started for c2')
        elif event_type == 'ins23':
            ins2 = 3
            c3 += 1
            c3_s += 1
            appendToCSV(sim_time,'ins2 started for c3')
        elif event_type == 'ins22_done':
            if c2_ws2 < 2:
                ins2 = 0
                c2_ws2 += 1
                c2_ws2_t += 1
                appendToCSV(sim_time,'ins2 end produce to c2_ws2')
        elif event_type == 'ins23_done':
            if c3_ws3 < 2:
                ins2 = 0
                c3_ws3 += 1
                c3_ws3_t += 1
                appendToCSV(sim_time,'ins2 end produce to c3_ws3')

        # handle ws1 start and done events
        elif event_type == 'ws1':
            if c1_ws1 > 0:
                ws1 = 1
                c1_ws1 -= 1
                appendToCSV(sim_time,'ws1 started')
        elif event_type == 'ws1_done':
            ws1 = 0
            p1 += 1
            c1_s -= 1
            appendToCSV(sim_time,'ws1 end produce to p1')

        # handle ws2 start and done events
        elif event_type == 'ws2':
            if c1_ws2 > 0 and c2_ws2 > 0:
                ws2 = 1
                c1_ws2 -= 1
                c2_ws2 -= 1
                appendToCSV(sim_time,'ws2 started')
        elif event_type == 'ws2_done':
            ws2 = 0
            p2 += 1
            c1_s -= 1
            c2_s -= 1
            appendToCSV(sim_time,'ws2 end produce to p2')

        # handle ws3 start and done events
        elif event_type == 'ws3':
            if c1_ws3 > 0 and c3_ws3 > 0:
                ws3 = 1
                c1_ws3 -= 1
                c3_ws3 -= 1
                appendToCSV(sim_time,'ws3 started')
        elif event_type == 'ws3_done':
            ws3 = 0
            p3 += 1
            c1_s -= 1
            c3_s -= 1
            appendToCSV(sim_time,'ws3 end produce to p3')

    print(f'simulation ran for:', {sim_time}, 'minutes')
    print(f'components used: c1:', {c1}, 'c2:', {c2}, 'c3:', {c3})
    print(f'products created: p1:', {p1}, 'p2:', {p2}, 'p3:', {p3})

    # total components little's law
    print('facility littles law')
    print(f'L c1: {c1_o}')
    print(f'L c2: {c2_o}')
    print(f'L c3: {c3_o}')

    print(f'lambda c1 take in rate: {c1_s/sim_time}')
    print(f'lambda c2 take in rate: {c2_s/sim_time}')
    print(f'lambda c3 take in rate: {c3_s/sim_time}')

    print(f'W c1: {c1_l/c1_s}')
    print(f'W c2: {c2_l/c2_s}')
    print(f'W c3: {c3_l/c3_s}')

    # buffers little's law
    print('buffers littles law')
    print(f'L c1_ws1 average occupancy: {c1_ws1_o}')
    print(f'L c1_ws2 average occupancy: {c1_ws2_o}')
    print(f'L c2_ws2 average occupancy: {c2_ws2_o}')
    print(f'L c1_ws3 average occupancy: {c1_ws3_o}')
    print(f'L c3_ws3 average occupancy: {c3_ws3_o}')

    print(f'lambda c1_ws1: {c1_ws1_t/sim_time}')
    print(f'lambda c1_ws2: {c1_ws2_t/sim_time}')
    print(f'lambda c2_ws2: {c2_ws2_t/sim_time}')
    print(f'lambda c1_ws3: {c1_ws3_t/sim_time}')
    print(f'lambda c3_ws3: {c3_ws3_t/sim_time}')

    print(f'W c1_ws1: {c1_ws1_s/c1_ws1_t}')
    print(f'W c1_ws2: {c1_ws2_s/c1_ws2_t}')
    print(f'W c2_ws2: {c2_ws2_s/c2_ws2_t}')
    print(f'W c1_ws3: {c1_ws3_s/c1_ws3_t}')
    print(f'W c3_ws3: {c3_ws3_s/c3_ws3_t}')

    print(f'ins1 work time: {ins1_w}')
    print(f'ins1 blocked time: {ins1_b}')
    print(f'ins2 work time: {ins2_w}')
    print(f'ins2 blocked time: {ins2_b}')

    print(f'ws1 work time: {ws1_w}')
    print(f'ws1 blocked time: {ws1_i}')

    print(f'ws2 work time: {ws2_w}')
    print(f'ws2 blocked time: {ws2_i}')

    print(f'ws3 work time: {ws3_w}')
    print(f'ws3 blocked time: {ws3_i}')

sim(10423,12140)
