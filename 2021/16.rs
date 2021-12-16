use std::io::{self, BufRead};

struct BitStream {
    bytes: Vec<u8>,
    position: usize, // bit position
}

impl BitStream {
    fn read_bit(&mut self) -> Option<u8> {
        if self.position / 8 >= self.bytes.len() {
            return None;
        }
        let byte = self.bytes[self.position / 8];
        let value = (byte >> (7 - self.position % 8)) & 1;
        self.position += 1;
        Some(value)
    }
    fn read_bits(&mut self, size: u8) -> u32 {
        let mut a: u32 = 0;
        for i in 0..size {
            let m = 1 << (size - i - 1);
            a += m * self.read_bit().unwrap() as u32;
        }
        a
    }
}

fn hex(chars: &[char]) -> u8 {
    16 * chars[0].to_digit(16).unwrap() as u8 + chars[1].to_digit(16).unwrap() as u8
}

fn as_bitstream(packet: String) -> BitStream {
    let chars: Vec<_> = packet.chars().collect();
    BitStream {
        bytes: chars.chunks(2).map(hex).collect(),
        position: 0,
    }
}

fn parse(stream: &mut BitStream) -> u64 {
    let _version = stream.read_bits(3);
    let t = stream.read_bits(3);
    if t == 4 {
        // literal
        let mut groups = Vec::new();
        while {
            let cont = stream.read_bit();
            let group = stream.read_bits(4);
            groups.push(group);
            cont.unwrap_or(0) > 0
        } { }
        let mut value: u64 = 0;
        for (i, group) in groups.iter().enumerate() {
            let m = 1 << ((groups.len() - i - 1) * 4);
            value += m * *group as u64;
        }
        return value;
    } else {
        let length_type = stream.read_bit().unwrap();
        let mut values = Vec::new();
        if length_type == 0 {
            let length = stream.read_bits(15) as usize;
            let before = stream.position;
            while stream.position - before < length {
                values.push(parse(stream));
            }
        } else {
            let count = stream.read_bits(11);
            for _ in 0..count {
                values.push(parse(stream));
            }
        }
        return match t {
            0 => values.iter().sum(),
            1 => values.iter().product(),
            2 => *values.iter().min().unwrap(),
            3 => *values.iter().max().unwrap(),
            5 => if values[0] > values[1] { 1 } else { 0 },
            6 => if values[0] < values[1] { 1 } else { 0 },
            7 => if values[0] == values[1] { 1 } else { 0 }
            _ => panic!(),
        }
    }
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock()
        .lines()
        .map(|line| line.unwrap());

    for line in lines {
        let v = parse(&mut as_bitstream(line));
        println!("{}", v);
    }
}