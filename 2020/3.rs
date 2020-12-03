use std::io::{self, BufRead};
fn main() {
    let stdin = io::stdin();
    let trees: Vec<_> = stdin.lock().lines().map(|line| line.unwrap()).collect();
    let mut x: usize = 0;
    let mut y: usize = 0;
    let dx: usize = 3;
    let dy: usize = 1;
    let mut n: i32 = 0;
    while y < trees.len() {
        if trees[y].chars().nth(x % trees[y].len()) == Some('#') {
            n += 1
        }
        x += dx;
        y += dy;
    }
    println!("{}", n);
}