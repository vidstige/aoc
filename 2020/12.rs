use std::io::{self, BufRead};
use std::str::FromStr;

#[derive(Debug, PartialEq, Copy, Clone)]
enum CardinalDirection {N, S, E, W}
enum RelativeDirection {Left, Right}

enum Instruction {
    Move(CardinalDirection, i32),
    Turn(RelativeDirection, i32),
    Forward(i32)
}

impl FromStr for Instruction {
    type Err = ();
    fn from_str(input: &str) -> Result<Instruction, Self::Err> {
        let movement_str: String = input.chars().take(1).collect();
        let value_str: String = input.chars().skip(1).collect();
        let value: i32 = value_str.parse().unwrap();
        match movement_str.as_str() {
            "N" => Ok(Instruction::Move(CardinalDirection::N, value)),
            "S" => Ok(Instruction::Move(CardinalDirection::S, value)),
            "E" => Ok(Instruction::Move(CardinalDirection::E, value)),
            "W" => Ok(Instruction::Move(CardinalDirection::W, value)),
            "L" => Ok(Instruction::Turn(RelativeDirection::Left, value / 90)),
            "R" => Ok(Instruction::Turn(RelativeDirection::Right, value / 90)),
            "F" => Ok(Instruction::Forward(value)),
            _ => Err(())
        }
    }
}

use std::ops::Add;

#[derive(Debug, PartialEq, Copy, Clone)]
struct Vector(i32, i32);

impl Add for Vector {
    type Output = Self;

    fn add(self, other: Self) -> Self::Output {
        Self(self.0 + other.0, self.1 + other.1)
    }
}

fn delta(direction: CardinalDirection, distance: i32) -> Vector {
    match direction {
        CardinalDirection::N => Vector(0, -distance),
        CardinalDirection::S => Vector(0, distance),
        CardinalDirection::W => Vector(-distance, 0),
        CardinalDirection::E => Vector(distance, 0),
    }
}

fn turn(direction: CardinalDirection, rd: &RelativeDirection) -> CardinalDirection {
    match rd {
        RelativeDirection::Left => match direction {
            CardinalDirection::N => CardinalDirection::W,
            CardinalDirection::W => CardinalDirection::S,
            CardinalDirection::S => CardinalDirection::E,
            CardinalDirection::E => CardinalDirection::N,
        }
        RelativeDirection::Right => match direction {
            CardinalDirection::N => CardinalDirection::E,
            CardinalDirection::E => CardinalDirection::S,
            CardinalDirection::S => CardinalDirection::W,
            CardinalDirection::W => CardinalDirection::N,
        }
    }
}

fn turn_n(direction: CardinalDirection, rd: &RelativeDirection, turns: i32) -> CardinalDirection {
    let mut d = direction;
    for _ in 0..turns {
        d = turn(d, rd);
    }
    d
}

type Ship = (Vector, CardinalDirection);

fn update(ship: Ship, instruction: Instruction) -> Ship {
    let (position, ship_direction) = ship;
    match instruction {
        Instruction::Move(move_direction, distance) => 
            (position + delta(move_direction, distance), ship_direction),
        Instruction::Turn(rd, turns) =>
            (position, turn_n(ship_direction, &rd, turns)),
        Instruction::Forward(distance) => (position + delta(ship_direction, distance), ship_direction),
    }
}

fn manhattan(vector: Vector) -> i32 {
    vector.0.abs() + vector.1.abs()
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let instructions: Vec<Instruction> = lines.map(|line| line.unwrap().parse().unwrap()).collect();
    
    let mut ship = (Vector(0, 0), CardinalDirection::E);

    for instruction in instructions {
        //println!("{}", instruction.value);
        ship = update(ship, instruction);
        let (position, _) = ship;
        println!("{}, {}", position.0, position.1);
    }
    println!("{}", manhattan(ship.0))
}