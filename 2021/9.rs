use std::io::{self, BufRead};
use std::ops::Range;
use std::collections::{HashMap, HashSet};

fn xrange(heightmap: &HashMap<(i32, i32), u32>) -> Range<i32> {
    let xmin = heightmap.keys().map(|(x, _)| *x).min().unwrap();
    let xmax = heightmap.keys().map(|(x, _)| *x).max().unwrap();
    xmin..xmax + 1
}

fn yrange(heightmap: &HashMap<(i32, i32), u32>) -> Range<i32> {
    let ymin = heightmap.keys().map(|(_, y)| *y).min().unwrap();
    let ymax = heightmap.keys().map(|(_, y)| *y).max().unwrap();
    ymin..ymax + 1
}

fn neighbours(heightmap: &HashMap<(i32, i32), u32>, p: (i32, i32)) -> HashMap<(i32, i32), u32> {
    let deltas: [(i32, i32); 4] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ];
    let mut tmp = HashMap::new();
    let (x, y) = p;
    for (dx, dy) in deltas {
        let point = (x + dx, y + dy);
        match heightmap.get(&point) {
            Some(height) => { tmp.insert(point, *height); },
            None => (),
        }
    }
    return tmp;
}

fn basin(heightmap: &HashMap<(i32, i32), u32>, point: (i32, i32)) -> usize {
    let mut visited = HashSet::new();
    let mut stack = vec![point];
    while !stack.is_empty() {
        let p = stack.pop().unwrap();
        visited.insert(p);
        for (n, height) in neighbours(heightmap, p).iter() {
            if visited.contains(n) {
                continue;
            }
            if height < &9 {
                stack.push(*n);
            }
        }
    }
    visited.len()
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap());

    // parse
    let mut heightmap = HashMap::new();
    for (y, line) in lines.enumerate() {
        for (x, c) in line.chars().enumerate() {
            heightmap.insert((x as i32, y as i32), c.to_digit(10).unwrap());
        }
    }

    // find low points
    let mut sum = 0;
    let mut basins = Vec::new();
    for y in yrange(&heightmap) {
        for x in xrange(&heightmap) {
            let p = (x, y);
            if let Some(height) = heightmap.get(&p) {
                if neighbours(&heightmap, p).values().all(|h| height < h) {
                    basins.push(basin(&heightmap, p));
                    let risk = height + 1;
                    sum += risk;
                }
            }

        }
    }
    println!("risk {}", sum);
    basins.sort();
    basins.reverse();
    let top3: usize = basins.iter().take(3).product();
    println!("{}", top3);
}