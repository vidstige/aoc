use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut elfs = vec!();
    let mut acc = 0;
    for line in lines.map(|line| line.unwrap()) {
        if line.is_empty() {
            elfs.push(acc);
            acc = 0;
        } else {
            let calories = line.parse::<i32>().unwrap();
            acc += calories;
        }
    }
    let top_elf = elfs.iter().max().unwrap();
    println!("{}", top_elf);
}