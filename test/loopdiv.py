import math
import numpy as np

TabTab = "\t\t"

def divide_sum(S, N):
    base = int(S / N)
    remainder = S % N
    results = np.full(N, base)
    for i in range(remainder):
        results[i] += 1

    return results    

# print(divde_sum(4, 3))

# parts = divde_sum(4,3)

# print(parts.sum())

# for Np in range(4, 13):
#     for divnum in range(1, Np+1):
#         parts = divde_sum(Np, divnum)
#         if(parts.size != divnum or parts.sum() != Np):
#             print("Not pass in Np = {0}, Div = {1}".format(Np, divnum))

# print("Done")

# sum = 1

# for Np in range(4, 13):
#     sum += Np

# print(sum)

def gen_x_loopbody(Np, division):
    loop_body = ""
    if(division == 0):
        loop_body += TabTab + "q_tmp(i,j,k) = filterMat(i,1) * q_in(1,j,k) + &\n"
        for j in range(2, Np):
            loop_body += TabTab + "filterMat(i,{0}) * q_in({0},j,k) + &\n".format(j)
        loop_body += TabTab + "filterMat(i,{0}) * q_in({0},j,k)\n".format(Np)
    else:

        div_nums = divide_sum(Np, division)

        var_idx = 1
        idx = 1

        for i in range(div_nums.size):
            loop_body += TabTab + "tmp{0} = ".format(var_idx) 
            for j in range(div_nums[i]):
                loop_body += "filterMat(i,{0}) * q_in({0},j,k) + ".format(idx)
                idx += 1
            loop_body = loop_body[:-2] + "\n" 
            var_idx += 1

        ## q_tmp(i,j,k) = tmp1 + tmp2 + ......
        loop_body += TabTab + "q_tmp(i,j,k) = "
        for tmp_var in range(1, division + 1):
            loop_body += "tmp{0} + ".format(tmp_var)
        loop_body = loop_body[:-2] + "\n"

        print(loop_body)

gen_x_loopbody(5,4)