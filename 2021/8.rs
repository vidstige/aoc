use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::FromIterator;

fn main() {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap());

    let mut digital: Vec<HashSet<_>> = Vec::new();
    digital.push(HashSet::from_iter("abcefg".chars()));
    digital.push(HashSet::from_iter("cf".chars()));
    digital.push(HashSet::from_iter("acdeg".chars()));
    digital.push(HashSet::from_iter("acdfg".chars()));
    digital.push(HashSet::from_iter("bcdf".chars()));
    digital.push(HashSet::from_iter("abdfg".chars()));
    digital.push(HashSet::from_iter("abdefg".chars()));
    digital.push(HashSet::from_iter("acf".chars()));
    digital.push(HashSet::from_iter("abcdefg".chars()));
    digital.push(HashSet::from_iter("abcdfg".chars()));

    for (i, d) in digital.iter().enumerate() {
        println!("{} {}", i, d.len());
    }
    
    let mut sum = 0;
    for line in lines {
        let mut splitter = line.splitn(2, " | ");
        let first = splitter.next().unwrap();
        let second = splitter.next().unwrap();

        //let mut displayed: Vec<HashSet<_>> = Vec::new();
        for word in second.split(' ') {
            //displayed.push(word.chars().collect());
            let displayed: HashSet<_> = word.chars().collect();

            for i in [1, 4, 7, 8] {
                if digital[i].len() == displayed.len() {
                    sum +=1;
                }
            }
        }
        
    }
    println!("{}", sum);
}