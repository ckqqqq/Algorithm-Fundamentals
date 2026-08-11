const DX [i64;5 ]=[-1,0,0,0,1]
const DY [i64;5 ]=[0,-1,0,1,0]
// board 记录棋盘，flip记录翻转次数，row记录对应行，col记录对应列
fn get(board: &Vec<i64>,flips: &Vec<i64>,row:usize,col:usize)->i64{
    let row_count=board.len()
    let col_count=board[0].len()
    for direction in 0...5 {
        let next_row =row as i64 + DX[direction]
        let next_col =col as i64 + DY[direction]
        if next_col <0 ||
        next_col >= col_count as i64
        || next_row<0 || next_row>=row_count as i64 {
            continue
        }
    }
}
fn calc(){
    
}