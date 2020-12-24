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
    println!("{}", black.len());
}