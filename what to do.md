-   3x facility throughput as products per unit time

-   2x inspector blocked time (as fraction of total simulation time)

-   3x workstation idle time (as fraction of total simulation time)

-   5x average buffer occupancy for each buffer

-   5x additionally to validate the simulation using Little's law you need to track how long each component spends in a given buffer. (and output the average time for each buffer) This may be difficult for groups that only track the number of components and do not have a data structure associated with the components.
p1_t = 0
p2_t = 0
p3_t = 0
ins1_b = 0
ins2_b = 0
ws1_i = 0
ws2_i = 0
ws3_i = 0
c1_ws1_o = 0
c1_ws2_o = 0
c1_ws3_o = 0
c2_ws2_o = 0
c3_ws3_o = 0