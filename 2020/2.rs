use std::io::{self, BufRead};
use std::ops::Range;


fn parse_range(range: &str) -> Range<usize> {
    let mut parts = range.split("-");
    let start = parts.next().unwrap().parse::<usize>().unwrap();
    let end = parts.next().unwrap().parse::<usize>().unwrap();
    assert_eq!(None, parts.next());
    Range{start: start, end: end + 1}
}

fn xor(a: bool, b: bool) -> bool {
    (a || b ) && !(a && b)
}

fn validate_policy(password: &str, character: &str, range: Range<usize>) -> bool {
    let first = range.start..(range.start + 1);
    let second = (range.end-1)..range.end;
    println!("{} {}", &password[first.clone()], &password[second.clone()]);
    return xor(&password[first] == character, &password[second] == character);

    //let n = password.matches(character).count();
    //return range.contains(&n);
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut n = 0;
    //let tab: Vec<i32> = lines.map(|line| line.unwrap().parse::<i32>().unwrap()).collect();
    for line in lines.map(|line| line.unwrap()) {
        let mut parts = line.split(":");
        let mut policy_parts = parts.next().unwrap().split(" ");
        let range = parse_range(policy_parts.next().unwrap());
        let character = policy_parts.next().unwrap();
        let password: &str = parts.next().unwrap();
        let valid = validate_policy(password, character, range);
        println!("{}: {}", line, valid);
        if valid {
            n += 1;
        }
    }
    println!("{}", n);
}