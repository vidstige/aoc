use std::{io::{self, Read}, collections::HashSet};

enum Direction {Left, Right}

impl Direction {
    fn from_char(char: char) -> Option<Direction> {
        match char {
            '<' =>  Some(Direction::Left),
            '>' => Some(Direction::Right),
            _ => None,
        }
    }
}

fn slurp() -> String {
    let stdin = io::stdin();
    let mut buffer = String::new();
    stdin.lock().read_to_string(&mut buffer).unwrap();
    buffer
}

fn parse(s: String) -> Vec<Direction> {
    s.chars().filter_map(|c| Direction::from_char(c)).collect()
}

struct Grid {
    levels: Vec<[bool; 7]>
}

impl Grid {
    fn new() -> Grid {
        Grid { levels: Vec::new() }
    }
}

fn main() {
    let mut directions = parse(slurp()).iter().cycle();
    let stones = Vec::from([8 as i32]);
    let mut grid = Grid::new();

    for stone in stones.iter().cycle().take(2022) {
        while let Some(position) = step(stone) {
            
        }
        
    }
    
    println!("{}", 17);
}