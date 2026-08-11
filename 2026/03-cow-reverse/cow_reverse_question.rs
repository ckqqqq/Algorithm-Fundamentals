/*
开关翻转问题（Flip Game / Lights Out，经典原型：POJ 1753）

【题目描述】

有一个 n 行 m 列的棋盘，每个格子里有一个开关，状态为 0（关）或 1（开）。

每次操作可以选择一个开关进行"翻转"：该开关自身，以及它上下左右四个方向，注意上下左右四个方向可以不合法的
相邻的所有开关（边界处不足四个则忽略不存在的方向），状态同时取反（0 变 1，1 变 0）。

目标：通过若干次操作，使棋盘上所有开关状态一致（全为 0 或全为 1）。
求最少操作次数；如果无论如何都无法达到，输出 "Impossible"。

【关键性质（解题提示）】

1. 同一个开关翻转两次等于没翻 → 每个格子最多翻一次，操作集合是 0/1 选择；
2. 操作顺序不影响最终结果（异或可交换）→ 只需决定"翻哪些格子"；
3. 第一行的翻法一旦确定，第二行每个格子是否翻转被第一行唯一"逼"出来
   （为了把第一行全部消成目标状态），依此类推 → 枚举行首行，其余贪心；
4. 因此总复杂度 O(2^m · n · m)，m 较大时也可改用 GF(2) 高斯消元。

【输入格式】

第一行两个整数 n, m（1 ≤ n, m ≤ 16）。
接下来 n 行，每行 m 个整数（0 或 1），空格分隔，表示棋盘初始状态。

【输出格式】

一行一个整数：最少操作次数；若不可能，输出 Impossible。

【样例输入】

4 4
1 0 0 1
0 1 1 0
0 1 1 0
1 0 0 1

【样例输出】

4

【样例解释】

一种可行方案：翻转 (0,1)、(0,2)、(3,1)、(3,2)（0-based 行列号），
共 4 次操作后全棋盘变为 0。可以证明不存在更少次数的方案。
*/
// 方向偏移表：(dx[i], dy[i]) 依次表示 自身、上、下、左、右
const DX: [i32; 5] = [-1, 0, 0, 0, 1];
const DY: [i32; 5] = [0, -1, 0, 1, 0];

// ============ 1. get：查询某个格子的颜色 ============
// 给定棋盘和翻转方案，返回 (row, col) 这个格子的当前状态（0 或 1）。
// 算法：初始值 异或 所有会翻转它的格子（自身 + 上、下、左、右）。
fn get(board: &[Vec<i32>], flips: &[Vec<i32>], row: usize, col: usize) -> i32 {
    let row_count = board.len();
    let column_count = board[0].len();

    // 数一数这个格子总共被翻了多少次（初始值 + 自身 + 上、下、左、右）
    let mut flip_count = board[row][col];
    for direction in 0..5 {
        // row / col 是 usize（不能为负数），但方向里有 -1，所以先转成 i32 才能做加法
        let next_row = row as i32 + DX[direction];
        let next_col = col as i32 + DY[direction];

        // 越界的方向（比如第一行没有"上方"）直接跳过
        if next_row < 0
            || next_row >= row_count as i32
            || next_col < 0
            || next_col >= column_count as i32
        {
            continue;
        }
        flip_count += flips[next_row as usize][next_col as usize]; // 累加每个方向的翻转
    }
    // 被翻奇数次 → 结果为 1，偶数次 → 结果为 0（本质等价于异或）
    flip_count % 2
}

// ============ 2. calc：第一行翻法确定后，算最少次数 ============
// 第一行翻法一旦确定（first_row_mask），其余每一行怎么翻就被唯一"逼"出来：
//   第 row 行的 (row, col) 是否翻，取决于上一行 (row-1, col) 是不是目标值。
// 翻完后检查最后一行是否也全部达标：
//   - 达标 → 返回总共翻了多少次；
//   - 不达标 → 返回 -1，表示这种第一行翻法不可行。
fn calc(board: &[Vec<i32>], target: i32, first_row_mask: usize) -> i32 {
   // 传入棋盘，翻或者不翻
    let row_count = board.len();
    let column_count = board[0].len();

    // flips[row][col] == 1 表示要翻转 (row, col)；作用域只在函数内部
    let mut flips = vec![vec![0; column_count]; row_count];

    // 1. 设置第一行的翻法
    for col in 0..column_count {
        flips[0][col] = ((first_row_mask >> col) & 1) as i32;// 取对应的列，然后判断翻不翻
    }//遍历这一列的方案，判断它翻不翻

    // 2. 从第二行开始，每一行都被"修正上一行"这一条件逼出来
    for row in 1..row_count {
        for col in 0..column_count {
            // 上一行这一格还不是目标值，就翻转正下方这一格来修正它。
            // 注意此时 flips[row][col] 还是 0，get 自然算的是"没被正下方翻过"的状态。
            flips[row][col] = if get(board, &flips, row - 1, col) != target { 1 } else { 0 };
        }
        //注意值去翻转正下方这一格来修正上一行，所以这里翻转的是当前行
    }

    // 3. 最后一行没有下一行帮它修正，单独检查是否全部达标
    for col in 0..column_count {
        if get(board, &flips, row_count - 1, col) != target {// 最后一行这一列
            return -1; // 有一格不达标 → 这种第一行翻法不可行
        }
    }

    // 4. 统计总翻转次数
    flips.iter().map(|row| row.iter().sum::<i32>()).sum()
}

// ============ 3. solve：读输入 + 枚举第一行 ============
// 目标状态可能是"全 0"或"全 1"，分别枚举第一行的所有翻法（2^m 种），
// 调用 calc 得到每种翻法的次数，取最小。
fn solve() {
    // 读输入：全部数字进来，前两个是行数 n 和列数 m
    let mut input = String::new();
    std::io::stdin().read_to_string(&mut input).unwrap();
    let nums: Vec<i32> = input
        .split_whitespace()
        .map(|token| token.parse().unwrap())
        .collect();

    let row_count = nums[0] as usize;
    let column_count = nums[1] as usize;
    let mut board = Vec::new();
    let mut index = 2;
    for _ in 0..row_count {
        let mut row = Vec::new();
        for _ in 0..column_count {
            row.push(nums[index]);
            index += 1;
        }
        board.push(row);
    }

    let mut best = i32::MAX;
    for target in 0..=1 {//// target = 0：把所有格子变成 0//// 再跑一遍 target = 1：把所有格子变成 1
        for first_row_mask in 0..(1 << column_count) {// first_row_mask是第一行翻转方案，二进制位表示哪些列要翻
            // 把第一行翻转方案传给 calc，得到总次数（或 -1）
            let result = calc(&board, target, first_row_mask);
            if result != -1 {
                best = best.min(result);
            }
        }
    }

    if best == i32::MAX {
        println!("Impossible");
    } else {
        println!("{}", best);
    }
}

// main 只做一件事：调用 solve
fn main() {
    solve();
}