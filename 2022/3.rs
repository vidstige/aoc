use std::io::{self, BufRead};
use std::collections::HashSet;

fn priority(c: &char) -> i32 {
    let items = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    items.find(*c).unwrap() as i32 + 1
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    let mut sum = 0;
    for line in lines {
        let mid = line.len() / 2;
        let a: HashSet<_> = line.chars().take(mid).collect();
        let b: HashSet<_> = line.chars().skip(mid).collect();
        let common = a.intersection(&b);
        
        sum += common.map(|c| priority(c)).sum::<i32>();
    }
    println!("{}", sum);
}