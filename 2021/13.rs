use std::io::{self, BufRead};
use std::collections::HashSet;

#[derive(Debug)]
enum Instruction {
    Vertical(i32),
    Horizontal(i32),
}

fn parse(stdin: std::io::Stdin) -> (HashSet<(i32, i32)>, Vec<Instruction>) {
    let lines = stdin.lock()
        .lines()
        .map(|line| line.unwrap());

    let mut map = HashSet::new();
    let mut instructions = Vec::new(); 
    let mut reading_coords = true;
    for line in lines {
        if line.is_empty() {
            reading_coords = false;
            continue;
        }
        if reading_coords {
            let mut parts = line.split(',');
            let x: i32 = parts.next().unwrap().parse().unwrap();
            let y: i32 = parts.next().unwrap().parse().unwrap();
            map.insert((x,  y));
        } else {
            let mut parts = line.split(' ');
            parts.next(); // "fold"
            parts.next(); // "along"
            let tmp = parts.next().unwrap();
            let mut splitter = tmp.split('=');
            let axis = splitter.next().unwrap();
            let at: i32 = splitter.next().unwrap().parse().unwrap();
            let maybe_fold = 
                match axis {
                    "x" => Some(Instruction::Vertical(at)),
                    "y" => Some(Instruction::Horizontal(at)),
                    _ => None,
                };
            if let Some(fold) = maybe_fold {
                instructions.push(fold);
            }
        }
    }
    (map, instructions)
}

fn fold(before: &HashSet<(i32, i32)>, instruction: &Instruction) -> HashSet<(i32, i32)> {
    match instruction {
        Instruction::Vertical(x0) => {
            before.iter().map(|(x, y)| 
                if *x > *x0 { (2* *x0 - *x, *y) } else { (*x, *y) }
            ).collect()
        }
        Instruction::Horizontal(y0) => {
            before.iter().map(|(x, y)| 
                if *y > *y0 { (*x, 2 * *y0 - *y) } else { (*x, *y) }
            ).collect()
        }
    }
}

fn print(map: &HashSet<(i32, i32)>) {
    let xmin = *map.iter().map(|(x, _)| x).min().unwrap();
    let xmax = *map.iter().map(|(x, _)| x).max().unwrap();
    let ymin = *map.iter().map(|(_, y)| y).min().unwrap();
    let ymax = *map.iter().map(|(_, y)| y).max().unwrap();
    for y in ymin..(ymax + 1) {
        for x in xmin..(xmax + 1) {
            let c = if map.contains(&(x, y)) { '*' } else { ' ' };
            print!("{}", c);
        }
        println!();
    }
}

fn main() {
    let stdin = io::stdin();
    let (original, instructions) = parse(stdin);
    let mut map = original;
    for instruction in instructions {
        map = fold(&map, &instruction);
    }
    print(&map);
    println!("{}", map.len());
    
}