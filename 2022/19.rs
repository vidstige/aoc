use std::io::{self, BufRead};
use std::num::ParseIntError;
use std::str::FromStr;
use std::collections::VecDeque;
use regex::{Regex, Captures};

fn group_as<T, E>(captures: &Captures, index: usize) -> Result<T, E> where T: FromStr<Err = E> {
    captures.get(index).unwrap().as_str().parse()
}

#[derive(Clone, Debug)]
struct State {
    ore: i32,
    clay: i32,
    obsidian: i32,
    geode: i32,
}
impl State {
    fn new() -> State {
        State{ore: 0, clay: 0, obsidian: 0, geode: 0}
    }
    fn ore(&self, ore: i32) -> State {
        State{ore: self.ore + ore, clay: self.clay, obsidian: self.obsidian, geode: self.geode}
    }
    fn clay(&self, clay: i32) -> State {
        State{ore: self.ore, clay: self.clay + clay, obsidian: self.obsidian, geode: self.geode}
    }
    fn obsidian(&self, obsidian: i32) -> State {
        State{ore: self.ore, clay: self.clay, obsidian: self.obsidian + obsidian, geode: self.geode}
    }
    fn geode(&self, geode: i32) -> State {
        State{ore: self.ore, clay: self.clay, obsidian: self.obsidian, geode: self.geode + geode}
    }
    fn sub(&self, rhs: &State) -> State {
        State {
            ore: self.ore - rhs.ore,
            clay: self.clay - rhs.clay,
            obsidian: self.obsidian - rhs.obsidian,
            geode: self.geode - rhs.obsidian
        }
    }
    fn add(&self, rhs: State) -> State {
        State {
            ore: self.ore + rhs.ore,
            clay: self.clay + rhs.clay,
            obsidian: self.obsidian + rhs.obsidian,
            geode: self.geode + rhs.obsidian
        }
    }
    fn is_positive(&self) -> bool {
        [self.ore, self.clay, self.obsidian, self.geode].iter().all(|x| x >= &0)
    }
}

struct Costs {
    ore: State,
    clay: State,
    obsidian: State,
    geode: State,
}

struct Blueprint {
    number: i32,
    costs: Costs,
}

impl FromStr for Blueprint {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"^Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.$").unwrap();
        let captures = re.captures(s).unwrap();
        let number = group_as::<_, ParseIntError>(&captures, 1)?;
        let costs = Costs{
            ore: State::new().ore(group_as::<_, ParseIntError>(&captures, 2)?),
            clay: State::new().ore(group_as::<_, ParseIntError>(&captures, 3)?),
            obsidian: State::new()
                .ore(group_as::<_, ParseIntError>(&captures, 4)?)
                .clay(group_as::<_, ParseIntError>(&captures, 5)?),
            geode: State::new()
                .ore(group_as::<_, ParseIntError>(&captures, 6)?)
                .obsidian(group_as::<_, ParseIntError>(&captures, 7)?),
        };
        Ok(Blueprint{number: number, costs: costs})
    }
}

fn edges(costs: &Costs, resources: &State) -> Vec<(State, State)> {
    let mut result = Vec::new();
    let options = [
        (State::new(), &State::new()), // do nothing
        (State::new().ore(1), &costs.ore), 
        (State::new().clay(1), &costs.clay), 
        (State::new().obsidian(1), &costs.obsidian), 
        (State::new().geode(1), &costs.geode),
    ];
    for (robots, cost) in options {
        if resources.sub(cost).is_positive() {
            result.push((robots, cost.clone()));
        }
    }
    result
}

fn gains(robots: &State) -> State {
    robots.clone() // gain one resource per robot
}

fn search(blueprint: &Blueprint) -> i32 {
    let mut queue = VecDeque::from([(State::new().ore(1), State::new(), 24)]);
    while let Some((robots, resources, time)) = queue.pop_front() {
        //println!("{time}: {robots:?} {resources:?}");
        if time == 0 {
            println!("{:?}, {}, {}", resources, time, queue.len());
            //return 1;
            continue;
        }
        for (robots_delta, resource_delta) in edges(&blueprint.costs, &resources) {
            //println!("deltas: {robots_delta:?} {resource_delta:?}");
            queue.push_front((robots.add(robots_delta), resources.sub(&resource_delta).add(gains(&robots)), time - 1));
        }
    }
    0
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    
    let blueprints: Vec<Blueprint> = lines.map(|line| line.parse().unwrap()).collect();
    
    for blueprint in blueprints {
        println!("{}", search(&blueprint));
    }
    
}