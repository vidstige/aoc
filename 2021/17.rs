use std::io::{self, BufRead};
use regex::Regex;

type Target = ((i32, i32), (i32, i32));

fn parse(line: &String) -> Target {
    let re = Regex::new(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)").unwrap();    
    let captures = re.captures(&line).unwrap();
    let x1 = captures.get(1).unwrap().as_str().parse().unwrap();
    let x2 = captures.get(2).unwrap().as_str().parse().unwrap();
    let y1 = captures.get(3).unwrap().as_str().parse().unwrap();
    let y2 = captures.get(4).unwrap().as_str().parse().unwrap();
    ((x1, y1), (x2, y2))
}

fn hits(v: (i32, i32), target: Target) -> bool {
    let mut x = 0;
    let mut y = 0;
    let (mut vx, mut vy) = v;
    let ((x1, y1), (x2, y2)) = target;
    while y > y2 || vy > 0 {
        x += vx;
        y += vy;
        vx += -vx.signum();
        vy += -1;
        if x >= x1 && x <= x2 && y >= y1 && y <= y2 {
            return true;
        }
    }
    false
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    for line in lines {
        let target = parse(&line);
        println!("{}", hits((6, 3), target));
    }
}