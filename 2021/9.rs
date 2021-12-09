use std::io::{self, BufRead};
use std::ops::Range;
use std::collections::HashMap;

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

fn neighbours(heightmap: &HashMap<(i32, i32), u32>, p: (i32, i32)) -> Vec<u32> {
    let deltas: [(i32, i32); 4] = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1),
    ];
    let mut tmp = Vec::new();
    let (x, y) = p;
    for (dx, dy) in deltas {
        let point = (x + dx, y + dy);
        match heightmap.get(&point) {
            Some(height) => tmp.push(*height),
            None => (),
        }
    }
    return tmp;
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
    for y in yrange(&heightmap) {
        for x in xrange(&heightmap) {
            let p = (x, y);
            if let Some(height) = heightmap.get(&p) {
                let heights = neighbours(&heightmap, p);
                if heights.iter().all(|h| height < h) {
                    let risk = height + 1;
                    sum += risk;
                }
            }

        }
    }   
    println!("{}", sum);
}