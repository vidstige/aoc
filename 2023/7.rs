use std::cmp::Ordering;
use std::io::{self, BufRead};
use std::str::FromStr;

use itertools::enumerate;

type Card = u8;

#[derive(Eq, Debug)]
struct Hand {
    cards: [Card; 5],
}

impl Hand {
    fn kind(&self) -> i32 {
        let mut counts: [u8; 13] = [0; 13];
        for card in self.cards {
            counts[card as usize] += 1;
        }
        // we don't care which card value has what count, just the counts
        counts.sort();
        counts.reverse();
        if counts[0] == 5 { return 6;} // five of a kind
        if counts[0] == 4 { return 5; } // four of a kind
        if counts[0] == 3 && counts[1] == 2 { return 4; } // full house
        if counts[0] == 3 { return 3; } // three of a kind
        if counts[0] == 2 && counts[1] == 2 { return 2; } // two pars
        if counts[0] == 2 { return 1; } // pair
        0  // high card
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> Ordering {
        (self.kind(), self.cards).cmp(&(other.kind(), other.cards))
    }
}


impl PartialEq for Hand {
    fn eq(&self, other: &Self) -> bool {
        self.cards == other.cards
    }
}

#[derive(Debug, PartialEq, Eq)]
struct ParseHandError;

impl FromStr for Hand {
    type Err = ParseHandError;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let values = "23456789TJQKA";
        let cards: Vec<_> = s.chars().map(|card| values.chars().position(|c| c == card).unwrap() as u8).collect();
        Ok(Hand{cards: [cards[0], cards[1], cards[2], cards[3], cards[4]]})
    }
}

fn parse_line(s: &str) -> (Hand, i32) {
    let mut parts = s.split_whitespace();
    let hand: Hand = parts.next().unwrap().parse().unwrap();
    let bid: i32 = parts.next().unwrap().parse().unwrap();
    (hand, bid)
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();

    let mut data: Vec<_> = lines.map(|line| line.unwrap()).map(|line| parse_line(&line)).collect();

    data.sort();
    let mut total = 0;
    for (index, (hand, bid)) in data.iter().enumerate() {
        let rank = (index + 1) as i32;
        total += rank * bid; 
        //println!("{:?} {} {}", hand, hand.kind(), bid);
    }
    println!("{}", total);

}