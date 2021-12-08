use std::io::{self, BufRead};
use std::collections::{HashSet, HashMap};
use std::iter::FromIterator;
use itertools::Itertools;

fn all_segments(segments: &Vec<HashSet<char>>) -> HashSet<char> {
    let mut tmp = HashSet::new();
    for segment in segments {
        tmp.extend(segment);
    }
    tmp
}

fn transform(values: &HashSet<char>, map: &HashMap<char, char>) -> HashSet<char> {
    values.iter().map(|c| *map.get(c).unwrap()).collect()
}

fn search(digits: &Vec<HashSet<char>>, values: &Vec<HashSet<char>>) -> Option<HashMap<char, char>> {
    // lock order
    let old: Vec<char> = all_segments(digits).into_iter().collect();
    'mega: for new in old.iter().permutations(old.len()) {
        let mut map = HashMap::new();
        for (a, b) in new.into_iter().zip(old.iter()) {
            map.insert(*a, *b);
        }
        for value in values {
            if !digits.contains(&transform(value, &map)) {
                continue 'mega;
            }
        }
        return Some(map);
    }
    None
}

fn display(digits: &Vec<HashSet<char>>, value: &HashSet<char>) -> Option<usize> {
    for (i, digit) in digits.iter().enumerate() {
        if digit == value {
            return Some(i);
        }
    }
    None
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap());

    let mut digits: Vec<HashSet<_>> = Vec::new();
    digits.push(HashSet::from_iter("abcefg".chars()));
    digits.push(HashSet::from_iter("cf".chars()));
    digits.push(HashSet::from_iter("acdeg".chars()));
    digits.push(HashSet::from_iter("acdfg".chars()));
    digits.push(HashSet::from_iter("bcdf".chars()));
    digits.push(HashSet::from_iter("abdfg".chars()));
    digits.push(HashSet::from_iter("abdefg".chars()));
    digits.push(HashSet::from_iter("acf".chars()));
    digits.push(HashSet::from_iter("abcdefg".chars()));
    digits.push(HashSet::from_iter("abcdfg".chars()));

    let mut sum = 0;
    for line in lines {
        let mut splitter = line.splitn(2, " | ");
        let first = splitter.next().unwrap();
        let second = splitter.next().unwrap();

        let inputs: Vec<HashSet<char>> = first.split(' ').map(|w| w.chars().collect()).collect();
        let outputs: Vec<HashSet<char>> = second.split(' ').map(|w| w.chars().collect()).collect();
        let all = inputs.into_iter().chain(outputs.clone().into_iter()).collect();

        match search(&digits, &all) {
            Some(map) => {
                let mut o = Vec::new();
                for output in outputs {
                    let values = transform(&output, &map);
                    o.push(display(&digits, &values).unwrap().to_string());
                }
                let tmp: usize = o.join("").parse().unwrap();
                sum += tmp;
            },
            None => {
                println!("No solution found");
            }
        }
    }
    println!("{}", sum);
}