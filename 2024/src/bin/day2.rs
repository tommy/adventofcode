use std::fs;

use itertools::Itertools;

fn main() {
    println!("A: {}", solve_a("inputs/day2.txt"));
}

fn solve_a(filename: &str) -> usize {
    let reports = parse(filename);
    reports.iter().filter(|report| is_safe(report)).count()
}

fn is_safe(report: &[i32]) -> bool {
    let asc = report.is_sorted_by(|a, b| a < b);
    let desc = report.is_sorted_by(|a, b| a > b);

    (asc || desc)
        && report.iter().zip(report.iter().skip(1)).all(|(a, b)| {
            let diff = a.abs_diff(*b);
            (1..=3).contains(&diff)
        })
}

fn parse(filename: &str) -> Vec<Vec<i32>> {
    let input = fs::read_to_string(filename).expect("Failed to read file");
    let mut reports = Vec::new();
    for line in input.lines() {
        reports.push(
            line.split(char::is_whitespace)
                .map(|s| s.parse::<i32>().unwrap())
                .collect_vec(),
        );
    }

    reports
}
