use std::collections::{HashMap, HashSet, VecDeque};

use itertools::Itertools;

fn main() {
    println!("A: {}", solve_a("inputs/day5.txt"));
    println!("B: {}", solve_b("inputs/day5.txt"));
}

fn solve_a(filename: &str) -> u32 {
    let puzzle = parse(filename);
    let mut sum = 0;
    for update in &puzzle.updates {
        if puzzle.is_okay(update) {
            sum += update[update.len() / 2];
        }
    }
    sum
}

fn solve_b(filename: &str) -> u32 {
    let puzzle = parse(filename);
    let mut sum = 0;
    for update in &puzzle.updates {
        if !puzzle.is_okay(update) {
            let fixed = &puzzle.topo_sort(&update);
            sum += fixed[fixed.len() / 2];
        }
    }
    sum
}

#[derive(Debug, Default)]
struct Puzzle {
    partial_order: HashSet<(u32, u32)>,
    updates: Vec<Vec<u32>>,
}

impl Puzzle {
    fn is_okay(&self, update: &[u32]) -> bool {
        for i in 0..update.len() {
            for j in i..update.len() {
                if self.partial_order.contains(&(update[j], update[i])) {
                    return false;
                }
            }
        }

        true
    }

    fn topo_sort(&self, update: &[u32]) -> Vec<u32> {
        let has = update.iter().copied().collect::<HashSet<_>>();

        // 1 -> { 2, 3 } etc
        let mut precedes: HashMap<u32, HashSet<u32>> = HashMap::default();
        for (left, right) in &self.partial_order {
            if has.contains(left) && has.contains(right) {
                precedes.entry(*left).or_default().insert(*right);
                precedes.entry(*right).or_default();
            }
        }

        let mut correct_order: VecDeque<u32> = VecDeque::default();
        while !precedes.is_empty() {
            let k = precedes
                .iter()
                .find_map(|(k, v)| if v.is_empty() { Some(*k) } else { None })
                .expect(&format!("fail: {:?}\n\n{:?}", &precedes, &correct_order));

            for v in precedes.values_mut() {
                v.remove(&k);
            }

            precedes.remove(&k);

            correct_order.push_front(k);
        }

        correct_order.into()
    }
}

fn parse(filename: &str) -> Puzzle {
    let str = std::fs::read_to_string(filename).unwrap();
    let mut lines = str.lines();

    let mut puzzle = Puzzle::default();

    // partial_order
    loop {
        let line = lines.next().unwrap();
        if line.is_empty() {
            break;
        }
        let (left, right) = line.split("|").collect_tuple().unwrap();

        puzzle
            .partial_order
            .insert((left.parse::<u32>().unwrap(), right.parse::<u32>().unwrap()));
    }

    // updates
    loop {
        let Some(line) = lines.next() else {
            break;
        };

        let update = line.split(",").map(|s| s.parse().unwrap()).collect();
        puzzle.updates.push(update);
    }

    puzzle
}
