use std::fs;

use itertools::Itertools as _;
use regex::Regex;

fn main() {
    println!("A: {}", solve_a("inputs/day1.txt"));
    println!("B: {}", solve_b("inputs/day1.txt"));
}

fn solve_a(filename: &str) -> u32 {
    let (mut lefts, mut rights) = parse(filename);

    lefts.sort();
    rights.sort();

    lefts
        .iter()
        .zip(rights.iter())
        .map(|(left, right)| left.abs_diff(*right))
        .sum()
}

fn solve_b(filename: &str) -> i32 {
    let (lefts, rights) = parse(filename);

    let counts = rights.iter().counts();
    lefts
        .into_iter()
        .map(|left| left * counts.get(&left).copied().unwrap_or_default() as i32)
        .sum()
}

fn parse(filename: &str) -> (Vec<i32>, Vec<i32>) {
    let input = fs::read_to_string(filename).expect("Failed to read file");
    let pattern = Regex::new(r"(\d+)\s+(\d+)").unwrap();
    let mut lefts = Vec::new();
    let mut rights = Vec::new();
    for line in input.lines() {
        let groups = pattern.captures(line).unwrap();
        lefts.push(groups.get(1).unwrap().as_str().parse::<i32>().unwrap());
        rights.push(groups.get(2).unwrap().as_str().parse::<i32>().unwrap());
    }

    (lefts, rights)
}
