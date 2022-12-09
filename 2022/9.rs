use std::{io::{self, BufRead}, str::FromStr};

struct Movement {
    dx: i32,
    dy: i32,
}
type Point = (i32, i32);

impl FromStr for Movement {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {    
        let mut parts = s.split(" ");
        let direction = parts.next().unwrap();
        let amount = parts.next().unwrap().parse().unwrap();
        match direction {
            "R" => Ok(Movement{dx: amount, dy: 0}),
            "L" => Ok(Movement{dx: -amount, dy: 0}),
            "D" => Ok(Movement{dx: 0, dy: amount}),
            "U" => Ok(Movement{dx: 0, dy: -amount}),
            _ => Err(())
        }
    }
}

fn move_point(p: Point, m: Movement) -> Point {
    let (x, y) = p;
    (x + m.dx, y + m.dy)
}

fn delta(a: Point, b: Point) -> Movement {
    let (ax, ay) = a;
    let (bx, by) = b;
    Movement { dx: bx - ax, dy: by - ay }
}

fn follow(tail: Point, head: Point) -> Point {
    let d = delta(tail, head);
    if d.dx.abs() <= 1 && d.dy.abs() <= 1 {
        return tail;
    }
    move_point(tail, Movement { dx: d.dx.signum(), dy: d.dy.signum() })
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    let mut head = (0, 0);
    let mut tail = (0, 0);
    let mut tail_path = Vec::new();
    tail_path.push(tail);
    for line in lines {
        let movement: Movement = line.parse().unwrap();
        if movement.dx == 0 {
            for _ in 0..movement.dy.abs() {
                head = move_point(head, Movement { dx: 0, dy: movement.dy.signum() });
                tail = follow(tail, head);
                tail_path.push(tail);
            }
        }
        if movement.dy == 0 {
            for _ in 0..movement.dx.abs() {
                head = move_point(head, Movement { dx: movement.dx.signum(), dy: 0 });
                tail = follow(tail, head);
                tail_path.push(tail);
            }
        }
    }
    tail_path.sort_unstable();
    tail_path.dedup();
    println!("{}", tail_path.len());
}