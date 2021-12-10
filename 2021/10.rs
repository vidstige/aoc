use std::io::{self, BufRead};

fn parse(line: String) -> Option<char> {
    let opening = "([{<";
    let closing = ")]}>";
    let mut stack = Vec::new();
    for c in line.chars() {
        if opening.contains(c) {
            stack.push(c);
        }
        if closing.contains(c) {
            let open = stack.pop().unwrap();
            let open_index = opening.chars().position(|c| c == open).unwrap();
            let expected = closing.chars().nth(open_index).unwrap();
            if c != expected {
                return Some(c);
            }
        }
    }
    None
}

fn score(c: char) -> usize {
    match c {
        ')' => 3,
        ']' => 57,
        '}' => 1197,
        '>' => 25137,
        _ => 0,
    }
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap());

    let total: usize = lines.map(parse).flatten().map(score).sum();
    println!("{}", total);
}