use std::io::{self, BufRead};
use std::collections::HashSet;

fn parse(line: String) -> (i32, i32, i32) {
    let chars: Vec<_> = line.chars().collect();
    let mut i = 0;
    let mut x = 0;
    let mut y = 0;
    let mut z = 0;
    while i < chars.len() {
        let (di, (dx, dy, dz)) = match chars[i] {
            's' => match chars[i + 1] {
                'e' => (2, (0, -1, 1)),
                'w' => (2, (-1, 0, 1)),
                _ => (1, (0, 0, 0))
            },
            'n' => match chars[i + 1] {
                'e' => (2, (1, 0, -1)),
                'w' => (2, (0, 1, -1)),
                _ => (1, (0, 0, 0))
            },
            'e' => (1, (1, -1, 0)),
            'w' => (1, (-1, 1, 0)),
            _ => (1, (0, 0, 0))
        };
        i += di;
        x += dx; 
        y += dy;
        z += dz;
    }
    assert!(x + y + z == 0);
    (x, y, z)
}

static NEIGHBOURS: &'static [(i32, i32, i32)] = &[
    (0, -1, 1),
    (-1, 0, 1),
    (1, 0, -1),
    (0, 1, -1),
    (1, -1, 0),
    (-1, 1, 0),
];

fn add((ax, ay, az): &(i32, i32, i32), (bx, by, bz): &(i32, i32, i32)) -> (i32, i32, i32) {
    (ax + bx, ay + by, az + bz)
}

fn step(black: &mut HashSet<(i32, i32, i32)>) {
    let mut everything = HashSet::new();
    // Find all tiles to consider
    for tile in black.iter() {
        everything.insert(*tile);
        for n in NEIGHBOURS {
            everything.insert(add(tile, n));
        }
    }
    // Find all to flip
    let mut flip = HashSet::new();
    for tile in everything.iter() {
        let mut count = 0;
        for n in NEIGHBOURS {
            if black.contains(&add(tile, n)) {
                count += 1;
            }
        }

        if black.contains(tile) {
            if count == 0 || count > 2 {
                flip.insert(*tile);
            }
        } else {
            if count == 2 {
                flip.insert(*tile) ;
            }
        }
    }
    for tile in flip.iter() {
        if black.contains(tile) {
            black.remove(tile);
        } else {
            black.insert(*tile);
        }
    }
}


fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut black = HashSet::new();
    for maybe_line in lines {
        let line = maybe_line.unwrap();
        let p = parse(line);
        if black.contains(&p) {
            black.remove(&p);
        } else {
            black.insert(p);
        }
    }
    for _ in 0..100 {
        step(&mut black);
    }
    println!("{}", black.len());
}