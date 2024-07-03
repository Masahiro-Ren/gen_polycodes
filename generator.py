import sys
import argparse
import math

TabTab = "\t\t"

def load_template(path):
    with open(path, mode="r") as f:
        code = f.readlines()
    return code

## Generating loop body in x direction
def gen_x_loopbody(template_code, loopbody_line, Np, division):
    loop_body = ""
    if(division == 0):
        loop_body += TabTab + "q_tmp(i,j,k) = filterMat(i,1) * q_in(1,j,k) + &\n"
        for j in range(2, Np):
            loop_body += TabTab + "filterMat(i,{0}) * q_in({0},j,k) + &\n".format(j)
        loop_body += TabTab + "filterMat(i,{0}) * q_in({0},j,k)\n".format(Np)
    else:
        len_per_block = math.ceil(Np / division)
        np = Np
        var_idx = 1
        idx = 1
        while np > 0 :
            muladd_len = min(np, len_per_block)
            loop_body += TabTab + "tmp{0} = ".format(var_idx) 
            for j in range(0, muladd_len):
                loop_body += "filterMat(i,{0}) * q_in({0},j,k) + ".format(idx)
                idx += 1
            loop_body = loop_body[:-2] + "\n" 

            np -= len_per_block
            var_idx += 1
        ## q_tmp(i,j,k) = tmp1 + tmp2 + ......
        loop_body += TabTab + "q_tmp(i,j,k) = "
        for tmp_var in range(1, division + 1):
            loop_body += "tmp{0} + ".format(tmp_var)
        loop_body = loop_body[:-2] + "\n"

    template_code[loopbody_line] = loop_body

## Generating loop body in y direction
def gen_y_loopbody(template_code, loopbody_line, Np, division):
    loop_body = ""
    if(division == 0):
        loop_body += TabTab + "q_in(i,j,k) = q_tmp(i,1,k) * filterMat_tr(1,j) + &\n"
        for j in range(2, Np):
            loop_body += TabTab + "q_tmp(i,{0},k) * filterMat_tr({0},j) + &\n".format(j)
        loop_body += TabTab + "q_tmp(i,{0},k) * filterMat_tr({0},j)\n".format(Np)
    else:
        len_per_block = math.ceil(Np / division)
        np = Np
        var_idx = 1
        idx = 1
        while np > 0 :
            muladd_len = min(np, len_per_block)
            loop_body += TabTab + "tmp{0} = ".format(var_idx) 
            for j in range(0, muladd_len):
                loop_body += "q_tmp(i,{0},k) * filterMat_tr({0},j) + ".format(idx)
                idx += 1
            loop_body = loop_body[:-2] + "\n" 

            np -= len_per_block
            var_idx += 1
        ## q_in(i,j,k) = tmp1 + tmp2 + ......
        loop_body += TabTab + "q_in(i,j,k) = "
        for tmp_var in range(1, division + 1):
            loop_body += "tmp{0} + ".format(tmp_var)
        loop_body = loop_body[:-2] + "\n"

    template_code[loopbody_line] = loop_body

## Generating loop body in z direction
def gen_z_loopbody(template_code, loopbody_line, Np, division):
    loop_body = ""
    if(division == 0):
        loop_body += TabTab + "q_tmp(i,j,k) = q_in(i,j,1) * filterMat_vtr(1,k) + &\n"
        for j in range(2, Np):
            loop_body += TabTab + "q_in(i,j,{0}) * filterMat_vtr({0},k) + &\n".format(j)
        loop_body += TabTab + "q_in(i,j,{0}) * filterMat_vtr({0},k)\n".format(Np)
    else:
        len_per_block = math.ceil(Np / division)
        np = Np
        var_idx = 1
        idx = 1
        while np > 0 :
            muladd_len = min(np, len_per_block)
            loop_body += TabTab + "tmp{0} = ".format(var_idx) 
            for j in range(0, muladd_len):
                loop_body += "q_in(i,j,{0}) * filterMat_vtr({0},k) + ".format(idx)
                idx += 1
            loop_body = loop_body[:-2] + "\n" 

            np -= len_per_block
            var_idx += 1
        ## q_tmp(i,j,k) = tmp1 + tmp2 + ......
        loop_body += TabTab + "q_tmp(i,j,k) = "
        for tmp_var in range(1, division + 1):
            loop_body += "tmp{0} + ".format(tmp_var)
        loop_body = loop_body[:-2] + "\n"

    template_code[loopbody_line] = loop_body

def gen_tmp_var(template_code, tmp_var_line, division):
    if(division == 0):
        return
    code_line = TabTab + "real(RP) :: "
    for var_num in range(1, division + 1):
        code_line += "tmp{0}, ".format(var_num)
    code_line = code_line[:-2] + "\n"
    template_code[tmp_var_line] = code_line


def gen_modalfilter(poly_order, division):
    Np = poly_order + 1
    path = "./templates/modalfilter_template.F90"
    template_code = load_template(path)
    line_tmp_var = -1
    line_loopbody_x = -1
    line_loopbody_y = -1
    line_loopbody_z = -1
    ## Assign Np
    for i, code_line in enumerate(template_code):
        if("dof" in code_line):
            template_code[i] = code_line.replace("dof", "{0}".format(Np))
        if("!CODEGEN TEMP_VAR" in code_line):
            line_tmp_var = i
        if("!LOOPBODY X" in code_line):
            line_loopbody_x = i
        if("!LOOPBODY Y" in code_line):
            line_loopbody_y = i
        if("!LOOPBODY Z" in code_line):
            line_loopbody_z = i
    ## Gen tmp vars
    gen_tmp_var(template_code, line_tmp_var, division)
    ## Gen x loop body
    gen_x_loopbody(template_code, line_loopbody_x, Np, division) 
    ## Gen y loop body
    gen_y_loopbody(template_code, line_loopbody_y, Np, division) 
    ## Gen z loop body
    gen_z_loopbody(template_code, line_loopbody_z, Np, division) 

    return template_code
            

def gen_matrixvector(polyorder):
    Np = polyorder + 1
    path = "./template/matrixvector_template.F90"
    template_code = load_template(path)
    # To be continued

def main():
    parser = argparse.ArgumentParser(description="Input File name and PolyOrder")
    parser.add_argument("-t", "--target", type=str)
    parser.add_argument("-p", "--polyorder", type=int)
    parser.add_argument("-d", "--division", type=int)

    args = parser.parse_args()

    poly_order = args.polyorder
    target = args.target
    division = args.division

    if(poly_order < 3):
        print("This program doesn't support polyorder less than 3.")
        exit(1)

    if(division > poly_order + 1):
        print("Wrong division number.")
        exit(1)

    if(target == "modalfilter"): 
        code = gen_modalfilter(poly_order, division)
        with open("modalfilter.F90", mode="w") as f:
            f.writelines(code)
    if(target == "matrixvector"):
        gen_matrixvector(poly_order)

if __name__ == "__main__":
    main()
