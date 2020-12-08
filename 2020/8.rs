use std::io::{self, BufRead};
use std::collections::HashSet;

fn parse_line(line: &str) -> (String, i32) {
    let mut parts = line.split_whitespace();
    let opcode = parts.next().unwrap();
    let operand = parts.next().unwrap().parse::<i32>().unwrap();
    return (opcode.to_string(), operand)
}

fn main() {
    let stdin = io::stdin();
    let program: Vec<_> = stdin.lock()
        .lines()
        .map(|line| line.unwrap())
        .map(|line| parse_line(&line))
        .collect();
    
    let mut visited = HashSet::new();

    let mut accumulator: i32 = 0;
    let mut ip: i32 = 0;
    while !visited.contains(&ip) {
        visited.insert(ip);
        let (opcode, operand) = &program[ip as usize];
        //println!("{} {} | {} {}", opcode, operand, accumulator, ip);
        match opcode.as_str() {
            "acc" => accumulator += *operand,
            "jmp" => ip = ip + operand - 1,
            "nop" => {},
            _ => println!("Unknown opcode: {}", opcode),
        }
        ip += 1;
    }
    println!("accumulator: {}, ip: {}", accumulator, ip);
}
