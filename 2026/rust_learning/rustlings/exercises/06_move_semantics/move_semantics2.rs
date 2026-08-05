fn fill_vec(vec: Vec<i32>) -> Vec<i32> {
    // let mut vec2 = vec;//参数vec本身不带mut。所以要绑定到一个新的变量才能push÷
    // vec 不适合实现copy，复制是昂贵操作rust不允许其发生，所以这是mov，因此vec0不可用
    let mut vec2=vec;
    vec2.push(88);

    vec2
}

fn main() {
    // You can optionally experiment here.
}

#[cfg(test)]
mod tests {
    use super::*;

    // TODO: Make both vectors `vec0` and `vec1` accessible at the same time to
    // fix the compiler error in the test.
    #[test]
    fn move_semantics2() {
        let vec0 = vec![22, 44, 66];

        let vec1 = fill_vec(vec0.clone());

        assert_eq!(vec0, [22, 44, 66]);
        assert_eq!(vec1, [22, 44, 66, 88]);
    }
}
