use std::fs;

fn main() {
    println!("A: {}", solve_a("inputs/day2.txt"));
    println!("B: {}", solve_b("inputs/day2.txt"));
}

fn solve_a(filename: &str) -> usize {
    let reports = parse(filename);
    reports.iter().filter(|r| r.is_safe()).count()
}

fn solve_b(filename: &str) -> usize {
    let reports = parse(filename);
    reports
        .iter()
        .filter(|r| r.is_safe_with_dampening())
        .count()
}

impl Report {
    fn is_safe(&self) -> bool {
        let asc = self.levels.is_sorted_by(|a, b| a < b);
        let desc = self.levels.is_sorted_by(|a, b| a > b);

        (asc || desc)
            && self
                .levels
                .iter()
                .zip(self.levels.iter().skip(1))
                .all(|(a, b)| {
                    let diff = a.abs_diff(*b);
                    (1..=3).contains(&diff)
                })
    }

    fn dampened(&self) -> Vec<Report> {
        let mut dampened_reports = Vec::new();
        for i in 0..self.levels.len() {
            let mut levels = self.levels.clone();
            levels.remove(i);
            dampened_reports.push(Report { levels });
        }
        dampened_reports
    }

    fn is_safe_with_dampening(&self) -> bool {
        self.is_safe() || self.dampened().iter().any(|r| r.is_safe())
    }
}

struct Report {
    levels: Vec<i32>,
}

impl FromIterator<i32> for Report {
    fn from_iter<I: IntoIterator<Item = i32>>(iter: I) -> Self {
        Report {
            levels: iter.into_iter().collect(),
        }
    }
}

fn parse(filename: &str) -> Vec<Report> {
    let input = fs::read_to_string(filename).expect("Failed to read file");
    let mut reports = Vec::new();
    for line in input.lines() {
        reports.push(
            line.split(char::is_whitespace)
                .map(|s| s.parse::<i32>().unwrap())
                .collect(),
        );
    }

    reports
}
