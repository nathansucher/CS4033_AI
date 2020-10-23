# DO + YOU + FEEL = LUCKY

import constraint
import time


def equation(d, y, f, l, o, u, e, c, k):
    if (d*10 + o) + (y*100 + o*10 + u) + (f*1000 + e*100 + e*10 + l) == (l*10000 + u*1000 + c*100 + k*10 + y):
        return True


if __name__ == "__main__":
    start = time.time()

    problem = constraint.Problem()

    problem.addVariables("DYFL", range(1, 10))
    problem.addVariables("OUECK", range(10))

    problem.addConstraint(equation, "DYFLOUECK")
    problem.addConstraint(constraint.AllDifferentConstraint())

    solutions = problem.getSolutions()

    stop = time.time()
    print("Program took " + "{:.2f}".format(stop - start) + " seconds to find solution(s).")

    print("\nNumber of Solutions: ", len(solutions))

    for solution in solutions:
        print("\nD: ", solution['D'])
        print("\nY: ", solution['Y'])
        print("\nF: ", solution['F'])
        print("\nL: ", solution['L'])
        print("\nO: ", solution['O'])
        print("\nU: ", solution['U'])
        print("\nE: ", solution['E'])
        print("\nC: ", solution['C'])
        print("\nK: ", solution['K'])

