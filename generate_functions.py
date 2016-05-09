__author__ = 'malahova'

from pyeda.inter import exprvar, Variable, point2upoint, expr2truthtable
import itertools

# a, b, c, d = map(exprvar, "abcd")
# f0 = ~a & b | c & ~d
# print(f0)
# print(f0.restrict({a: 0}))

# x1, x2, x3, x4, x5 = map(exprvar, "x1 x2 x3 x4 x5".split())
# kardo_function = (x1 & x2 | ~x1 & ~x2) & (~x3 & x4 | x3 & ~x4) | (~x1 & x2 | x1 & ~x2) & (x3 & x4 | ~x3 & ~x4)
# print(kardo_function)
# print(kardo_function.compose({x1:~x2}))

#f = kardo_function.restrict({x1: 0})
#print(f)
#print(kardo_function.compose({x1: x3}))
#print(expr2truthtable(f))
#print(list(map(lambda x: x-1, list(expr2truthtable(f).pcdata))))

x4, x3, x2, notx1, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x1, notx4 = map(exprvar, "x4 x3 x2 notx1 x21 x22 notx21 notx22 x31 x32 notx31 notx32 x1 notx4".split())
all_vars = [x1, notx1, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x4, notx4]
#equals = [(x1,[x1, notx1]), (x2,[x21, x22, notx21, notx22]), (x3, [x31, x32, notx31, notx32]), (x4, [x4, notx4])]
equals = [(~x1, [notx1]), (x2,[x21, x22]), (~x2,[notx21, notx22]), (x3, [x31, x32]),
          (~x3, [notx31, notx32]), (~x4, [notx4])]
#f = x1 & notx21 & notx31 & notx4 | x1 & notx21 & x31 & x4 | x1 & x21 & notx32 & x4 | x1 & x21 & x32 & notx4 | notx1 & notx22 & notx32 & x4 | notx1 & notx22 & x32 & notx4 | notx1 & x22 & notx31 & notx4 | notx1 & x22 & x31 & x4

#print(set([(0,0,0),(0,0,1),(0,0,0)]))

inputs = [x1, x2, x3, x4]
kardo_functions = set()
count = 0
for vec in list(itertools.product(range(3), repeat=12))[::-1]:
    d = dict(zip(all_vars, vec))
    #print("==============================")
    #print(d)
    function = (x1 & notx21 & notx31 & notx4) | (x1 & notx21 & x31 & x4) | (x1 & x21 & notx32 & x4) | (x1 & x21 & x32 & notx4) | (notx1 & notx22 & notx32 & x4) | (notx1 & notx22 & x32 & notx4) | (notx1 & x22 & notx31 & notx4) | (notx1 & x22 & x31 & x4)
    restrict_dict = {key:value for key, value in d.items() if value in (0, 1)}
    #print(restrict_dict)
    function = function.restrict(restrict_dict)
    #print(function)
    for var, vars_lst in equals:
        for v in vars_lst:
            function = function.compose({v: var})
    #print(function)
    fictitious_vars = [v for v in inputs if v not in function.inputs]
    for v in fictitious_vars:
        function = function & (v | ~v)
    #print(function)
    #print(expr2truthtable(function))
    kardo_functions.add(str(tuple(map(lambda x: x-1, list(expr2truthtable(function).pcdata)))))
    count += 1
    print(count)
    #if count > 1000:
    #    break

with open("results.txt", "w") as f:
    f.write("\n".join(sorted(kardo_functions)))

print("# functions: ", len(kardo_functions))