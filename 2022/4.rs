use std::io::{self, BufRead};
use std::ops::Range;

fn parse_assignment(assignment: &str) -> Range<i32> {
    let mut split = assignment.split("-");
    let start = split.next().unwrap().parse().unwrap();
    let end: i32 = split.next().unwrap().parse().unwrap();
    start..end + 1
}

fn contains(a: &Range<i32>, b: &Range<i32>) -> bool {
    a.contains(&b.start) && a.contains(&(b.end - 1)) || b.contains(&a.start) && b.contains(&(a.end - 1))
}

fn overlaps(a: &Range<i32>, b: &Range<i32>) -> bool {
    (a.start < b.end) && (a.end > b.start)
}

fn parse_elf_pair(line: &String) -> (Range<i32>, Range<i32>) {
    let mut split = line.split(",");
    let a = parse_assignment(split.next().unwrap());
    let b = parse_assignment(split.next().unwrap());
    (a, b)
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    let elf_pairs: Vec<_> = lines.map(|line| parse_elf_pair(&line)).collect();

    println!("{}", elf_pairs.iter().filter(|(a, b)| contains(&a, &b)).count());
    println!("{}", elf_pairs.iter().filter(|(a, b)| overlaps(&a, &b)).count());
}