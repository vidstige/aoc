use std::io::{self, BufRead};

fn points_for(c: char) -> usize {
    match c {
        ')' => 1,
        ']' => 2,
        '}' => 3,
        '>' => 4,
        _ => 0,
    }
}

fn parse(line: String) -> Option<usize> {
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
                return None;
            }
        }
    }
    stack.reverse();
    let mut score = 0;
    for character in stack {
        let open_index = opening.chars().position(|c| c == character).unwrap();
        let expected = closing.chars().nth(open_index).unwrap();

        score *= 5;
        score += points_for(expected);
    }
    return Some(score);
}


fn main() {
    let stdin = io::stdin();
    let lines = stdin
        .lock()
        .lines()
        .map(|line| line.unwrap());

    let mut scores: Vec<usize> = lines.map(parse).flatten().collect();
    scores.sort();
    println!("{}", scores[scores.len() / 2]);
}