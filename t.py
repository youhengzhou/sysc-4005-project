elif event_type == 'ins1_done':
            if counter == 1:
                if c1_ws1 < 2:
                    ins1 = 0
                    c1_ws1 += 1
                    c1_ws1_t += 1
                    appendToCSV(sim_time,'ins1 end produce to c1_ws1')
            elif counter == 2:
                if c1_ws2 < 2:
                    ins1 = 0
                    c1_ws2 += 1
                    c1_ws2_t += 1
                    appendToCSV(sim_time,'ins1 end produce to c1_ws2')
            else:
                if c1_ws3 < 2:
                    ins1 = 0
                    c1_ws3 += 1
                    c1_ws3_t += 1
                    appendToCSV(sim_time,'ins1 end produce to c1_ws3')
            counter = (counter + 1) % 3