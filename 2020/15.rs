use std::io::{self, BufRead};
use std::collections::HashMap;

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let mut turns: HashMap<i32, i32> = HashMap::new();
    let mut last_spoken: i32 = -1;
    for (i, say) in lines.map(|line| line.unwrap().parse::<i32>().unwrap()).enumerate() {
        turns.insert(say, i as i32);
        last_spoken = say;
    }
    turns.remove(&last_spoken);

    for i in turns.len()..30000000 - 1 {
        let turn_said = turns.get(&last_spoken);
        let say = match turn_said {
            Some(t) => i as i32 - t,
            None => 0
        };
        turns.insert(last_spoken, i as i32);
        last_spoken = say;
    }
    
    println!("{}", last_spoken);
}