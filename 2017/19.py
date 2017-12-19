ex = """     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+"""
    
def inside(x, y, maze):
    if y < 0 or y >= len(maze):
        return False
    return x >= 0 and x < len(maze[y])

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def solve(maze):
    x, y = maze[0].index('|'), 0
    dx, dy = 0, 1

    while inside(x, y, maze) and maze[y][x] != ' ':
        c = maze[y][x]
        if c == '+':
            for cx, cy in [dir for dir in DIRECTIONS if dir != (-dx, -dy)]:
                if inside(x + cx, y + cy, maze) and maze[y + cy][x + cx] != ' ':
                    dx, dy = cx, cy

        yield c

        x += dx
        y += dy


def count(sequence):
    return sum(1 for _ in sequence)

def main():
    print(count(solve(ex.splitlines())))

    with open('input/19') as f:
        maze = f.read().splitlines()
    
    print(count(solve(maze)))

main()
