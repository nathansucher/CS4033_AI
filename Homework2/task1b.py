# CHECK + THE = TIRES

import constraint
import time


def equation(c, t, h, e, k, i, r, s):
    if (c*10000 + h*1000 + e*100 + c*10 + k) + (t*100 + h*10 + e) == (t*10000 + i*1000 + r*100 + e*10 + s):
        return True


if __name__ == "__main__":
    start = time.time()

    problem = constraint.Problem()

    problem.addVariables("CT", range(1, 10))
    problem.addVariables("HEKIRS", range(10))

    problem.addConstraint(equation, "CTHEKIRS")
    problem.addConstraint(constraint.AllDifferentConstraint())

    solutions = problem.getSolutions()

    stop = time.time()
    print("Program took " + "{:.2f}".format(stop - start) + " seconds to find solution(s).")

    print("\nNumber of Solutions: ", len(solutions))

    for solution in solutions:
        print("\nC: ", solution['C'])
        print("\nT: ", solution['T'])
        print("\nH: ", solution['H'])
        print("\nE: ", solution['E'])
        print("\nK: ", solution['K'])
        print("\nI: ", solution['I'])
        print("\nR: ", solution['R'])
        print("\nS: ", solution['S'])
