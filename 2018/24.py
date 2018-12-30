import re

def load(filename):
    teams = []
    with open(filename) as f:
        while True:
            team = f.readline()
            if not team:
                break
            line1 = f.readline().rstrip()
            match = re.match('(\d+) units each with (\d+) hit points \(.*\) ', line1)
            #17 units each with 5390 hit points (weak to radiation, bludgeoning) with
            #an attack that does 4507 fire damage at initiative 2
            line2 = f.readline().rstrip()
            f.readline()  # blank
            teams.append(team)
    return teams                


teams = load('input/24ex')
print(teams)
