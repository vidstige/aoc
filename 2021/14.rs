use std::io::{self, BufRead};
use std::collections::HashMap;

fn parse(stdin: std::io::Stdin) -> (String, HashMap<(char, char), char>) {
    let mut lines = stdin.lock()
        .lines()
        .map(|line| line.unwrap());

    let initial = lines.next().unwrap();
    lines.next(); // blank
    let mut rules = HashMap::new();
    for line in lines {
        let mut splitter = line.split(" -> ");
        let from_str = splitter.next().unwrap();
        let to = splitter.next().unwrap();
        let mut from_chars = from_str.chars();
        let a = from_chars.next().unwrap();
        let b = from_chars.next().unwrap();
        rules.insert((a, b), to.chars().next().unwrap());
    }
    (initial, rules)
}

fn pairwise<I>(right: I) -> impl Iterator<Item = (I::Item, I::Item)>
where
    I: IntoIterator + Clone,
{
    let left = right.clone().into_iter().skip(1);
    left.zip(right)
}

fn step(polymer: &String, rules: &HashMap<(char, char), char>) -> String {
    let mut tmp = Vec::new();
    for (b, a) in pairwise(polymer.chars()) {
        match rules.get(&(a, b)) {
            Some(c) => {
                tmp.push(a);
                tmp.push(*c);
            },
            None => {
                tmp.push(a);
            }
        }
    }
    tmp.push(polymer.chars().last().unwrap());
    tmp.iter().collect()
}

fn frequency(s: &String) -> HashMap<char, usize> {
    let mut f = HashMap::new();
    for c in s.chars() {
        *f.entry(c).or_default() += 1;
    }
    f
}

fn main() {
    let stdin = io::stdin();
    let (initial, rules) = parse(stdin);
    let mut polymer = initial;
    for _ in 0..10 {
        polymer = step(&polymer, &rules);
    }
    let f = frequency(&polymer);
    println!("{:?}", f.values().max().unwrap() - f.values().min().unwrap());
}