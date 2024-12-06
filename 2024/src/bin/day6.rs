use std::collections::HashSet;

use itertools::Itertools;

fn main() {
    println!("A: {}", solve_a("inputs/day6.txt"));
    println!("B: {}", solve_b("inputs/day6-sample.txt"));
}

fn solve_a(filename: &str) -> usize {
    let mut puzzle = parse(filename);
    let mut seen_states: HashSet<(Dir, Loc)> = HashSet::new();
    let mut seen_locs: HashSet<Loc> = HashSet::new();
    while !seen_states.contains(&puzzle.guard_state()) {
        seen_locs.insert(puzzle.guard_loc);
        seen_states.insert(puzzle.guard_state());
        if puzzle.iterate().is_none() {
            break;
        };
    }

    seen_locs.len()
}

fn solve_b(filename: &str) -> u32 {
    let puzzle = parse(filename);
    0
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
enum Dir {
    Up,
    Down,
    Left,
    Right,
}

impl Dir {
    fn turn_right(&self) -> Self {
        use Dir::*;
        match self {
            Up => Right,
            Down => Left,
            Left => Up,
            Right => Down,
        }
    }
}

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq, PartialOrd, Ord)]
enum Tile {
    Free,
    Blocked,
}

type Loc = (usize, usize);

#[derive(Debug)]
struct Puzzle {
    grid: Vec<Vec<Tile>>,
    guard_loc: Loc,
    guard_dir: Dir,
}

impl Puzzle {
    fn guard_state(&self) -> (Dir, Loc) {
        (self.guard_dir, self.guard_loc)
    }

    fn oob(&self, r: i32, c: i32) -> bool {
        r < 0 || r >= self.grid.len() as i32 || c < 0 || c >= self.grid[0].len() as i32
    }

    /// Returns None if the next step is off the map
    #[must_use]
    fn iterate(&mut self) -> Option<()> {
        let (row, col) = self.next_cell(self.guard_dir, self.guard_loc)?;

        match self.grid[row][col] {
            Tile::Free => {
                self.guard_loc = (row, col);
            }
            Tile::Blocked => self.guard_dir = self.guard_dir.turn_right(),
        };

        Some(())
    }

    fn next_cell(&self, dir: Dir, loc: Loc) -> Option<Loc> {
        let (row, col) = (loc.0 as i32, loc.1 as i32);
        let (r, c) = match dir {
            Dir::Up => (row - 1, col),
            Dir::Down => (row + 1, col),
            Dir::Left => (row, col - 1),
            Dir::Right => (row, col + 1),
        };

        if self.oob(r, c) {
            None
        } else {
            Some((r as usize, c as usize))
        }
    }
}

fn parse(filename: &str) -> Puzzle {
    let input = std::fs::read_to_string(filename).unwrap();
    let mut grid = Vec::new();
    let mut guard_loc = None;
    let mut guard_dir = None;

    for (row, line) in input.lines().enumerate() {
        let grid_row = line
            .chars()
            .enumerate()
            .map(|(col, x)| match x {
                '.' => Tile::Free,
                '#' => Tile::Blocked,
                p => {
                    match p {
                        '^' => guard_dir = Some(Dir::Up),
                        '>' => guard_dir = Some(Dir::Right),
                        '<' => guard_dir = Some(Dir::Left),
                        'v' => guard_dir = Some(Dir::Down),
                        _ => panic!("wat"),
                    }
                    guard_loc = Some((row, col));
                    Tile::Free
                }
            })
            .collect_vec();
        grid.push(grid_row);
    }

    Puzzle {
        grid,
        guard_dir: guard_dir.unwrap(),
        guard_loc: guard_loc.unwrap(),
    }
}

#[test]
fn sample_a() {
    assert_eq!(solve_a("inputs/day6-sample.txt"), 41);
}
