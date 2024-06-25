import sys
import argparse

def load_template(path):
    with open(path, mode="r") as f:
        code = f.readlines()
    return code

def gen_modalfilter(poly_order):
    DoF = poly_order + 1
    path = "./template/modalfilter_template.F90"
    template_code = load_template(path)
    start_line = 0
    end_line = 0
    ## Generating loop in x direction
    for i, code_line in enumerate(template_code):
        if("!CODEGEN X" in code_line):
            start_line = i
        if("!CODEGEN X END" in code_line):
            end_line = i
    for i, code_line in enumerate(template_code[start_line, end_line]):
        if("!<DOF>" in code_line):
            code_line = code_line.replace("!<DOF>", "{0}".format(DoF))
        if("!CODEGEN LOOP_BODY" in code_line):
            loop_body = "q_tmp(i,j,k) = filterMat(i,1) * q_in(1,j,k) + &\n"
            for j in range(2, DoF):
                loop_body += "filterMat(i,{0}) * q_in({0},j,k) + &\n".format(j)
            

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
        gen_modalfilter(poly_order)
    if(target == "matrixvector"):
        gen_matrixvector(poly_order)

if __name__ == "__main__":
    main()
