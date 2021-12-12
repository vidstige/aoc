use std::io::{self, BufRead};
use std::collections::{HashMap, LinkedList};

fn parse(stdin: std::io::Stdin) -> HashMap<String, Vec<String>> {
    let lines = stdin
    .lock()
    .lines()
    .map(|line| line.unwrap());

    let mut map = HashMap::new();
    for line in lines {
        let mut parts = line.splitn(2, '-');
        let from = parts.next().unwrap().to_string();
        let to = parts.next().unwrap().to_string();
        map.entry(from.clone()).or_insert_with(Vec::new).push(to.clone());
        map.entry(to.clone()).or_insert_with(Vec::new).push(from.clone());
    }
    map
}

fn is_big(cave_id: &String) -> bool {
    return &cave_id.to_uppercase() == cave_id;
}

fn frequency(v: &Vec<&String>) -> HashMap<String, usize> {
    let mut f = HashMap::new();
    for s in v {
        *f.entry(s.to_string()).or_default() += 1;
    }
    f
}

fn is_acceptable(path: &Vec<String>) -> bool {
    let small = path.iter().filter(|ci| !is_big(ci)).collect();
    let freq = frequency(&small);
    // small caves may only be visited once, except one cave
    // may be visited twice
    if freq.values().filter(|c| **c == 2).count() > 1 {
        return false;
    }
    // no cave may be visited _more_ than once
    if freq.values().any(|c| *c > 2) {
        return false;
    }
    // start & end can only be visited at most once
    if freq.get(&"start".to_string()).unwrap_or(&0) > &1 {
        return false;
    }
    if freq.get(&"end".to_string()).unwrap_or(&0) > &1 {
        return false;
    }
    true
}

fn search(map: &HashMap<String, Vec<String>>) -> usize{
    let mut queue = LinkedList::new();
    queue.push_back(("start".to_string(), vec!["start".to_string()]));
    let mut count = 0;
    while !queue.is_empty() {
        let (cave_id, path) = queue.pop_front().unwrap();
        if cave_id == "end" {
            //println!("{:?}", path);
            count += 1;
        } else {
            for adjecent in map.get(&cave_id).unwrap_or(&Vec::new()) {
                let mut p = path.clone();
                p.push(adjecent.clone());
                if is_acceptable(&p) {
                    queue.push_back((adjecent.to_string(), p));      
                }
            }
        }
    }
    count
}

fn main() {
    let map = parse(io::stdin());
    let count = search(&map);
    println!("{}", count);
}