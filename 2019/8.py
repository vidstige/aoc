def load():
    with open('input/8') as f:
        return f.read()
    

def gray(color):
    if color == '0':
        return 0
    if color == '1':
        return 255

def render_layer(target, source):
    return bytes([a if b == '2' else gray(b) for a, b in zip(target, source)])

class Image:
    def __init__(self, raw, size):
        self.raw = raw
        self.size = size

    def layer_size(self):
        w, h = self.size
        return w * h

    def layers(self):
        layer_size = self.layer_size()
        index = 0
        while index < len(self.raw):
            yield self.raw[index:index + layer_size]
            index += layer_size

    def flat(self):
        layers = list(self.layers())
        acc = bytes(self.layer_size())
        for layer in reversed(layers):
            acc = render_layer(acc, layer)
        return acc

def count(layer, color):
    return len([c for c in layer if c == color])

def count_zeroes(layer):
    return count(layer, '0')

raw = load()
im = Image(raw, size=(25, 6))
layer = min(im.layers(), key=count_zeroes)
print(layer)
print(count(layer, '1') * count(layer, '2'))
    
with open('8.raw', 'wb') as f:
    f.write(im.flat())

# convert -size 25x6 -depth 8 gray:8.raw image.png