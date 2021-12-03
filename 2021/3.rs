use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();

    let mut count0 = Vec::new();
    let mut count1 = Vec::new();
    for maybe_line in lines {
        let line = maybe_line.unwrap();
        count0.resize(line.len(), 0);
        count1.resize(line.len(), 0);
        for (i, c) in line.chars().enumerate() {
            match c {
                '0' => count0[i] += 1,
                '1' => count1[i] += 1,
                _ => println!("bad character"),
            }
        }
    }
    
    let mut m = 1;
    let mut gamma = 0;
    let mut epsilon = 0;
    for (c0, c1) in count0.iter().rev().zip(count1.iter().rev()) {
        if c1 > c0 {
            gamma += m;
        } else {
            epsilon += m;
        }
        m *= 2;
    }
    println!("{:?} {:?} => {:?}", gamma, epsilon, gamma * epsilon);
}