use std::io::{self, BufRead};
use std::str::FromStr;

enum Instruction {
    AddX(i32),
    Noop,
}

impl FromStr for Instruction {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {    
        let mut parts = s.split(" ");
        let opcode = parts.next().unwrap();
        match opcode {
            "addx" => Ok(Instruction::AddX(parts.next().unwrap().parse().unwrap())),
            "noop" => Ok(Instruction::Noop),
            _ => Err(())
        }
    }
}

fn cycles_for(instruction: &Instruction) -> usize {
    match instruction { 
        Instruction::AddX(_) => 2,
        Instruction::Noop => 1,
    }
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    let instructions: Vec<Instruction> = lines.map(|line| line.parse().unwrap()).collect();
    
    let mut x = 1;
    let mut cycle = 1;
    let mut ip = 0;
    let mut cycles_left = cycles_for(&instructions[ip]);
    let mut signals = Vec::new();
    while ip < instructions.len() || cycles_left > 0 {
        let during = x;
        cycles_left -= 1;
        if cycles_left == 0 {
            // finish current instruction, if any
            if ip >= instructions.len() {
                break;
            }
            match instructions[ip] {
                Instruction::AddX(dx) => x += dx,
                Instruction::Noop => {},
            }
            ip += 1;

            // take next instruction
            cycles_left = if ip == instructions.len() { 1 } else { cycles_for(&instructions[ip]) };
        }

        let after = x;
        let signal_strength = cycle * during;
        //println!("cycle: {}, during: {}, after: {}, signal strength left: {}", cycle, during, after, signal_strength);
        if (cycle + 20) % 40 == 0 {            
            //println!("{} {} {}", cycle, during, signal_strength);
            signals.push(signal_strength);
        }
        
        cycle += 1;
    }
    println!("{}", signals.iter().sum::<i32>());
}