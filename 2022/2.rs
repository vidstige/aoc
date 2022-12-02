use std::io::{self, BufRead};
use std::str::FromStr;

enum Ply {Rock, Paper, Scissors}
enum Outcome {Win, Draw, Loss}

impl FromStr for Ply {
    type Err = String;
    fn from_str(input: &str) -> Result<Ply, Self::Err> {
        match input {            
            "A"  => Ok(Ply::Rock),
            "B"  => Ok(Ply::Paper),
            "C"  => Ok(Ply::Scissors),

            _ => Err(format!("Unknown ply '{}'", input)),
        }
    }
}

impl FromStr for Outcome {
    type Err = String;
    fn from_str(input: &str) -> Result<Outcome, Self::Err> {
        match input {
            "X"  => Ok(Outcome::Loss),
            "Y"  => Ok(Outcome::Draw),
            "Z"  => Ok(Outcome::Win),
            
            _ => Err(format!("Unknown outcome '{}'", input)),
        }
    }
}
fn outcome(a: &Ply, b: &Ply) -> Outcome {
    match (a, b) {
        (Ply::Rock, Ply::Rock) => Outcome::Draw,
        (Ply::Rock, Ply::Paper) => Outcome::Loss,
        (Ply::Rock, Ply::Scissors) => Outcome::Win,

        (Ply::Paper, Ply::Rock) => Outcome::Win,
        (Ply::Paper, Ply::Paper) => Outcome::Draw,
        (Ply::Paper, Ply::Scissors) => Outcome::Loss,

        (Ply::Scissors, Ply::Rock) => Outcome::Loss,
        (Ply::Scissors, Ply::Paper) => Outcome::Win,
        (Ply::Scissors, Ply::Scissors) => Outcome::Draw,
    }
}

fn score(opponent: &Ply, you: &Ply) -> i32 {
    let a = match you {
        Ply::Rock => 1,
        Ply::Paper => 2,
        Ply::Scissors => 3,
    };
    let b = match outcome(you, opponent) {
        Outcome::Win => 6,
        Outcome::Draw => 3,
        Outcome::Loss => 0,
    };
    a + b
}

fn find(opponent: &Ply, need: &Outcome) -> Ply {
    match (opponent, need) {
        (Ply::Rock, Outcome::Win) => Ply::Paper,
        (Ply::Rock, Outcome::Draw) => Ply::Rock,
        (Ply::Rock, Outcome::Loss) => Ply::Scissors,

        (Ply::Paper, Outcome::Win) => Ply::Scissors,
        (Ply::Paper, Outcome::Draw) => Ply::Paper,
        (Ply::Paper, Outcome::Loss) => Ply::Rock,

        (Ply::Scissors, Outcome::Win) => Ply::Rock,
        (Ply::Scissors, Outcome::Draw) => Ply::Scissors,
        (Ply::Scissors, Outcome::Loss) => Ply::Paper,
    }
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    
    let mut sum = 0;
    for line in lines {
        let mut parts = line.split_whitespace();
        let opponent = parts.next().unwrap().parse().unwrap();
        let need = parts.next().unwrap().parse().unwrap();
        let ply = find(&opponent, &need);
        sum += score(&opponent, &ply)
    }
    println!("{}", sum);
}
