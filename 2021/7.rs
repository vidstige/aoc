use std::io::{self, BufRead};

fn cost(crabs: &Vec<i32>, p: i32) -> i32 {
    crabs.iter().map(|c| c - p).map(i32::abs).sum()
}

fn main() {
    let stdin = io::stdin();
    let crabs: Vec<i32> = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap())
        .flat_map(|line| line.split(",").map(str::to_owned).collect::<Vec<_>>())
        .map(|word| word.parse().unwrap())
        .collect();

    let start = crabs.iter().min().unwrap();
    let end = crabs.iter().max().unwrap();
    let range = *start..*end;
    let cheapest = range.map(|p| cost(&crabs, p)).min();
    println!("{:?}", cheapest);
}