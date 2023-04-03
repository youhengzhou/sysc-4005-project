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

# part 1 verification, we are building our system right:

-   our output never exceeds our input

    -   screenshot of we don't use more components than our products

-   our buffer never exceeds 2 or less than 1

    -   screenshot

# part 2 verification, using little's law:

little's law

L: average number of items in a system, average buffer occupancy
lambda: the average rate at which items enter and leave the system,
W: average time that each item spends in the system

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

# part 4: OC curve

use OC curve to find replications

x axis: alpha, accepting h0 percentage, 0 -> 100
y axis: beta, fail to reject null hypo when it's false, 0 -> 0.5

average of all trials

we do 1 min/standard deviation of avg of all buffer occupancy trials

# part 5: initialization time

use ensemble averages to find initialization time

# part 6: confidence interval

with replications, find standard deviation

each of the buffer
