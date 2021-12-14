use std::io::{self, BufRead};
use std::collections::HashMap;

type Polymer = HashMap<(char, char), usize>;

fn pairwise<I>(right: I) -> impl Iterator<Item = (I::Item, I::Item)>
where
    I: IntoIterator + Clone,
{
    let left = right.clone().into_iter().skip(1);
    left.zip(right)
}

fn parse(stdin: std::io::Stdin) -> (Polymer, HashMap<(char, char), char>) {
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
    let mut polymer = HashMap::new();
    for (b, a) in pairwise(initial.chars()) {
        *polymer.entry((a, b)).or_insert(0) += 1;
    }
    (polymer, rules)
}

fn step(polymer: &Polymer, rules: &HashMap<(char, char), char>) -> Polymer {
    let mut deltas = HashMap::new();
    for (pair, count) in polymer {
        if let Some(to) = rules.get(pair) {
            *deltas.entry(*pair).or_insert(0) -= count;
            let (a, b) = pair;
            *deltas.entry((*a, *to)).or_insert(0) += count;
            *deltas.entry((*to, *b)).or_insert(0) += count;
        }
    }
    let mut new = polymer.clone();
    for (pair, delta) in deltas {
        *new.entry(pair).or_insert(0) += delta;
    }
    new
}

fn main() {
    let stdin = io::stdin();
    let (initial, rules) = parse(stdin);
    let mut polymer = initial;
    for _ in 0..40 {
        polymer = step(&polymer, &rules);
    }
    
    let mut f: HashMap<char, usize> = HashMap::new();
    for ((a, b), count) in polymer {
        *f.entry(a).or_insert(0) += count;
        *f.entry(b).or_insert(0) += count;
    }
    let lo = f.values().min().unwrap();
    let hi = f.values().max().unwrap();
    let diff = (hi+1) / 2 - (lo+1) / 2;
    println!("{}", diff);
}