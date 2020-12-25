use std::env;

fn search(n: i128, subject: i128, public_key: i128) -> i128 {
    let mut value: i128 = 1;
    for secret in 1..n {
        value = value * subject % 20201227;
        if value == public_key {
            return secret;
        }
    }
    -1
}
fn encrypt(subject: i128, secret: i128) -> i128 {
    let mut value: i128 = 1;
    for _ in 0..secret {
        value = value * subject % 20201227;
    }
    value
}

fn main() {
    let args: Vec<String> = env::args().collect();

    // example
    //let (pub_door, pub_card): (i128, i128) = (5764801, 17807724);
    // input
    let (pub_door, pub_card): (i128, i128) = (16616892, 14505727);
    let n: i128 = args[1].parse().unwrap();
    let private_door = search(n, 7, pub_door);
    let private_card  = search(n, 7, pub_card);
    println!("{} {}", private_door, private_card);
    println!("{}", encrypt(pub_door, private_card));
    println!("{}", encrypt(pub_card, private_door));
}