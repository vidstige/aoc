use std::io::{self, BufRead};
use std::str::FromStr;
use std::ops::{Add, Mul};

#[derive(Debug, PartialEq, Copy, Clone)]
struct Vector(i32, i32);

impl Add for Vector {
    type Output = Self;
    fn add(self, other: Self) -> Self::Output {
        Self(self.0 + other.0, self.1 + other.1)
    }
}
impl Mul<i32> for Vector {
    type Output = Self;
    fn mul(self, other: i32) -> Self::Output {
        Self(self.0 * other, self.1 * other)
    }
}

const NORTH: Vector = Vector(0, -1);
const EAST: Vector = Vector(1, 0);
const SOUTH: Vector = Vector(0, 1);
const WEST: Vector = Vector(-1, 0);

type Rotation = i32;

enum Instruction {
    MoveWaypoint(Vector),
    RotateWaypoint(Rotation),
    Forward(i32)
}

impl FromStr for Instruction {
    type Err = ();
    fn from_str(input: &str) -> Result<Instruction, Self::Err> {
        let movement_str: String = input.chars().take(1).collect();
        let value_str: String = input.chars().skip(1).collect();
        let value: i32 = value_str.parse().unwrap();
        match movement_str.as_str() {
            "N" => Ok(Instruction::MoveWaypoint(NORTH * value)),
            "E" => Ok(Instruction::MoveWaypoint(EAST * value)),
            "S" => Ok(Instruction::MoveWaypoint(SOUTH * value)),
            "W" => Ok(Instruction::MoveWaypoint(WEST * value)),
            "L" => Ok(Instruction::RotateWaypoint(value / 90)),
            "R" => Ok(Instruction::RotateWaypoint(-value / 90)),
            "F" => Ok(Instruction::Forward(value)),
            _ => Err(())
        }
    }
}

struct Ship {
    position: Vector,
    waypoint: Vector,
}

fn rotate(vector: Vector, r: Rotation) -> Vector {
    let mut v = vector;
    let rr = ((r % 4) + 4) % 4;
    for _ in 0..rr {
        v = Vector(v.1, -v.0)  // rotate left
    }
    v
}

fn update(ship: Ship, instruction: Instruction) -> Ship {
    match instruction {
        Instruction::MoveWaypoint(waypoint_delta) => Ship{
            position: ship.position,
            waypoint: ship.waypoint + waypoint_delta},
        Instruction::RotateWaypoint(rotation) => Ship{
            position: ship.position,
            waypoint: rotate(ship.waypoint, rotation)
        },
        Instruction::Forward(amount) => {
            Ship{
                position: ship.position + ship.waypoint * amount,
                waypoint: ship.waypoint,
            }
        }
    }
}

fn manhattan(vector: Vector) -> i32 {
    vector.0.abs() + vector.1.abs()
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();
    let instructions: Vec<Instruction> = lines.map(|line| line.unwrap().parse().unwrap()).collect();
    
    let mut ship = Ship{
        position: Vector(0, 0),
        waypoint: Vector(10, -1),
    };

    for instruction in instructions {
        //println!("{}", instruction.value);
        ship = update(ship, instruction);
        println!("{}, {}", ship.position.0, ship.position.1);
    }
    println!("{}", manhattan(ship.position))
}