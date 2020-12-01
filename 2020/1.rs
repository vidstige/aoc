use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let tab: Vec<i32> = lines.map(|line| line.unwrap().parse::<i32>().unwrap()).collect();

    for i in 0..tab.len() {
        for j in (i+1)..tab.len() {
            if tab[i] + tab[j] == 2020 {
                println!("{}", tab[i] * tab[j]);
            }
        }
    }
}