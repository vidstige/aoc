use std::io::{self, BufRead};
use std::str::FromStr;

fn line_value(line: &String) -> String {
    let mut parts = line.split(":");
    parts.next();
    parts.next().unwrap().trim().to_string()
}

enum Operand {
    Literal(i32),
    Old,
}

impl Operand {
    fn apply(&self, old: i32) -> i32 {
        match self {
            Operand::Literal(value) => *value,
            Operand::Old => old,
        }
    }
}

enum Operation {
    Add(Operand, Operand),
    Mul(Operand, Operand)
}

impl Operation {
    fn apply(&self, old: i32) -> i32 {
        match self {
            Operation::Add(left, right) => left.apply(old) + right.apply(old),
            Operation::Mul(left, right) => left.apply(old) * right.apply(old),
        }
    }
}

impl FromStr for Operand {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "old" => Ok(Operand::Old),
            _ => Ok(Operand::Literal(s.parse().unwrap())),
        }
    }
}

struct Monkey {
    items: Vec<i32>,
    operation: Operation,
    test: i32,
    throw_true: usize,
    throw_false: usize,
    counter: usize,
}

fn parse_monkey(lines: &[String]) -> Monkey {
    let items: Vec<i32> = line_value(&lines[1]).split(",").map(|p| p.trim().parse().unwrap()).collect();
    
    let value = line_value(&lines[2]);
    let mut parts = value.split(" ");
    parts.next(); // new
    parts.next(); // =
    let left = parts.next().unwrap();
    let operator = parts.next();
    let right = parts.next().unwrap();
    let operation = match operator {
        Some("*") => Operation::Mul(left.parse().unwrap(), right.parse().unwrap()),
        Some("+") => Operation::Add(left.parse().unwrap(), right.parse().unwrap()),
        _ => { panic!("Unknown operation"); },
    };

    let test_value = lines[3].split_whitespace().last().unwrap().parse().unwrap();
    let throw_true = lines[4].split_whitespace().last().unwrap().parse().unwrap();
    let throw_false = lines[5].split_whitespace().last().unwrap().parse().unwrap();

    Monkey{
        items: items,
        operation: operation,
        test: test_value,
        throw_true: throw_true,
        throw_false: throw_false,
        counter: 0,
    }
}

fn throw(monkeys: &mut Vec<Monkey>, index: usize) {
    let monkey = &monkeys[index];
    for item in monkey.items.clone() {
        monkeys[index].counter += 1;
        let value = monkeys[index].operation.apply(item) / 3;
        let to_index = if value % monkeys[index].test == 0 {
            monkeys[index].throw_true
        } else {
            monkeys[index].throw_false
        };
        monkeys[to_index].items.push(value);
    }
    monkeys[index].items.clear();
}

fn main() {
    let stdin = io::stdin();
    let lines: Vec<_> = stdin.lock().lines().map(|line| line.unwrap()).collect();
    
    let mut monkeys: Vec<_> = lines.chunks(7).map(|ml| parse_monkey(ml)).collect();

    for _ in 0..20 {
        for index in 0..monkeys.len() {
            throw(&mut monkeys, index);
        }
    }

    let mut counters: Vec<_> = monkeys.iter().map(|monkey| monkey.counter).collect();
    counters.sort();
    counters.reverse();
    println!("{}", counters[0] * counters[1]);
    
}