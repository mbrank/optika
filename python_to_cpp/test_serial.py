import multiprocessing

# setup output lists
output1 = list()
output2 = list()
output3 = list()
offset = 1


def calc_stuff(args):
    return 1*args, 1*args, 1*args

for j in range(0, 100000000):
    # calc individual parameter value
    parameter = j * offset
    # call the calculation
    out1, out2, out3 = calc_stuff(j)

    # put results into correct output list
    output1.append(out1)
    output2.append(out2)
    output3.append(out3)
