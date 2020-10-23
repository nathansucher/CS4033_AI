# SINCE + JULIUS = CAESAR

import constraint
import time


def equation(s, j, c, i, n, e, u, l, a, r):
    if (s*10000 + i*1000 + n*100 + c*10 + e) + (j*100000 + u*10000 + l*1000 + i*100 + u*10 + s) == (c*100000 + a*10000 + e*1000 + s*100 + a*10 + r):
        return True


if __name__ == "__main__":
    start = time.time()

    problem = constraint.Problem()

    problem.addVariables("SJC", range(1, 10))
    problem.addVariables("INEULAR", range(10))

    problem.addConstraint(equation, "SJCINEULAR")
    problem.addConstraint(constraint.AllDifferentConstraint())

    solutions = problem.getSolutions()

    stop = time.time()
    print("Program took " + "{:.2f}".format(stop - start) + " seconds to find solution(s).")

    print("\nNumber of Solutions: ", len(solutions))

    for solution in solutions:
        print("\nS: ", solution['S'])
        print("\nJ: ", solution['J'])
        print("\nC: ", solution['C'])
        print("\nI: ", solution['I'])
        print("\nN: ", solution['N'])
        print("\nE: ", solution['E'])
        print("\nU: ", solution['U'])
        print("\nL: ", solution['L'])
        print("\nA: ", solution['A'])
        print("\nR: ", solution['R'])