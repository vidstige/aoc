use std::io::{self, BufRead};

fn partition(boarding: &str) -> (i32, i32) {
    let mut row = 0..128;
    let mut column = 0..8;
    for character in boarding.chars() {
        if character == 'F' {
            let mid = (row.start + row.end) / 2;
            row = row.start..mid;
        }
        if character == 'B' {
            let mid = (row.start + row.end) / 2;
            row = mid..row.end;
        }
        if character == 'L' {
            let mid = (column.start + column.end) / 2;
            column = column.start..mid;
        }
        if character == 'R' {
            let mid = (column.start + column.end) / 2;
            column = mid..column.end;
        }
    }
    (row.start, column.start)
}

fn seat_id((row, column): (i32, i32)) -> i32 { row * 8 + column }

fn main() {
    let stdin = io::stdin();
    let boarding_passes: Vec<_> = stdin.lock()
        .lines()
        .map(|line| line.unwrap()).collect();
    
    let mut seat_ids: Vec<i32> = Vec::new();
    for boarding_pass in boarding_passes {
        let position = partition(&boarding_pass);
        seat_ids.push(seat_id(position));
    }
    println!("{}", seat_ids.iter().max().unwrap());
    //let (r, c) = partition("BFFFBBFRRR");
    //println!("{} {}", r, c);
}