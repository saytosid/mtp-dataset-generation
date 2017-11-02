from Stress import *
import sys

if __name__ == '__main__':
    load_id = sys.argv[1]
    intensity = sys.argv[2]
    if load_id<2 or load_id>9 :
        print "load_id must be between 2-9"
    if intensity<1 or intensity>5 :
        print "intensity must be between 1-5"

    loads[load_id-1].doStress(intensity)