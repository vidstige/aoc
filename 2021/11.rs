use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet};

type Point = (i32, i32);

fn neighbours(p: &Point) -> Vec<(i32, i32)> {
    let deltas = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (-1, 0),
        (1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
    ];
    let (x, y) = p;
    let mut n = Vec::new();
    for (dx, dy) in deltas {
        n.push((x + dx, y + dy));
    }
    n
} 

fn step(cave: &mut HashMap<Point, u32>) -> usize {
    // 1. Increase all octopussies
    for (_, v) in &mut cave.iter_mut() {
        *v += 1;
    }

    // 2. keep flashing until stable
    let mut flashed = HashSet::new();
    while {
        let before = flashed.len();
        for p in cave.clone().keys() {
            if cave[p] > 9 && !flashed.contains(p) {
                flashed.insert(*p);
                for n in neighbours(p) {
                    if let Some(v) = cave.get_mut(&n) {
                        *v += 1;
                    }
                }
            }
        }
        flashed.len() > before
    } {}

    // 3. reset flashed to zero
    for f in flashed.iter() {
        *cave.get_mut(&f).unwrap() = 0;
    }

    flashed.len()
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap());

    let mut cave = HashMap::new();
    for (y, line) in lines.enumerate() {
        for (x, c) in line.chars().enumerate() {
            let p = (x as i32, y as i32);
            cave.insert(p, c.to_digit(10).unwrap());
        }
    }

    /*let mut sum = 0;
    for _ in 0..100 {
        sum += step(&mut cave);
    }
    println!("{}", sum);*/

    let mut i = 0;
    loop {
        i += 1;
        let n = step(&mut cave);
        if n == cave.len() {
            println!("sync!");
            break;
        }
    }
    println!("{}", i);
}