import sys

def write_air_file(active1, passive1, active2, passive2, segid1='A', segid2='B', output_file = "air.tbl"):

    sys.stdout = open(output_file, "w")

    active1 = [int(x) for x in active1]
    passive1 = [int(x) for x in passive1]
    active2 = [int(x) for x in active2]
    passive2 = [int(x) for x in passive2]

    all1 = active1 + passive1
    all2 = active2 + passive2

    for resi1 in active1:
        print('assign (resi {:d} and segid {:s})'.format(resi1, segid1))
        print('(')
        c = 0
        for resi2 in all2:
            print('       (resi {:d} and segid {:s})'.format(resi2, segid2))
            c += 1
            if c != len(all2):
                print('        or')

        print(') 2.0 2.0 0.0\n')
            
    for resi2 in active2:
        print('assign (resi {:d} and segid {:s})'.format(resi2, segid2))
        print('(\n')
        c = 0
        for resi1 in all1:
            print('       (resi {:d} and segid {:s})'.format(resi1, segid1))
            c += 1
            if c != len(all1):
                print('        or\n')

        print(') 2.0 2.0 0.0\n')
    
    sys.stdout.close()
