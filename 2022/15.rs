use std::io::{self, BufRead};
use std::ops::Range;
use std::{str::FromStr, num::ParseIntError};
use regex::{Regex, Captures};

#[derive(Clone)]
struct RangeSet<T> where T: Clone+PartialOrd {
    include: Vec<Range<T>>,
    exclude: Vec<T>,
}

fn sub(a: i32, b: i32) -> usize {
    (a - b) as usize
}

fn overlaps<T>(a: &Range<T>, b: &Range<T>) -> bool where T: PartialOrd {
    a.start <= b.end && b.start <= a.end
}

// wether a completely contains b
fn contains<T>(a: &Range<T>, b: &Range<T>) -> bool where T: PartialOrd {
    a.contains(&b.start) && a.contains(&b.end)
}

impl RangeSet<i32>  {
    fn new() -> RangeSet<i32>{
        RangeSet{include: Vec::new(), exclude: Vec::new()}
    }
    /*fn contains(&self, item: &i32) -> bool {
        self.include.iter().any(|range| range.contains(item) && !self.exclude.contains(item))
    }*/
    fn full_range(&self) -> Range<i32> {
        let maybe_lo = self.include.iter().map(|r| r.start).min();
        let maybe_hi = self.include.iter().map(|r| r.end).max();
        match (maybe_lo, maybe_hi) {
            (Some(lo), Some(hi)) => lo..hi,
            _ => 0..0,
        }
        
    }
    fn dense(&self, full_range: &Range<i32>) -> Vec<bool>{
        let mut dense = vec![false; sub(full_range.end, full_range.start) + 1];
        for range in &self.include {
            for i in range.clone() {
                dense[sub(i, full_range.start)] = true;
            }
        }
        // TODO: i might be outside
        for i in &self.exclude {
            dense[sub(*i, full_range.start)] = false;
        }
        dense
    }
    fn undense(dense: Vec<bool>, lo: i32) -> Self {
        // collects dense representation into ranges again
        let mut set = RangeSet::new();
        let mut maybe_current = None;
        for (i, contains) in dense.iter().enumerate() {
            let index = i as i32 + lo;
            if *contains {
                if maybe_current.is_none() {
                    maybe_current = Some(index);
                }
            } else {
                if let Some(current) = maybe_current {
                    set.extend(&(current..index));
                }
                maybe_current = None;
            }
        }
        if let Some(current) = maybe_current {
            set.extend(&(current..dense.len() as i32 + lo));
        }
        set
    }
    fn len(&self) -> usize {
        let dense = self.dense(&self.full_range());
        dense.iter().filter(|i| **i).count()
    }
    fn extend(&mut self, range: &Range<i32>) {
        if !range.is_empty() {
            self.include.push((*range).clone());
        }
    }
    fn remove(&mut self, index: &i32) {
        self.exclude.push(*index);
    }
    fn difference(&self, rhs: &RangeSet<i32>) -> RangeSet<i32> {
        let mut stack = self.include.clone(); // intervals left to check
        let mut include = Vec::new(); // ok intervals
        
        while let Some(lhs_range) = stack.pop() {
            let mut dirty = false;
            if lhs_range.is_empty() {
                continue;
            }
            for rhs_range in &rhs.include {
                if contains(rhs_range, &lhs_range) {
                    // discard range
                    dirty = true;
                    break;
                } 
                if contains(&lhs_range, rhs_range) {
                    // we need to split this range
                    // aaaaaaaaaaaaa
                    //       bbbbb
                    // aaaaaa    aaa
                    stack.push(lhs_range.start..rhs_range.start-1);
                    stack.push(rhs_range.end..lhs_range.end);
                    dirty = true;
                    break;
                } else {
                    // check for right/left overlaps
                    if lhs_range.contains(&rhs_range.start) {
                        // move lhs end left if needed
                        stack.push(lhs_range.start..rhs_range.start);
                        dirty = true;
                        break; // keep going
                    }
                    if lhs_range.contains(&(rhs_range.end - 1)) {
                        // move lhs start right if needed
                        stack.push(rhs_range.end..lhs_range.end);
                        dirty = true;
                        break; // keep going
                    }
                }
            }
            if !dirty {
                include.push(lhs_range);
            }
        }
        
        RangeSet { include: include, exclude: self.exclude.clone() }
    }
    // poor mans iter
    fn items(&self) -> Vec<i32> {
        let full_range = self.full_range();
        let dense = self.dense(&full_range);
        dense
            .iter()
            .enumerate()
            .filter_map(|(index, contains)| contains.then(|| index as i32 + full_range.start))
            .collect()
    }
}

fn combine(a: &Range<i32>, b: &Range<i32>) -> Range<i32> {
    let start = a.start.min(b.start);
    let end = a.end.max(b.end);
    start..end
}

impl From<&[Range<i32>]> for RangeSet<i32> {
    fn from(slice: &[Range<i32>]) -> Self {
        RangeSet { include: slice.to_vec(), exclude: Vec::new() }
    }
}

type Point = (i32, i32);

fn manhattan((ax, ay): &Point, (bx, by): &Point) -> i32 {
    (bx - ax).abs() + (by - ay).abs()
}

struct Sensor {
    position: Point,
    beacon: Point,
}

fn group_as<T, E>(captures: &Captures, index: usize) -> Result<T, E> where T: FromStr<Err = E> {
    captures.get(index).unwrap().as_str().parse()
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

fn print_range_set(range_set: &RangeSet<i32>) {
    for range in &range_set.include {
        println!("{}-{}", range.start, range.end);
    }
}

fn print_dense_range_set(range_set: &RangeSet<i32>) {
    let full_range = range_set.full_range();
    let dense = range_set.dense(&full_range);
    for (index, contains) in dense.iter().enumerate() {
        println!("{}: {}", index as i32 + full_range.start, contains);
    }
}

fn fill(grid: &mut RangeSet<i32>, sensor: &Sensor, y: i32) {
    let (px, py) = sensor.position;
    let d = manhattan(&sensor.position, &sensor.beacon);
    assert!(d >= 0);
    let r = d - (py - y).abs();
    //println!("r: {r}, p: ({px}, {py}), d: {d}");
    grid.extend(&((px - r)..(px + r + 1)));
}

fn part_one(sensors: &Vec<Sensor>, search_y: i32) -> usize {
    let mut row = RangeSet::new();
    for sensor in sensors {
        fill(&mut row, sensor, search_y);
    }
    for (bx, by) in sensors.iter().map(|sensor| sensor.beacon) {
        if by == search_y {
            row.remove(&bx);
        }
    }
    //print_range_set(&row);
    //print_dense_range_set(&row);

    row.len()
}

fn tuning_frequency(x: i32, y: i32) -> i64 {
    x as i64 * 4000000 + y as i64
}

fn part_two(sensors: &Vec<Sensor>, n: i32) -> Option<i64> {
    for y in 0..=n {
        let mut row = RangeSet::new();
        for sensor in sensors {
            fill(&mut row, sensor, y);
        }
        let everything = RangeSet::from([0..n+1].as_slice());
        let tmp = everything.difference(&row);
        if let Some(x) = tmp.items().first() {
            return Some(tuning_frequency(*x, y));
        }
        //println!("y: {y}");
    }
    return None
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());    
    let sensors: Vec<Sensor> = lines.map(|line| line.parse().unwrap()).collect();
    
    //println!("{}", part_one(&sensors, 10));
    //println!("{:?}", part_two(&sensors, 20));
    println!("{}", part_one(&sensors, 2000000));
    println!("{:?}", part_two(&sensors, 4000000));
}