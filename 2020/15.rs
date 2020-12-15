use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut turns: Vec<i32> = lines.map(|line| line.unwrap().parse().unwrap()).collect();

    for _ in turns.len()..2020 {
        let last_spoken = *turns.last().unwrap();
        let turn_said = turns.iter().rev().skip(1).position(|&w| w == last_spoken);
        let say = match turn_said {
            Some(t) => t as i32 + 1,
            None => 0
        };
        turns.push(say);
    }
    
    println!("{}", turns.last().unwrap());
}