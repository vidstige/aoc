use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut fishes: Vec<i32> = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap())
        .flat_map(|line| line.split(",").map(str::to_owned).collect::<Vec<_>>())
        .map(|word| word.parse().unwrap())
        .collect();
    
    let days = 80;
    for _day in 0..days {
        let mut new = 0;
        for fish in &mut fishes {
            if *fish == 0 {
                *fish = 6;
                new += 1;
            } else {
                *fish -=1;
            }
        }
        for _ in 0..new {
            fishes.push(8);
        }
    }
    /*for fish in fishes {
        println!("{}", fish);
    }*/
    println!("{}", fishes.len());
}
