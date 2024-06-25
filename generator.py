import sys
import argparse

def load_template(path):
    with open(path, mode="r") as f:
        code = f.readlines()
    return code

def gen_filter_loopbody(lhs, rhs, filtermat, DoF, division):
    loop_body = ""
    tabtab = '\t\t'
    if(division == 1):
        loop_body = tabtab + "{0}(i,j,k) = {1}(i,1) * {2}(1,j,k) + &\n".format(lhs, rhs, filtermat)
        for i in range(2,DoF):
            loop_body = tabtab + "{0}(i,{1}) * {2}({1},j,k) + &\n".format(filtermat, i, rhs)
        loop_body = tabtab + "{0}(i,{1}) * {2}({1},j,k) + &\n".format(filtermat, DoF, rhs)
    else:
        print("loop division dealing")
    
    return loop_body


def gen_modalfilter(poly_order):
    DoF = poly_order + 1
    path = "./templates/modalfilter_template.F90"
    template_code = load_template(path)
    start_line = 0
    end_line = 0
    ## Generating loop in x direction
    for i, code_line in enumerate(template_code):
        if("!CODEGEN X" in code_line):
            start_line = i
        if("!CODEGEN END X" in code_line):
            end_line = i
    for i, code_line in enumerate(template_code[start_line:end_line]):
        if("!<DOF>" in code_line):
            template_code[start_line + i] = code_line.replace("!<DOF>", "{0}".format(DoF))
        if("!CODEGEN LOOP_BODY" in code_line):
            loop_body = "\t\tq_tmp(i,j,k) = filterMat(i,1) * q_in(1,j,k) + &\n"
            for j in range(2, DoF):
                loop_body += "\t\tfilterMat(i,{0}) * q_in({0},j,k) + &\n".format(j)
            loop_body += "\t\tfilterMat(i,{0}) * q_in({0},j,k)\n".format(DoF)
            template_code[start_line + i] = loop_body
    
    ## Generating loop in y direction
    for i, code_line in enumerate(template_code):
        if("!CODEGEN Y" in code_line):
            start_line = i
        if("!CODEGEN END Y" in code_line):
            end_line = i
    for i, code_line in enumerate(template_code[start_line:end_line]):
        if("!<DOF>" in code_line):
            template_code[start_line + i] = code_line.replace("!<DOF>", "{0}".format(DoF))
        if("!CODEGEN LOOP_BODY" in code_line):
            loop_body = "\t\tq_in(i,j,k) = filterMat_tr(i,1) * q_tmp(1,j,k) + &\n"
            for j in range(2, DoF):
                loop_body += "\t\tfilterMat_tr(i,{0}) * q_tmp({0},j,k) + &\n".format(j)
            loop_body += "\t\tfilterMat_tr(i,{0}) * q_tmp({0},j,k)\n".format(DoF)
            template_code[start_line + i] = loop_body

    ## Generating loop in z direction
    for i, code_line in enumerate(template_code):
        if("!CODEGEN Z" in code_line):
            start_line = i
        if("!CODEGEN END Z" in code_line):
            end_line = i
    for i, code_line in enumerate(template_code[start_line:end_line]):
        if("!<DOF>" in code_line):
            template_code[start_line + i] = code_line.replace("!<DOF>", "{0}".format(DoF))
        if("!CODEGEN LOOP_BODY" in code_line):
            loop_body = "\t\tq_tmp(i,j,k) = filterMat_vtr(i,1) * q_in(1,j,k) + &\n"
            for j in range(2, DoF):
                loop_body += "\t\tfilterMat_vtr(i,{0}) * q_in({0},j,k) + &\n".format(j)
            loop_body += "\t\tfilterMat_vtr(i,{0}) * q_in({0},j,k)\n".format(DoF)
            template_code[start_line + i] = loop_body
    return template_code
            

def gen_matrixvector(polyorder):
    DoF = polyorder + 1
    path = "./template/matrixvector_template.F90"
    template_code = load_template(path)
    # To be continued

def main():
    parser = argparse.ArgumentParser(description="Input File name and PolyOrder")
    parser.add_argument("-p", "--polyorder", type=int)
    parser.add_argument("-t", "--target", type=str)

    args = parser.parse_args()

    poly_order = args.polyorder
    target = args.target

    if(poly_order < 3):
        print("This program doesn't support polyorder less than 3.")
        exit(1)

    if(target == "modalfilter"): 
        code = gen_modalfilter(poly_order)
        with open("modalfilter.F90", mode="w") as f:
            f.writelines(code)
    if(target == "matrixvector"):
        gen_matrixvector(poly_order)

if __name__ == "__main__":
    main()
