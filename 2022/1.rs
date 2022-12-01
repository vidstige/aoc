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
    elfs.push(acc);

    elfs.sort();
    elfs.reverse();
    println!("{} {}", elfs[0], elfs[0..3].iter().sum::<i32>());
}