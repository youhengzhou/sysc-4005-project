-   3x facility throughput as products per unit time

-   2x inspector blocked time (as fraction of total simulation time)

-   3x workstation idle time (as fraction of total simulation time)

-   5x average buffer occupancy for each buffer

-   5x additionally to validate the simulation using Little's law you need to track how long each component spends in a given buffer. (and output the average time for each buffer) This may be difficult for groups that only track the number of components and do not have a data structure associated with the components.

mean of:

ins1
ins22
ins23
ws1
ws2
ws3

# part 1 validation, we are building our system right:

-   code review, writing, youheng

    -   independent individual review the model code of part they didn't do

-   flow chart, leenesh does it first, then we critique it

-   check output for reasonableness, screenshots, youheng

    -   queue size cannot be more than 2, or less than 0
    -   throughput not negative
    -   component in
    -   product out
        -   should match up

_- other validation alternatives, imran_

# part 2 verification, using little's law:

little's law, youheng

L: average number of items in a system, average buffer occupancy
lambda: the average rate at which items enter and leave the system,
W: average time that each item spends in the system

buffer is now [1|2] and time [1'stime,2'stime]

L: total number used
lambda: total number used / sim_time
W: time component is in inspector + time component is in buffer + time component is in workstation

-   system

    -   c1 + c2 + c3
    -   L:
    -   lambda:
    -   W:

-   c1_ws1 buffer

    -   L:
    -   lambda:
    -   W:

-   c1_ws2 buffer

    -   L:
    -   lambda:
    -   W:

-   c1_ws3 buffer

    -   L:
    -   lambda:
    -   W:

-   c2_ws2 buffer

    -   L:
    -   lambda:
    -   W:

-   c3_ws3 buffer

    -   L:
    -   lambda:
    -   W:

0.470099549/0.010998983

# part 3: validation

compare with pdf numbers, 20% confidence interval

# part 4: OC curve, imran

we pick critical diff

critical diff divide stnd dev

sigma on x axis

1 - sigma for y axis

find closest number on OC curve

use OC curve to find n value, number of replications

x axis: alpha, accepting h0 percentage, 0 -> 100
y axis: beta, fail to reject null hypo when it's false, 0 -> 0.5

average of all trials

we do 1 min/standard deviation of avg of all buffer occupancy trials, for like 30 trials

we find beta, and then do 1 - beta to find alpha, which is our y axis

# part 5: initialization time, imran

use ensemble averages to find initialization time, and eyeball it

# part 6: confidence interval, imran

with replications, find standard deviation

each of the buffer

Y +- t table state \* stnd dev / sqrt(n of replications)

# answers

**Flight List**

**Model verification and validation**

How we verified our model

Different validation alternatives

Little’s law to verify our code

Input-output validation

**Product runs and analysis**

Find quantities of interest

Perform replications, show replications are enough

Find initialization phase with proper length

Find confidence interval of each quantity
