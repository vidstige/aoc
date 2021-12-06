use std::io::{self, BufRead};

// 2^(d/7)

fn main() {
    let stdin = io::stdin();
    let initial: Vec<usize> = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap())
        .flat_map(|line| line.split(",").map(str::to_owned).collect::<Vec<_>>())
        .map(|word| word.parse().unwrap())
        .collect();
    
    let days = 256;
    let mut cycle: [i64; 9] = [0; 9];
    for fish in initial {
        cycle[fish] += 1;
    }

    for _day in 0..days {
        let mut dc: [i64; 9] = [0; 9];
        for i in 0..(9-1) {
            dc[i] += cycle[i + 1];
            dc[i + 1] -= cycle[i + 1];
        }
        dc[0] -= cycle[0];
        dc[8] += cycle[0]; // every fish with 0 spawn a new fish with 8
        dc[6] += cycle[0]; // all fishes with 0 resets to 6
        for i in 0..9 {
            cycle[i] += dc[i];
        }        
    }
    println!("{:?}", cycle.iter().map(|x| *x as i64).sum::<i64>());
}
