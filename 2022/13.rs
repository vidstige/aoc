use std::io::{self, BufRead};
use std::str::FromStr;
use std::iter;
use std::fmt;

#[derive(Clone)]
enum Item {
    List(Vec<Item>),
    Literal(u32),
}

impl Eq for Item {
    
}
impl PartialEq for Item {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (Self::Literal(lhs), Self::Literal(rhs)) => lhs == rhs,
            (Self::Literal(_), Self::List(rhs)) => iter::once(self).eq(rhs),
            (Self::List(lhs), Self::Literal(_)) => lhs.iter().eq(iter::once(other)),
            (Self::List(lhs), Self::List(rhs)) => lhs.iter().eq(rhs.iter()),
        }
    }
}

impl PartialOrd for Item {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        match self {
            Item::Literal(a) => match other {
                Item::Literal(b) => a.partial_cmp(&b),
                Item::List(b) => iter::once(self).partial_cmp(b.iter()),
            }
            Item::List(a) => match other {
                Item::Literal(_) => a.iter().partial_cmp(iter::once(other)),
                Item::List(b) => a.iter().partial_cmp(b.iter()),
            }
        }
    }
}

fn parse_literal(chars: &Vec<char>, index: &mut usize) -> Result<Item, String> {
    let start = *index;
    while *index < chars.len() && chars[*index].to_digit(10).is_some() {
        *index += 1;
    }
    if let Ok(literal) = chars[start..*index].iter().collect::<String>().parse() {
        return Ok(Item::Literal(literal))
    }
    Err(format!("Could not parse literal {}-{}", start, *index))
}

fn parse_list(chars: &Vec<char>, index: &mut usize) -> Result<Item, String> {
    let mut tmp = Vec::new();
    while chars[*index] != ']' {
        let item_result = parse_item(chars, index);
        if let Ok(item) = item_result {
            tmp.push(item);
        } else {
            return item_result;
        }
        if chars[*index] == ',' {
            *index += 1; // consume ','
        }
    }
    *index += 1; // consume the ']'
    return Ok(Item::List(tmp));
}

fn parse_item(chars: &Vec<char>, index: &mut usize) -> Result<Item, String> {
    if chars[*index].to_digit(10).is_some() {
        return parse_literal(&chars, index);
    }
    if chars[*index] == '[' {
        *index += 1;
        return parse_list(&chars, index);
    }
    return Err(format!("Expected '[' or 0-9 at {index}"));
}

impl FromStr for Item {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let chars: Vec<_> = s.chars().collect();
        let mut index = 0;
        return parse_item(&chars, &mut index);
    }
}

impl fmt::Display for Item {
    fn fmt(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        match self {
            Item::Literal(value) => write!(formatter, "{}", value),
            Item::List(list) => {
                write!(formatter, "[")?;
                let mut first = true;
                for item in list {
                    if !first {
                        write!(formatter, ",")?;
                    }
                    first = false;
                    item.fmt(formatter)?;
                }
                write!(formatter, "]")
            },
        }
    }
}

fn parse() -> usize {
    let stdin = io::stdin();
    let lines: Vec<_> = stdin.lock().lines().map(|line| line.unwrap()).collect();

    lines.chunks(3).enumerate().filter_map(|(index, chunk)| {
        let a: Item = chunk[0].parse().unwrap();
        let b: Item = chunk[1].parse().unwrap();
        if a.le(&b) {
            Some(index + 1)
        } else {
            None
        }
    }).sum()
}


fn main() {
    let answer = parse();
    println!("{}", answer);
}
