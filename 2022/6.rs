use std::io::{self, BufRead};
use std::collections::HashSet;


fn distinct(window: &[char]) -> bool {
    let s: HashSet<_> = window.iter().collect();
    s.len() == window.len()
}

fn first_distinct(chars: &Vec<char>, n: usize) -> Option<usize> {
    let position = chars.windows(n).position(|window| distinct(window));
    match position {
        Some(p) => Some(p + n),
        None => None,
    }
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    for line in lines {
        let chars: Vec<_> = line.chars().collect();
        println!("{}, {}", first_distinct(&chars, 4).unwrap(), first_distinct(&chars, 14).unwrap());

    }
}