use std::convert::TryInto;
use std::io::{self, BufRead};
use std::ops::{RangeInclusive};
use std::{str::FromStr, num::ParseIntError};
use regex::{Regex, Captures};

type Point = (i32, i32);

struct RangeSet<T> where T: Clone+PartialOrd {
    include: Vec<RangeInclusive<T>>,
    exclude: Vec<T>,
}

fn sub(a: &i32, b: &i32) -> usize {
    (a - b).try_into().unwrap()
}

impl RangeSet<i32>  {
    fn new() -> RangeSet<i32>{
        RangeSet{include: Vec::new(), exclude: Vec::new()}
    }
    /*fn contains(&self, item: &i32) -> bool {
        self.include.iter().any(|range| range.contains(item) && !self.exclude.contains(item))
    }*/
    fn len(&self) -> usize {
        let lo = self.include.iter().map(|r| r.start()).min().unwrap();
        let hi = self.include.iter().map(|r| r.start()).max().unwrap();
        let mut tmp = vec![false; sub(hi, lo)];
        for range in &self.include {
            for i in range.clone() {
                tmp[sub(&i, lo)] = true;
            }
        }
        for i in &self.exclude {
            tmp[sub(i, lo)] = false;
        }
        tmp.iter().filter(|i| **i).count()
    }
    fn extend(&mut self, range: &RangeInclusive<i32>) {
        self.include.push((*range).clone());
    }
    fn remove(&mut self, index: &i32) {
        self.exclude.push(*index);
    }
}

fn group_as<T, E>(captures: &Captures, index: usize) -> Result<T, E> where T: FromStr<Err = E> {
    captures.get(index).unwrap().as_str().parse()
}

fn manhattan((ax, ay): &Point, (bx, by): &Point) -> i32 {
    (bx - ax).abs() + (by - ay).abs()
}

struct Sensor {
    position: Point,
    beacon: Point,
}

impl FromStr for Sensor {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let re = Regex::new(r"^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)$").unwrap();
        let captures = re.captures(s).unwrap();
        let sx: i32 = group_as(&captures, 1)?;
        let sy: i32 = group_as(&captures, 2)?;
        let bx: i32 = group_as(&captures, 3)?;
        let by: i32 = group_as(&captures, 4)?;
        Ok(Sensor {position: (sx, sy), beacon: (bx, by)})
    }
}

fn fill(grid: &mut RangeSet<i32>, sensor: &Sensor, y: i32) {
    let (px, py) = sensor.position;
    let d = manhattan(&sensor.position, &sensor.beacon);
    assert!(d >= 0);
    let r = d - (py - y).abs();
    //println!("r: {r}, p: ({px}, {py}), d: {d}");
    grid.extend(&((px - r)..=(px + r)));
}

fn part_one(sensors: &Vec<Sensor>, search_y: i32) -> usize {
    let mut grid = RangeSet::new();
    for sensor in sensors {
        fill(&mut grid, sensor, search_y);
    }
    for (bx, by) in sensors.iter().map(|sensor| sensor.beacon) {
        if by == search_y {
            grid.remove(&bx);
        }
    }
    grid.len()
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());    
    let sensors: Vec<Sensor> = lines.map(|line| line.parse().unwrap()).collect();
    
    println!("{}", part_one(&sensors, 2000000));
}