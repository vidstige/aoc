use std::io::{self, BufRead};
use std::collections::{HashMap, VecDeque};

fn parse(stdin: std::io::Stdin) -> HashMap<(i32, i32), u32> {
    let lines = stdin.lock()
        .lines()
        .map(|line| line.unwrap());

    let mut map = HashMap::new();
    for (y, line) in lines.enumerate() {
        for (x, c) in line.chars().enumerate() {
            map.insert((x as i32, y as i32), c.to_digit(10).unwrap());
        }
    }
    map
}

fn start(map: &HashMap<(i32, i32), u32>) -> (i32, i32) {
    (
        *map.keys().map(|(x, _)| x).min().unwrap(),
        *map.keys().map(|(_, y)| y).min().unwrap()
    )
}

fn end(map: &HashMap<(i32, i32), u32>) -> (i32, i32) {
    (
        *map.keys().map(|(x, _)| x).max().unwrap(),
        *map.keys().map(|(_, y)| y).max().unwrap()
    )
}

fn neigbours((x, y): (i32, i32)) -> Vec<(i32, i32)> {
    let mut tmp = Vec::new();
    tmp.push((x + 1, y));
    tmp.push((x - 1, y));
    tmp.push((x, y + 1));
    tmp.push((x, y - 1));
    tmp
}

fn search(map: &HashMap<(i32, i32), u32>, from: (i32, i32), to: (i32, i32)) -> u32 {
    let mut queue = VecDeque::new();
    let mut best = HashMap::new();
    queue.push_back((to, *map.get(&to).unwrap()));
    while let Some((p, cost)) = queue.pop_front() {
        for n in neigbours(p) {
            if let Some(risk) = map.get(&n) {
                if cost + risk < *best.get(&n).unwrap_or(&u32::MAX) {
                    best.insert(n, cost + risk);
                    queue.push_back((n, cost + risk));
                }
            }
        }
    }
    best.get(&from).unwrap() - map.get(&from).unwrap()
}

fn main() {
    let stdin = io::stdin();
    let map = parse(stdin);
    let best = search(&map, start(&map), end(&map));
    println!("{:?}", best);
}