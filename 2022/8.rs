use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet};
use std::cmp;
use std::ops::Range;
use std::fmt::Debug;

type Grid<T> = HashMap<(i32, i32), T>;

fn parse_grid() -> Grid<usize> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    let mut grid = Grid::new();
    for (y, line) in lines.enumerate() {
        for (x, c) in line.chars().enumerate() {
            let height = c.to_digit(16).unwrap() as usize;
            grid.insert((x as i32, y as i32), height);
        }
    }
    grid
}

fn xrange<T>(grid: &Grid<T>) -> Range<i32> {
    let xs: Vec<_> = grid.keys().map(|(x, _)| *x).collect();
    let xmin = *xs.iter().min().unwrap();
    let xmax = *xs.iter().max().unwrap();
    xmin..xmax + 1
}

fn yrange<T>(grid: &Grid<T>) -> Range<i32> {
    let ys: Vec<_> = grid.keys().map(|(x, _)| *x).collect();
    let ymin = *ys.iter().min().unwrap();
    let ymax = *ys.iter().max().unwrap();
    ymin..ymax + 1
}

fn print_grid<T>(grid: &Grid<T>) where T: Debug {
    println!("----------");
    for y in yrange(&grid) {
        for x in xrange(&grid) {
            print!("{:?}", grid[&(x, y)]);
        }
        println!("");
    }
}
fn print_bool_grid(grid: &Grid<bool>) {
    println!("----------");
    for y in yrange(&grid) {
        for x in xrange(&grid) {
            print!("{}", if grid[&(x, y)] {'.'} else { ' ' });
        }
        println!("");
    }
}

fn visible_positions(grid: &Grid<bool>) -> Vec<(i32, i32)> {
    grid.iter().filter_map(|(p, visible)| match visible {
        true => Some(*p),
        false => None
    }).collect()
}

fn part_one(grid: &Grid<u32>) -> usize {
    // from left
    let mut left = Grid::new();
    for y in yrange(&grid) {
        let mut tallest = 0;
        for x in xrange(&grid) {
            let h = grid[&(x, y)];
            left.insert((x, y), h > tallest);
            tallest = cmp::max(tallest, h);
        }
    }
    print_bool_grid(&left);

    // from right
    let mut right = Grid::new();
    for y in yrange(&grid) {
        let mut tallest = 0;
        for x in xrange(&grid).rev() {
            let h = grid[&(x, y)];
            right.insert((x, y), h > tallest);
            tallest = cmp::max(tallest, h);
        }
    }
    print_bool_grid(&right);

    // from top
    let mut top = Grid::new();
    for x in xrange(&grid) {
        let mut tallest = 0;
        for y in yrange(&grid) {
            let h = grid[&(x, y)];
            top.insert((x, y), h > tallest);
            tallest = cmp::max(tallest, h);
        }
    }
    print_bool_grid(&top);

    // from below
    let mut below = Grid::new();
    for x in xrange(&grid) {
        let mut tallest = 0;
        for y in yrange(&grid).rev() {
            let h = grid[&(x, y)];
            below.insert((x, y), h > tallest);
            tallest = cmp::max(tallest, h);
        }
    }
    print_bool_grid(&below);

    let mut positions: HashSet<(i32, i32)> = HashSet::new();

    positions.extend(visible_positions(&left));
    positions.extend(visible_positions(&right));
    positions.extend(visible_positions(&top));
    positions.extend(visible_positions(&below));
    
    positions.len()
}

fn main() {
    let grid = parse_grid();
    //print_grid(&grid);
    

    //println!("{}", part_one(&grid));
    
    let mut left: Grid<i32> = Grid::new();
    for y in yrange(&grid) {
        // how many trees of hight n is visible
        let mut counter: [i32; 10] = [0; 10];
        for x in xrange(&grid) {
            let h = grid[&(x, y)];
            left.insert((x, y), counter[h]);
            for i in 0..h+1 {
                counter[i] = 0;
            }
            for i in 0..10 {
                counter[i] += 1;
            }
        }
    }
    //print_grid(&left);

    // from right
    let mut right: Grid<i32> = Grid::new();
    for y in yrange(&grid) {
        // how many trees of hight n is visible
        let mut counter: [i32; 10] = [0; 10];
        for x in xrange(&grid).rev() {
            let h = grid[&(x, y)];
            right.insert((x, y), counter[h]);
            for i in 0..h+1 {
                counter[i] = 0;
            }
            for i in 0..10 {
                counter[i] += 1;
            }

        }
    }
    //print_grid(&right);

    // from top
    let mut top: Grid<i32> = Grid::new();
    for x in xrange(&grid) {
        // how many trees of hight n is visible
        let mut counter: [i32; 10] = [0; 10];
        for y in yrange(&grid) {
            let h = grid[&(x, y)];
            top.insert((x, y), counter[h]);
            for i in 0..h+1 {
                counter[i] = 0;
            }
            for i in 0..10 {
                counter[i] += 1;
            }
        }
    }
    //print_grid(&top);

    // from below
    let mut below: Grid<i32> = Grid::new();
    for x in xrange(&grid) {
        // how many trees of hight n is visible
        let mut counter: [i32; 10] = [0; 10];
        for y in yrange(&grid).rev() {
            let h = grid[&(x, y)];
            below.insert((x, y), counter[h]);
            for i in 0..h+1 {
                counter[i] = 0;
            }
            for i in 0..10 {
                counter[i] += 1;
            }
        }
    }
    //print_grid(&below);

    let mut scores = Grid::new();
    for x in xrange(&grid) {
        for y in yrange(&grid) {
            let p = (x, y);
            let score = left[&p] * right[&p] * top[&p] * below[&p];
            scores.insert(p, score);
        }
    }
    //print_grid(&scores);

    println!("{}", scores.values().max().unwrap());
}