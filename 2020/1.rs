use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let tab: Vec<i32> = stdin.lock().lines().into_iter().map(|line| line.unwrap().parse::<i32>().unwrap()).collect();

    for i in 0..tab.len() {
        for j in i..tab.len() {
            if tab[i] + tab[j] == 2020 {
                println!("{}", tab[i] * tab[j]);
            }
        }
    }
}