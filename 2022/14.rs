use std::hash::Hash;
use std::io::{self, BufRead};
use std::collections::HashSet;
use std::ops::RangeInclusive;
use std::str::FromStr;

#[derive(PartialEq, Eq, Hash, Clone, Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl FromStr for Point {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut parts = s.split(",");
        let x = parts.next().unwrap().parse().unwrap();
        let y = parts.next().unwrap().parse().unwrap();
        Ok(Point {x, y})
    }
}

fn parse_polygon(s: &str) -> Vec<Point> {
    s.split(" -> ").into_iter().map(|p| p.parse().unwrap()).collect()
}

fn forward<T>(a: T, b: T) -> RangeInclusive<T> where T: Ord+Copy {
    let lo = a.min(b);
    let hi = a.max(b);
    lo..=hi
}

fn line(a: &Point, b: &Point) -> Vec<Point> {
    if a.x == b.x {
        // vertical
        return forward(a.y, b.y).map(|y| Point{x: a.x, y: y}).collect();
    }
    if a.y == a.y {
        // horizontal
        return forward(a.x, b.x).map(|x| Point{x: x, y: a.y}).collect();
    }
    panic!("Diagonal line");
}

fn fill(grid: &mut HashSet<Point>, polygons: &Vec<Vec<Point>>) {
    for polygon in polygons {
        for (a, b) in polygon.iter().zip(polygon.iter().skip(1)) {
            for p in line(a, b) {
                grid.insert(p);
            }
        }
    }
}

fn drop(grid: &HashSet<Point>, spawn: &Point, floor: i32) -> Option<Point> {
    let mut p = spawn.clone();
    while p.y <= floor {
        let candidates = [Point{x: p.x, y: p.y + 1}, Point{x: p.x - 1, y: p.y + 1}, Point{x: p.x + 1, y: p.y + 1}];
        if let Some(next) = candidates.iter().find(|c| !(grid.contains(c) || c.y == floor)) {
            p = next.clone();
        } else {
            return Some(p);
        }
    }
    None
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    let polygons: Vec<_> = lines.map(|line| parse_polygon(&line)).collect();
    let spawn = Point{x: 500, y: 0};
    
    let mut grid = HashSet::new();
    fill(&mut grid, &polygons);
    let bottom = grid.iter().map(|p| p.y).max().unwrap();
    let floor = bottom + 2;

    let mut counter = 0;
    while let Some(rest) = drop(&grid, &spawn, floor) {
        counter += 1;
        if rest == spawn {
            break;
        }
        grid.insert(rest);
    }
    println!("{}", counter);
}
