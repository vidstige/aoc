import sys
from typing import List

class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


class Directory:
    def __init__(self, name: str, childs=[]):
        self.name = name
        self.childs = childs

    def __repr__(self) -> str:
        return 'Directory({})'.format(self.name)

    def cd(self, name: str):
        return next(child for child in self.childs if child.name == name)

    def files(self) -> List[File]:
        return [child for child in self.childs if isinstance(child, File)]

    def directories(self) -> List:
        return [child for child in self.childs if isinstance(child, Directory) and child.name != '..']


def sizes(node):
    assert isinstance(node, Directory)
    size = sum(f.size for f in node.files())
    for directory in node.directories():
        for d, s in sizes(directory):
            if d == directory:
                size += s
            yield d, s

    yield node, size


def parse(lines):
    root = Directory('/', [])
    cwd = root
    for line in lines:
        parts = line.rstrip().split()
        if parts[0] == "$":
            cmd = parts[1]
            if cmd == "cd":
                directory_name = parts[2]
                if directory_name == '/':
                    assert root == cwd
                else:
                    cwd = cwd.cd(directory_name)
        else:
            name = parts[1]
            if parts[0] == "dir":
                parent = Directory('..', childs=cwd.childs)
                node = Directory(name, childs=[parent])
            else:
                size = int(parts[0])
                node = File(name, size=size)
            cwd.childs.append(node)
    return root

root = parse(sys.stdin)

print(sum(s for d, s in sizes(root) if s <= 100000))
