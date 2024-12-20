use itertools::Itertools;

fn main() {
    println!("A: {}", solve_a("inputs/day4.txt"));
    println!("B: {}", solve_b("inputs/day4.txt"));
}

fn solve_a(filename: &str) -> usize {
    let input = parse(filename);
    input.count_xmases()
}

fn solve_b(filename: &str) -> usize {
    let input = parse(filename);
    input.count_ex_mases()
}

#[derive(Debug)]
struct Puzzle {
    rows: Vec<Vec<char>>,
}

impl Puzzle {
    fn offsets() -> &'static [[(i32, i32); 4]] {
        &[
            // right, or left
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (0, -1), (0, -2), (0, -3)],
            // down, or up
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (-1, 0), (-2, 0), (-3, 0)],
            // down right, or up left
            [(0, 0), (1, 1), (2, 2), (3, 3)],
            [(0, 0), (-1, -1), (-2, -2), (-3, -3)],
            // up right, or down left
            [(0, 0), (-1, 1), (-2, 2), (-3, 3)],
            [(0, 0), (1, -1), (2, -2), (3, -3)],
        ]
    }

    fn indicies_from_here(&self, r: i32, c: i32) -> Vec<[(i32, i32); 4]> {
        let width = self.rows[0].len() as i32;
        let height = self.rows.len() as i32;
        Self::offsets()
            .iter()
            .map(|rs| rs.map(|(dr, dc)| (r + dr, c + dc)))
            .filter(|idxs| {
                idxs.iter()
                    .all(|(i, j)| *i >= 0 && *i < width && *j >= 0 && *j < height)
            })
            .collect_vec()
    }

    fn words_from_here(&self, indices: Vec<&[(i32, i32)]>) -> Vec<String> {
        indices
            .into_iter()
            .map(|cells| {
                let mut s = String::new();
                for (r, c) in cells {
                    s.push((&self.rows)[*r as usize][*c as usize]);
                }
                s
            })
            .collect()
    }

    fn xmas_from_here(&self, r: i32, c: i32) -> usize {
        self.words_from_here(
            self.indicies_from_here(r, c)
                .iter()
                .map(|x| &x[..])
                .collect(),
        )
        .into_iter()
        .filter(|w| w == "XMAS")
        .count()
    }

    fn count_xmases(&self) -> usize {
        let mut answer = 0;
        for i in 0..self.rows.len() {
            for j in 0..self.rows[0].len() {
                answer += self.xmas_from_here(i as i32, j as i32);
            }
        }
        answer
    }

    fn offsets_b() -> &'static [[(i32, i32); 3]] {
        &[[(-1, 1), (0, 0), (1, -1)], [(1, 1), (0, 0), (-1, -1)]]
    }

    fn exes_from_here_b(&self, r: i32, c: i32) -> bool {
        let idx = Self::offsets_b()
            .into_iter()
            .map(|rs| rs.map(|(dr, dc)| (r + dr, c + dc)))
            .collect_vec();

        if idx
            .iter()
            .all(|idxs| idxs.iter().all(|(i, j)| self.in_bounds(*i, *j)))
        {
            self.words_from_here(idx.iter().map(|x| &x[..]).collect())
                .iter()
                .all(|word| word == "MAS" || word == "SAM")
        } else {
            false
        }
    }

    fn count_ex_mases(&self) -> usize {
        let mut answer = 0;
        for i in 0..self.rows.len() {
            for j in 0..self.rows[0].len() {
                answer += self.exes_from_here_b(i as i32, j as i32) as usize;
            }
        }
        answer
    }

    fn in_bounds(&self, i: i32, j: i32) -> bool {
        let width = self.rows[0].len() as i32;
        let height = self.rows.len() as i32;
        i >= 0 && i < width && j >= 0 && j < height
    }
}

fn parse(filename: &str) -> Puzzle {
    let str = std::fs::read_to_string(filename).unwrap();
    let rows: Vec<Vec<_>> = str.lines().map(|l| l.chars().collect_vec()).collect_vec();
    Puzzle { rows }
}
