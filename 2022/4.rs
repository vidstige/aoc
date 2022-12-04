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

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    let mut contained = 0;
    let mut overlapping = 0;

    for line in lines {
        let mut split = line.split(",");
        let a = parse_assignment(split.next().unwrap());
        let b = parse_assignment(split.next().unwrap());
        //println!("{} - {}, {} - {}: {}", a.start, a.end - 1, b.start, b.end - 1, overlaps(&a, &b));
        if contains(&a, &b) {
            contained += 1;
        }
        if overlaps(&a, &b) {
            overlapping += 1;
        }
    }
    println!("{}", contained);
    println!("{}", overlapping);
}