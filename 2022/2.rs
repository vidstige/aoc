use std::io::{self, BufRead};
use std::str::FromStr;

enum RPS {Rock, Paper, Scissors}

impl FromStr for RPS {
    type Err = String;
    fn from_str(input: &str) -> Result<RPS, Self::Err> {
        match input {
            "X"  => Ok(RPS::Rock),
            "Y"  => Ok(RPS::Paper),
            "Z"  => Ok(RPS::Scissors),
            
            "A"  => Ok(RPS::Rock),
            "B"  => Ok(RPS::Paper),
            "C"  => Ok(RPS::Scissors),

            _ => Err(format!("Unknown ply '{}'", input)),
        }
    }
}

fn outcome(a: RPS, b: RPS) -> i32 {
    match (a, b) {
        (RPS::Rock, RPS::Rock) => 0,
        (RPS::Rock, RPS::Paper) => -1,
        (RPS::Rock, RPS::Scissors) => 1,

        (RPS::Paper, RPS::Rock) => 1,
        (RPS::Paper, RPS::Paper) => 0,
        (RPS::Paper, RPS::Scissors) => -1,

        (RPS::Scissors, RPS::Rock) => -1,
        (RPS::Scissors, RPS::Paper) => 1,
        (RPS::Scissors, RPS::Scissors) => 0,
    }
}

fn score(opponent: RPS, you: RPS) -> i32 {
    let tmp = match you {
        RPS::Rock => 1,
        RPS::Paper => 2,
        RPS::Scissors => 3,
    };
    tmp + (outcome(you, opponent) + 1) * 3
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    
    let mut sum = 0;
    for line in lines {
        let mut parts = line.split_whitespace();
        let predicted = parts.next().unwrap().parse().unwrap();
        let recommendation = parts.next().unwrap().parse().unwrap();
        sum += score(predicted, recommendation)
    }
    println!("{}", sum);
}
