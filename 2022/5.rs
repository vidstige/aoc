use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let lines: Vec<_> = stdin.lock().lines().map(|line| line.unwrap()).collect();

    let index = lines.iter().position(|line| line.is_empty()).unwrap();

    let mut stacks: Vec<Vec<char>> = Vec::new();
    for line in &lines[0..index - 1] {
        let row: Vec<String> = line
            .chars()
            .collect::<Vec<char>>()
            .chunks(4)
            .map(|c| c.iter().collect::<String>())
            .collect();
        stacks.resize(row.len(), Vec::new());
        for (stack, column) in row.iter().enumerate() {
            let value = column.chars().nth(1).unwrap();
            if !value.is_whitespace() {
                stacks[stack].insert(0, value);
            }
        }
    }

    for line in &lines[index + 1..] {
        let mut tokens = line.split_whitespace();
        tokens.next(); // move
        let count = tokens.next().unwrap().parse::<usize>().unwrap();
        tokens.next(); // from
        let from = tokens.next().unwrap().parse::<usize>().unwrap() - 1;
        tokens.next(); // to
        let to: usize = tokens.next().unwrap().parse::<usize>().unwrap() - 1;

        for _ in 0..count {
            let value = stacks[from].pop().unwrap();
            stacks[to].push(value);
        }
    }

    let result: String = stacks.iter().map(|stack| stack.last().unwrap()).collect();

    println!("{}", result);
}