use std::io::{self, BufRead};
use std::collections::HashSet;

fn first_distinct(chars: &Vec<char>, n: usize) -> Option<usize> {
    for (index, window) in chars.windows(n).enumerate() {
        let s: HashSet<_> = window.iter().collect();
        if s.len() == window.len() {
            return Some(index + window.len());
        }
    }
    None
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    for line in lines {
        let chars: Vec<_> = line.chars().collect();
        println!("{}, {}", first_distinct(&chars, 4).unwrap(), first_distinct(&chars, 14).unwrap());

    }
}