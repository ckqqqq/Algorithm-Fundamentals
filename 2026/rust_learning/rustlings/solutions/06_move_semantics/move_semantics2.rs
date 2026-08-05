fn fill_vec(vec: Vec<i32>) -> Vec<i32> {//如果函数签名没有引用，代表这个函数会吃掉你的所有权，它会还我一个新的（可能改过，可能没改，我不需要知道）。
    let mut vec = vec;

    vec.push(88);

    vec
}

fn main() {
    // You can optionally experiment here.
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn move_semantics2() {
        let vec0 = vec![22, 44, 66];

        // Cloning `vec0` so that the clone is moved into `fill_vec`, not `vec0`
        // itself.
        let vec1 = fill_vec(vec0.clone());// 这里差点错了

        assert_eq!(vec0, [22, 44, 66]);
        assert_eq!(vec1, [22, 44, 66, 88]);
    }
}
