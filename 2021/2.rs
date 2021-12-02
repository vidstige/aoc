use std::io::{self, BufRead};

struct Position {
    x: i32,
    depth: i32,
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    
    let mut p = Position{x: 0, depth: 0};
    for maybe_line in lines {
        let line = maybe_line.unwrap();        
        let mut parts = line.split(" ");
        let command = parts.next().unwrap();
        let amount: i32 = parts.next().unwrap().parse().unwrap();
        match command.as_ref() {
            "forward" => p.x += amount,
            "down" => p.depth += amount,
            "up" => p.depth -= amount,
            _ => println!("unknown command: {}", command),
        }
      }
      println!("({}, {})", p.x, p.depth);
      println!("{}", p.x * p.depth);
}