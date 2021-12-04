use std::io::{self, BufRead};
use std::collections::HashSet;
use std::iter::FromIterator;

struct Board {
    numbers: [[u8; 5]; 5],
}

impl Board {
    fn new() -> Board {
        Board{numbers: [[0u8; 5]; 5]}
    }
}

// Returns all ways to win in bingo
fn combos(board: &Board) -> Vec<HashSet<u8>> {
    let mut c = Vec::new();
    // columns
    for x in 0..5 {
        c.push((0..5).map(|y| board.numbers[y][x]).collect());
    }
    // rows
    for y in 0..5 {
        c.push((0..5).map(|x| board.numbers[y][x]).collect());
    }
    c
}

fn is_win(board: &Board, numbers: &Vec<u8>) -> bool {
    let set = HashSet::from_iter(numbers.iter().map(|n| *n));
    for combo in combos(board) {
        if combo.is_subset(&set) {
            return true
        }
    }
    false
}

fn score(board: &Board, numbers: &Vec<u8>) -> i32 {
    let set = HashSet::from_iter(numbers.iter().map(|n| *n as i32));
    let bs: HashSet<i32> = board.numbers.iter().flat_map(|row| row.iter()).map(|n| *n as i32).collect();
    let sum: i32 = bs.difference(&set).sum();
    let last_called = *numbers.last().unwrap() as i32;
    sum * last_called
}

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines().map(|line| line.unwrap());
    let numbers: Vec<u8> = lines.next().unwrap().split(",").map(|s| s.parse().unwrap()).collect();

    let mut boards: Vec<Board> = Vec::new();
    let mut blank = lines.next();
    while blank.is_some() {
        let mut board = Board::new();
        for y in 0..5 {
            let line = lines.next().unwrap();
            for (x, value) in line.split(" ").filter(|&s| !s.is_empty()).enumerate() {
                board.numbers[y][x] = value.parse().unwrap();
            }
        }
        boards.push(board);
        blank = lines.next();
    }

    'outer: for n in 0..numbers.len() {
        let so_far: Vec<u8> = numbers.iter().take(n).map(|n| *n).collect();
        for board in boards.iter() {
            if is_win(board, &so_far) {
                println!("score: {}", score(board, &so_far));
                break 'outer;
            }
        }
    }
}