file = open('day17_testinput.txt', 'r')
line = [s.strip('\n') for s in file.readlines()][0]
print(len(line))


shapes = [
    [(0,0), (1,0), (2,0), (3,0)], # -
    [(1,0), (0,1), (1,1), (2,1), (1,2)], # +
    [(2,0), (2,1), (0,2), (1,2), (2,2)], # reverse L
    [(0,0), (0,1), (0,2), (0, 3)], # l
    [(0,0), (1,0), (0,1), (1, 1)], # square
]