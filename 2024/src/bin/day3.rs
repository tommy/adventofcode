use std::{fs, iter::Peekable};

fn main() {
    println!("A: {}", solve_a("inputs/day3.txt"));
}

fn solve_a(filename: &str) -> i32 {
    let muls = parse(filename);
    muls.into_iter().map(|(x, y)| x * y).sum()
}

#[derive(Debug)]
enum State {
    Start,
    Mul,
    MulX(i32),
    End,
}

fn parse(filename: &str) -> Vec<(i32, i32)> {
    let contents = fs::read_to_string(filename).expect("Something went wrong reading the file");

    let mut chars = contents.chars().peekable();
    let mut state = State::Start;
    let mut exprs = Vec::new();

    loop {
        match state {
            State::End => {
                break;
            }

            _ if chars.peek().is_none() => {
                state = State::End;
            }

            State::Start => {
                // consumes the string if matches
                if match_string(&mut chars, "mul(") {
                    state = State::Mul;
                }
                // otherwise skip the invalid character
                else {
                    chars.next();
                }
            }

            State::Mul => {
                if let Some(x) = match_number(&mut chars) {
                    if match_char(&mut chars, ',') {
                        state = State::MulX(x);
                    } else {
                        state = State::Start;
                        chars.next();
                    }
                } else {
                    state = State::Start;
                    chars.next();
                }
            }

            State::MulX(x) => {
                if let Some(y) = match_number(&mut chars) {
                    if match_char(&mut chars, ')') {
                        exprs.push((x, y));
                    } else {
                        chars.next();
                    }
                    state = State::Start;
                } else {
                    state = State::Start;
                    chars.next();
                }
            }
        }
    }

    exprs
}

fn match_char<I: Iterator<Item = char>>(chars: &mut Peekable<I>, c: char) -> bool {
    if chars.peek() == Some(&c) {
        chars.next();
        true
    } else {
        false
    }
}

fn match_string<I: Iterator<Item = char>>(chars: &mut Peekable<I>, s: &str) -> bool {
    for c in s.chars() {
        if !match_char(chars, c) {
            return false;
        }
    }
    true
}

fn match_number<I: Iterator<Item = char>>(chars: &mut Peekable<I>) -> Option<i32> {
    if !chars.peek().map_or(false, char::is_ascii_digit) {
        return None;
    }

    let mut num = 0;
    while let Some(c) = chars.next_if(char::is_ascii_digit) {
        num = num * 10 + c.to_digit(10).unwrap() as i32;
    }

    Some(num)
}
