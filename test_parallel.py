import multiprocessing

# setup output lists
output1 = list()
output2 = list()
output3 = list()
offset = 1


def calc_stuff(args, a=1, b=2):
    return 1*args, 1*args*a, 1*args*b

pool = multiprocessing.Pool(4)
out1, out2, out3 = zip(*pool.map(calc_stuff,
                                 range(0, 10 * offset,
                                       offset)))

