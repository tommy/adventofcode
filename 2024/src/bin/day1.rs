use std::fs;

use regex::Regex;

fn main() {
    println!("{}", solve_a("inputs/day1a.txt"));
}

fn solve_a(filename: &str) -> u32 {
    let input = fs::read_to_string(filename).expect("Failed to read file");
    let pattern = Regex::new(r"(\d+)\s+(\d+)").unwrap();
    let mut lefts = Vec::new();
    let mut rights = Vec::new();
    for line in input.lines() {
        let groups = pattern.captures(line).unwrap();
        lefts.push(groups.get(1).unwrap().as_str().parse::<i32>().unwrap());
        rights.push(groups.get(2).unwrap().as_str().parse::<i32>().unwrap());
    }

    lefts.sort();
    rights.sort();

    lefts
        .iter()
        .zip(rights.iter())
        .map(|(left, right)| left.abs_diff(*right))
        .sum()
}
