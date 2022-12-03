use std::io::{self, BufRead};
use std::collections::HashSet;
use itertools::Itertools;
 
fn priority(c: &char) -> i32 {
    let items = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
    items.find(*c).unwrap() as i32 + 1
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    let mut sum = 0;
    for (a, b, c) in lines.tuples() {
        let rucksack_a: HashSet<_> = a.chars().collect();
        let rucksack_b: HashSet<_> = b.chars().collect();
        let rucksack_c: HashSet<_> = c.chars().collect();
        
        let mut badge: HashSet<char> = rucksack_a.intersection(&rucksack_b).map(|c| *c).collect();
        badge = badge.intersection(&rucksack_c).map(|c| *c).collect();
        sum += badge.iter().map(|b| priority(b)).sum::<i32>();

        //let mid = line.len() / 2;
        //let a: HashSet<_> = line.chars().take(mid).collect();
        //let b: HashSet<_> = line.chars().skip(mid).collect();
        //let common = a.intersection(&b);
        
        //sum += common.map(|c| priority(c)).sum::<i32>();
        //println!("{}", a);
    }
    println!("{}", sum);
}