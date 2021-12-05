use std::io::{self, BufRead};
use std::str::FromStr;
use std::collections::HashMap;
use std::cmp;

#[derive(Hash, PartialEq, Eq, Debug)]
struct Point {
    x: i32,
    y: i32,
}

impl FromStr for Point {
    type Err = ();
    fn from_str(s: &str) -> Result<Point, ()> {
        let mut parts = s.split(",");
        let x = parts.next().unwrap().parse().unwrap();
        let y = parts.next().unwrap().parse().unwrap();
        Ok(Point { x: x, y: y })
    }
}

struct Vent {
    from: Point,
    to: Point,    
}

impl FromStr for Vent {
    type Err = ();
    fn from_str(s: &str) -> Result<Vent, ()> {
        let mut parts = s.split(" -> ");
        let from = parts.next().unwrap().parse().unwrap();
        let to = parts.next().unwrap().parse().unwrap();
        Ok(Vent { from: from, to: to })
    }
}
impl Vent {
    fn is_vertical(&self) -> bool { self.from.x == self.to.x }
    fn is_horizontal(&self) -> bool { self.from.y == self.to.y }
}

fn main() {
    let stdin = io::stdin();
    let vents: Vec<Vent> = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap())
        .map(|line| line.parse().unwrap())
        .collect();

    let mut intersections: HashMap<Point, i32> = HashMap::new();
    for vent in vents {
        if vent.is_vertical() {
            let x = vent.from.x;
            let ymin = cmp::min(vent.from.y, vent.to.y);
            let ymax = cmp::max(vent.from.y, vent.to.y) + 1;
            for y in ymin..ymax {
                let p = Point{x, y};
                *intersections.entry(p).or_insert(0) += 1;
            }
        } else if vent.is_horizontal() {
            let y = vent.from.y;
            let xmin = cmp::min(vent.from.x, vent.to.x);
            let xmax = cmp::max(vent.from.x, vent.to.x) + 1;
            for x in xmin..xmax {
                let p = Point{x, y};
                *intersections.entry(p).or_insert(0) += 1;
            }
        } else {
            // diagonal
            let n = (vent.from.x - vent.to.x).abs();
            let dx = (vent.to.x - vent.from.x) / n;
            let dy = (vent.to.y - vent.from.y) / n;
            for i in 0..(n + 1) {
                let x = vent.from.x + dx * i;
                let y = vent.from.y + dy * i;
                let p = Point{x, y};
                *intersections.entry(p).or_insert(0) += 1;
            }
        }
    }

    let dangerous = intersections.values().filter(|count| **count > 1).count();
    println!("{}", dangerous);
}