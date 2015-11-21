import itertools
import sys
import time

sys.setrecursionlimit(100000)

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()

    def __exit__(self, type, value, traceback):
        print("Elapsed time: {:.3f} sec".format(time.time() - self._startTime))


functions = []
with open('results_small.txt', 'r') as f:
    functions = [tuple([int(x) for x in line.strip()[1:-1].split(',')]) for line in f.readlines()]

boolean_sets = list(itertools.product(range(2), repeat=4))
#print(len(boolean_sets))
#print(len(functions[0]))

boolean_sets_mapping = dict(zip(range(8), boolean_sets))
#print(boolean_sets_mapping)

def get_min_difference(functions, checked_i_lst):
    min_difference = -1
    #min_boolean_set = -1
    min_boolean_sets = []
    min_f0s = []
    min_f1s = []
    for i in range(8):
        if i in checked_i_lst:
            continue
        f0 = []
        f1 = []
        for function in functions:
            if function[i] == 0:
                f0.append(function)
            else:
                f1.append(function)
        current_difference = abs(len(f1) - len(f0))
        if current_difference < min_difference or min_difference == -1:
            min_difference = current_difference
            #min_boolean_set = i
            min_boolean_sets = [i,]
            min_f0 = f0[:]
            min_f1 = f1[:]
            min_f0s = [min_f0,]
            min_f1s = [min_f1,]
        elif current_difference == min_difference:
            min_difference = current_difference
            #min_boolean_set = i
            min_boolean_sets.append(i)
            #print(min_boolean_sets)
            min_f0 = f0[:]
            min_f1 = f1[:]
            min_f0s.append(min_f0)
            min_f1s.append(min_f1)
    return min_boolean_sets, min_f0s, min_f1s


def func1(min_f0, checked_i_lst_1, binary, depth):
    min_boolean_sets_1, min_f0s_1, min_f1s_1 = get_min_difference(min_f0, checked_i_lst_1)
    #new_depth = depth + 1
    if depth >= 4:
        cases_1_1 = []
        for i_1, min_f0_1, min_f1_1 in zip(min_boolean_sets_1, min_f0s_1, min_f1s_1):
            yield(str(depth) + ":" + binary + "-" + str(i_1) + "-" + str(len(min_f0_1)) + " " + str(len(min_f1_1)))
            #yield("\t======DEPTH=" + str(depth) + "-" + binary + "========" + str(i_1) + "===" + str(len(min_f0_1)) + " " + str(len(min_f1_1)))
            #cases_1_1.append("\t======DEPTH=" + str(depth) + "-" + binary + "========" + str(i_1) + "===" + str(len(min_f0_1)) + " " + str(len(min_f1_1)))
        #return cases_1_1
    else:
        new_depth = depth + 1
        cases = []

        for i_1, min_f0_1, min_f1_1 in zip(min_boolean_sets_1, min_f0s_1, min_f1s_1):
            checked_i_lst_new = checked_i_lst_1[:]
            checked_i_lst_new.append(i_1)
            #cases_1_1 = func1(min_f0_1, checked_i_lst_new, "0", new_depth)
            #cases_1_2 = func1(min_f1_1, checked_i_lst_new, "1", new_depth)
            for case1_1 in func1(min_f0_1, checked_i_lst_new, "0", new_depth):
                for case2_1 in func1(min_f1_1, checked_i_lst_new, "1", new_depth):
                    if not (depth == 4 and (len(min_f0_1) > 16 or len(min_f1_1) > 16)):
                        #print(len(min_f0_1), len(min_f1_1))
                        yield (str(depth)+":" + binary + "-" + str(i_1) + "-" + str(len(min_f0_1)) + " " + str(len(min_f1_1))+'\n' + '\t'*depth + case1_1 + '\n' + '\t'*depth + case2_1)
                    #else:
                    #    print(len(min_f0_1), len(min_f1_1))
                    #yield("\t======DEPTH=" + str(depth)+"-" + binary + "========" + str(i_1) + "===" + str(len(min_f0_1)) + " " + str(len(min_f1_1))+'\n' + '\t'*depth + case1_1 + '\n' + '\t'*depth + case2_1 + '\n')
                    #cases.append("\t======DEPTH=" + str(depth)+"-" + binary + "========" + str(i_1) + "===" + str(len(min_f0_1)) + " " + str(len(min_f1_1))+'\n' + '\t'*depth + case1_1 + '\n' + '\t'*depth + case2_1 + '\n')
        #return
        #return cases

def very_new_deep_functions(functions):
    checked_i_lst = []
    min_boolean_sets, min_f0s, min_f1s = get_min_difference(functions, checked_i_lst)

    cases = []
    for i, min_f0, min_f1 in zip(min_boolean_sets, min_f0s, min_f1s):
        checked_i_lst_1 = checked_i_lst[:]
        checked_i_lst_1.append(i)
        #cases_1 = func(min_f0, checked_i_lst_1, "0")
        #cases_2 = func(min_f1, checked_i_lst_1, "1")
        #cases_1 = func1(min_f0, checked_i_lst_1, "0",2)
        #cases_2 = func1(min_f1, checked_i_lst_1, "1",2)

        for case1 in func1(min_f0, checked_i_lst_1, "0", 2):
            for case2 in func1(min_f1, checked_i_lst_1, "1", 2):
                yield "1:-" + str(i) + "-" + str(len(min_f0)) + " " + str(len(min_f1)) + "\n" + "\t" + case1 + "\n" + "\t" + case2
                #yield "======DEPTH=1========" + str(i) + "===" + str(len(min_f0)) + " " + str(len(min_f1)) + "\n" + case1 + "\n" + case2
                #cases.append("======DEPTH=1========" + str(i) + "===" + str(len(min_f0)) + " " + str(len(min_f1)) + "\n" + case1 + "\n" + case2)
    #return cases
    #with open("trees.txt", "w") as f:
    # i = 0
    # for case in cases:
    #     with open("trees/tree_"+str(i)+".txt", "w") as f:
    #         print(case)
    #         f.write(case)
    #         #break
    #     i += 1

#deep_in_functions_full(functions, 2, [], [], [], 0)
#new_deep_functions(functions)
#cases = very_new_deep_functions(functions)
with Profiler() as pr:
    i = 0
    threshold = int(2)
    for case in very_new_deep_functions(functions):
        #print(case)
        #print(i)
        count = 0
        bad_count = 0
        for line in case.split("\n"):
            line = line.strip()
            if line[:line.find(":")] == "7":
                count += 1
                lst = line.split("-")[-1].split(" ")
                value1 = int(lst[0])
                value2 = int(lst[1])
                #print(value1, value2, threshold)
                if value1 < threshold and value2 < threshold:
                    bad_count += 1
        if count != 0 and bad_count >= count:
            print("BADTREE======")
            print(case)
        #with open("D:/Programming/voronenko/trees/tree_"+str(i)+".txt", "w") as f:
            #print(case)
            #f.write(case)
            #break
        #print(case)
        i += 1
    print(i)

#print(recursive_deep_functions(functions, [], 0, []))

# with open('forest.txt', 'w') as f:
#     for tree in forest:
#         for i in range(16):
#             f.write(str(i) + ': ' + '\t'.join(tree[i]) + '\n')
#         f.write("========================================\n")

# with open('list.txt', 'w') as f:
#     f.write('\n'.join(all_nodes))