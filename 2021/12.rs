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
                if is_big(adjecent) || !path.contains(adjecent) {
                    let mut p = path.clone();
                    p.push(adjecent.clone());
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