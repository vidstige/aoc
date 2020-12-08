use std::io::{self, BufRead};
use std::collections::HashSet;

fn parse_line(line: &str) -> (String, i32) {
    let mut parts = line.split_whitespace();
    let opcode = parts.next().unwrap();
    let operand = parts.next().unwrap().parse::<i32>().unwrap();
    return (opcode.to_string(), operand)
}

fn boot(program: &Vec<(String, i32)>) -> bool {
    let mut visited = HashSet::new();

    let mut accumulator: i32 = 0;
    let mut ip: i32 = 0;
    while ip < program.len() as i32 {
        if visited.contains(&ip) {
            return false;
        }
        visited.insert(ip);
        let (opcode, operand) = &program[ip as usize];
        match opcode.as_str() {
            "acc" => accumulator += *operand,
            "jmp" => ip = ip + operand - 1,
            "nop" => {},
            _ => println!("Unknown opcode: {}", opcode),
        }
        ip += 1;
    }
    println!("accumulator: {}", accumulator);
    return true
}

fn main() {
    let stdin = io::stdin();
    let mut program: Vec<_> = stdin.lock()
        .lines()
        .map(|line| line.unwrap())
        .map(|line| parse_line(&line))
        .collect();
    
    for i in 0..program.len() {
        let backup = &program[i].0.to_string();
        // modify program
        program[i].0 = match program[i].0.as_str() {
            "jmp" => "nop",
            "nop" => "jmp",
            _ => program[i].0.as_str()
        }.to_string();

        // run if modified
        if &program[i].0 != backup {
            println!("replacing {} with {} at {}", backup, program[i].0, i);
            if boot(&program) {
                println!("ok!")
            }
        }

        // restore program
        program[i].0 = backup.to_string();
    }

    //println!("accumulator: {}, ip: {}", accumulator, ip);
    //println!("{}", program.len())
}
