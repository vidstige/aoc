use std::io::{self, BufRead};

fn filter_diagnostic_report(lines: Vec<String>, i: usize, c: char) -> Vec<String> {
    lines.into_iter().filter(|line| line.chars().nth(i).unwrap() == c ).collect()
}

fn counters(lines: Vec<String>) -> (Vec<i32>, Vec<i32>) {
    let mut count0 = Vec::new();
    let mut count1 = Vec::new();
    for line in lines {
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
    (count0, count1)
}

fn main() {
    let stdin = io::stdin();
    let lines: Vec<_> = stdin.lock()
        .lines()
        .map(|line| line.unwrap()).collect();

    let (count0, count1) = counters(lines.clone());
    
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

    let mut tmp = lines.clone();
    let mut i = 0;
    while tmp.len() > 1 {
        let (count0, count1) = counters(tmp.clone());
        let c = if count0[i] > count1[i] { '0' } else { '1' };
        tmp = filter_diagnostic_report(tmp, i, c);
        i += 1;
    }
    let oxygen_generator_rating = i32::from_str_radix(&tmp[0], 2).unwrap();

    let mut tmp = lines.clone();
    let mut i = 0;
    while tmp.len() > 1 {
        let (count0, count1) = counters(tmp.clone());
        let c = if count0[i] > count1[i] { '1' } else { '0' };
        tmp = filter_diagnostic_report(
            tmp, i, c);
        i += 1;
    }
    let co2_scrubber_rating = i32::from_str_radix(&tmp[0], 2).unwrap();

    println!("{}, {} -> {}", oxygen_generator_rating, co2_scrubber_rating, oxygen_generator_rating * co2_scrubber_rating);
    

}