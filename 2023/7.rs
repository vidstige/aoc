use std::cmp::Ordering;
use std::io::{self, BufRead};
use std::str::FromStr;

const VALUES: &str = "23456789TJQKA";
const JOKER_VALUES: &str = "J23456789TQKA";

#[derive(Eq, Debug)]
struct Hand {
    cards: [char; 5],
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

trait Joker {
    
}
impl Hand {
    fn values(&self, values: &str) -> [usize; 5] {
        self.cards.map(|card| values.chars().position(|c| c == card).unwrap())
    }
    fn kind(&self, values: &str, joker: Option<char>) -> Kind {
        let joker = joker.and_then(|j| values.chars().position(|c| c == j));
        let mut counts: [u8; 13] = [0; 13];
        for card in self.values(values) {
            counts[card as usize] += 1;
        }
        let mut jokers = 0;
        if let Some(j) = joker {
            jokers = counts[j];
            counts[j] = 0;
        }
        // we don't care which card value has what count, just the counts
        counts.sort();
        counts.reverse();
        // check top two counts
        match (counts[0] + jokers, counts[1]) {
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
        let cards: Vec<_> = s.chars().collect();
        Ok(Hand{cards: [cards[0], cards[1], cards[2], cards[3], cards[4]]})
    }
}

fn parse_line(s: &str) -> (Hand, usize) {
    let mut parts = s.split_whitespace();
    let hand: Hand = parts.next().unwrap().parse().unwrap();
    let bid: usize = parts.next().unwrap().parse().unwrap();
    (hand, bid)
}

fn compare_hands(a: &Hand, b: &Hand, values: &str, joker: Option<char>) -> Ordering {
    (a.kind(values, joker) as isize, a.values(values)).cmp(&(b.kind(values, joker) as isize, b.values(values)))
}

fn winnings(data: &Vec<(Hand, usize)>) -> usize {
    data
        .iter().map(|(_, bid)| bid)  // fetch only bids
        .enumerate().map(|(index, bid)| (index + 1) * *bid)
        .sum()
}

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines();

    let mut data: Vec<_> = lines.map(|line| line.unwrap()).map(|line| parse_line(&line)).collect();

    // first star
    data.sort_unstable_by(|(a, _), (b, _)| compare_hands(a, b, VALUES, None));
    println!("{}", winnings(&data));

    // second star
    data.sort_unstable_by(|(a, _), (b, _)| compare_hands(a, b, JOKER_VALUES, Some('J')));
    println!("{}", winnings(&data));
}
