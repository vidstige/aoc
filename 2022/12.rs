use std::cmp::Ordering;
use std::io::{self, BufRead};
use std::collections::{BinaryHeap, HashMap};

type Position = (i32, i32);
type Height = i32;
type Grid = HashMap<Position, Height>;

fn parse() -> (Grid, Position, Position) {
    let alphabet = "abcdefghijklmnopqrstuvwxyz";
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    let mut grid = HashMap::new();
    
    let mut start = Option::None;
    let mut end = Option::None;
    for (y, line) in lines.enumerate() {
        for (x, c) in line.chars().enumerate() {
            let p = (x as i32, y as i32);
            if c == 'S' {
                start = Some(p);
                grid.insert(p, alphabet.find('a').unwrap() as i32);
            } else if c == 'E' {
                end = Some(p);
                grid.insert(p, alphabet.find('z').unwrap() as i32);
            } else {
                let height = alphabet.find(c).unwrap() as i32;
                grid.insert(p, height);
            }
        }
    }
    (grid, start.unwrap(), end.unwrap())
}

fn neighbors(grid: &Grid, p: &Position) -> Vec<Position> {
    let deltas = Vec::from([(-1, 0), (1, 0), (0, -1), (0, 1)]);
    let mut neighbors = Vec::new();
    let (x, y) = p;
    for (dx, dy) in deltas {
        let n = (x + dx, y + dy);
        if grid.contains_key(&n) {
            neighbors.push(n);
        }
    }
    return neighbors;
}

// Use struct over tuple to allow impl of traits needed for BinaryHeap
#[derive(Copy, Clone, Eq, PartialEq)]
struct Node {
    position: Position,
    cost: usize,
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        // Notice that the we flip the ordering on costs.
        // In case of a tie we compare positions - this step is necessary
        // to make implementations of `PartialEq` and `Ord` consistent.
        other.cost.cmp(&self.cost).then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn dijkstra(grid: &Grid, start: Position, end: Position) -> Option<usize> {
    let mut heap = BinaryHeap::new();
    let mut costs: HashMap<Position, usize> = HashMap::new();

    costs.insert(start, 0);
    heap.push(Node { position: start, cost: 0 });
    while let Some(Node { position, cost }) = heap.pop() {
        if position == end {
            return Some(cost);
        }
        println!("{:?} {}", position, cost);
        
        // skip if we already found something better
        if cost > *costs.get(&position).unwrap_or(&usize::MAX) { continue; }

        let height = grid.get(&position).unwrap();
        for neighbor in &neighbors(grid, &position) {
            let neighbor_height = grid.get(neighbor).unwrap();
            if neighbor_height - height > 1 {
                continue;
            }
            let next = Node { position: *neighbor, cost: cost + 1 };

            if next.cost < *costs.get(&next.position).unwrap_or(&usize::MAX) {
                heap.push(next);
                costs.insert(next.position, next.cost);
            }
        }
    }
    None
}

fn main() {
    let (grid, start, goal) = parse();
    if let Some(steps) = dijkstra(&grid, start, goal) {
        println!("{}", steps);
    } else {
        println!("No path from {:?} to {:?}", start, goal);
    }
}
