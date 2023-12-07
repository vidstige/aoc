use std::cmp::Ordering;
use std::io::{self, BufRead};
use std::str::FromStr;

type Card = u8;

#[derive(Eq, Debug)]
struct Hand {
    cards: [Card; 5],
}

enum Kind {
    HighCard,
    Pair,
    TwoPairs,
    ThreeOfAKind,
    FullHouse,
    FourOfAKind,
    FiveOfAKind,
}

impl Hand {
    fn kind(&self) -> Kind {
        let mut counts: [u8; 13] = [0; 13];
        for card in self.cards {
            counts[card as usize] += 1;
        }
        // we don't care which card value has what count, just the counts
        counts.sort();
        counts.reverse();
        // check top two counts
        match (counts[0], counts[1]) {
            (5, _) => Kind::FiveOfAKind,
            (4, _) => Kind::FourOfAKind,
            (3, 2) => Kind::FullHouse,
            (3, _) => Kind::ThreeOfAKind,
            (2, 2) => Kind::TwoPairs,
            (2, _) => Kind::Pair,
            (_, _) => Kind::HighCard,
        }
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> Ordering {
        (self.kind() as isize, self.cards).cmp(&(other.kind() as isize, other.cards))
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

fn parse_line(s: &str) -> (Hand, usize) {
    let mut parts = s.split_whitespace();
    let hand: Hand = parts.next().unwrap().parse().unwrap();
    let bid: usize = parts.next().unwrap().parse().unwrap();
    (hand, bid)
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();

    let mut data: Vec<_> = lines.map(|line| line.unwrap()).map(|line| parse_line(&line)).collect();
    // sort by hand (and bid)
    data.sort();
    // fetch bids
    let bids: Vec<_> = data.iter().map(|(_, bid)| bid).collect();
    let total: usize = bids.iter().enumerate().map(|(index, bid)| (index + 1) * *bid).sum();
    println!("{}", total);

}