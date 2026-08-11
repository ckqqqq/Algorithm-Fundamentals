use std::io::{self, Read};

/// 翻转 (r, c) 处的十字：自身 + 上下左右
fn flip(board: &mut Vec<Vec<u8>>, n: usize, m: usize, r: usize, c: usize) {
    board[r][c] ^= 1;
    if r > 0 {
        board[r - 1][c] ^= 1;
    }
    if r + 1 < n {
        board[r + 1][c] ^= 1;
    }
    if c > 0 {
        board[r][c - 1] ^= 1;
    }
    if c + 1 < m {
        board[r][c + 1] ^= 1;
    }
}

/// 目标状态为 target（全 0 或全 1）时的最少操作次数；不可达返回 None
fn min_flips_to(board: &[Vec<u8>], n: usize, m: usize, target: u8) -> Option<u64> {
    let mut best: Option<u64> = None;

    // 枚举第一行的 2^m 种翻法，mask 的第 j 位 = 1 表示翻 (0, j)
    for mask in 0u64..(1 << m) {
        let mut b = board.to_vec(); // 在副本上模拟
        let mut count = 0u64;

        // 第一步：按 mask 翻第一行
        for j in 0..m {
            if mask >> j & 1 == 1 {
                flip(&mut b, n, m, 0, j);
                count += 1;
            }
        }

        // 第二步：贪心——第 i 行的翻法被第 i-1 行唯一决定：
        // 上一行哪个格子还不是 target，就必须翻它正下方的格子来修正
        for i in 1..n {
            for j in 0..m {
                if b[i - 1][j] != target {
                    flip(&mut b, n, m, i, j);
                    count += 1;
                }
            }
        }

        // 第三步：前 n-1 行已被修正，检查最后一行是否也全部达标
        if b[n - 1].iter().all(|&cell| cell == target) {
            best = Some(best.map_or(count, |old| old.min(count)));
        }
    }
    best
}

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut tokens = input.split_whitespace();

    let n: usize = tokens.next().unwrap().parse().unwrap();
    let m: usize = tokens.next().unwrap().parse().unwrap();
    let board: Vec<Vec<u8>> = (0..n)
        .map(|_| (0..m).map(|_| tokens.next().unwrap().parse().unwrap()).collect())
        .collect();

    // 两种目标状态都试，取较小者
    let answer = [min_flips_to(&board, n, m, 0), min_flips_to(&board, n, m, 1)]
        .into_iter()
        .flatten() // 滤掉 None，展开 Some(x) → x
        .min();

    match answer {
        Some(count) => println!("{count}"),
        None => println!("Impossible"),
    }
}
