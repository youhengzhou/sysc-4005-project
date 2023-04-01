import math
import jsoneng

jsoneng.create({})

def CLCG(x1, x2, a1, m1, a2, m2):
    for i in range(300):
        # step 2, for each individual generator
        # x1,j+1 = a1 * x1,j mod m1
        # x2,j+1 = a1 * x2,j mod m2
        x1 = (a1 * x1) % m1
        x2 = (a2 * x2) % m2

        # step 3:
        # xj+1 = (x1,j+1 - x2,j+1) mod 2147483562
        xj = (x1 - x2) % (2147483562)

        # step 4:
        # if xj+1 > 0, Rj+1 = xj+1 / 2147483563
        # if xj+1 = 0, Rj+1 = 2147483562 / 2147483563
        if xj > 0:
            randomNumberForCycle = xj / 2147483563
        else:
            randomNumberForCycle = 2147483562 / 2147483563

        print('for cycle ' + str(i+1) + ' x1 is ' + str(x1))
        print('for cycle ' + str(i+1) + ' x2 is ' + str(x2))
        print('for cycle ' + str(i+1) + ' random number is ' + str(randomNumberForCycle))
        # print(randomNumberForCycle)

# step 1
# seed1 = 100
# seed2 = 300
# a1 = 40014
# a2 = 40692
# m1 = 2147483563
# m2 = 2147483399
CLCG(100, 300, 40014, 2147483563, 40692, 2147483399)




def EXPDist_RVG(x1, x2, a1, m1, a2, m2, mean):
    for i in range(300):
        # step 2, for each individual generator
        # x1,j+1 = a1 * x1,j mod m1
        # x2,j+1 = a1 * x2,j mod m2
        x1 = (a1 * x1) % m1
        x2 = (a2 * x2) % m2

        # step 3:
        # xj+1 = (x1,j+1 - x2,j+1) mod 2147483562
        xj = (x1 - x2) % (2147483562)

        # step 4:
        # if xj+1 > 0, Rj+1 = xj+1 / 2147483563
        # if xj+1 = 0, Rj+1 = 2147483562 / 2147483563
        if xj > 0:
            randomNumberForCycle = xj / 2147483563
        else:
            randomNumberForCycle = 2147483562 / 2147483563

        # step 5:
        # finds the random number that follows the exponential distribution
        randomEXPDist = -1/(1/mean) * math.log(1 - randomNumberForCycle)

        print(randomEXPDist)

# step 1
# seed1 = 100
# seed2 = 300
# a1 = 40014
# a2 = 40692
# m1 = 2147483563
# m2 = 2147483399
# mean = 10.35791
# EXPDist_RVG(100, 300, 40014, 2147483563, 40692, 2147483399, 10.35791)


















def CLCGTest(x1, x2, x3, a1, a2, a3, m1, m2, m3):

    for i in range(5):
        x1 = (a1 * x1) % m1
        x2 = (a2 * x2) % m2
        x3 = (a3 * x3) % m3

        xj = x1 - x2 + x3 % m1

        randomNum = xj / m1
        
        # if randomNum < 1:
        #     randomNum += m1 - 1

        # randomNum = randomNum / m1

        jsoneng.patch_kv('x'+str(i+1),{'x1':x1,'x2':x2,'x3':x3,'randomNum':randomNum})

# CLCGTest(100,300,500,157,146,142,32363,31727,31657)
