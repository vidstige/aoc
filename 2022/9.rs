use std::{io::{self, BufRead}, str::FromStr};

struct Delta {
    dx: i32,
    dy: i32,
}
type Point = (i32, i32);
type Rope = Vec<Point>;

impl FromStr for Delta {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {    
        let mut parts = s.split(" ");
        let direction = parts.next().unwrap();
        let amount = parts.next().unwrap().parse().unwrap();
        match direction {
            "R" => Ok(Delta{dx: amount, dy: 0}),
            "L" => Ok(Delta{dx: -amount, dy: 0}),
            "D" => Ok(Delta{dx: 0, dy: amount}),
            "U" => Ok(Delta{dx: 0, dy: -amount}),
            _ => Err(())
        }
    }
}

impl Delta {
    fn signum(&self) -> Self {
        Self{dx: self.dx.signum(), dy: self.dy.signum()}
    }
}

fn move_point(p: &Point, m: &Delta) -> Point {
    let (x, y) = p;
    (x + m.dx, y + m.dy)
}

fn delta(a: Point, b: Point) -> Delta {
    let (ax, ay) = a;
    let (bx, by) = b;
    Delta { dx: bx - ax, dy: by - ay }
}

fn follow(tail: Point, head: Point) -> Point {
    let d = delta(tail, head);
    if d.dx.abs() <= 1 && d.dy.abs() <= 1 {
        return tail;
    }
    move_point(&tail, &Delta { dx: d.dx.signum(), dy: d.dy.signum() })
}

fn step(current: Rope, delta: Delta, n: i32, tail_path: &mut Vec<Point>) -> Rope {
    let mut rope = current.clone();
    for _ in 0..n {
        // head moves first
        rope[0] = move_point(&rope[0], &delta);

        // the rest follows the knot in front
        for i in 1..rope.len() {
            rope[i] = follow(rope[i], rope[i - 1]);
        }
        tail_path.push(*rope.last().unwrap());
    }
    rope
}

fn create_rope(n: usize) -> Rope {
    let mut rope = Vec::new();
    for _ in 0..n {
        rope.push((0, 0));
    }
    rope
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    let mut rope = create_rope(10);
    let mut tail_path = Vec::new();
    tail_path.push(*rope.last().unwrap());
    for line in lines {
        let movement: Delta = line.parse().unwrap();
        rope = step(rope, movement.signum(), movement.dx.abs() + movement.dy.abs(), &mut tail_path);
    }
    tail_path.sort_unstable();
    tail_path.dedup();
    println!("{}", tail_path.len());
}