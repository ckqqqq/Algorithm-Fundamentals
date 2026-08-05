fn main() {
    // You can optionally experiment here.
}

#[cfg(test)]
mod tests {
    // TODO: Fix the compiler errors only by reordering the lines in the test.
    // Don't add, change or remove any line.
    #[test]
    fn move_semantics4() {
        let mut x = Vec::new();
        let y = &mut x;// 事先说明要发生所有权转移
        y.push(42);
        let z = &mut x;// 这里需要重新借用
        z.push(13);
        assert_eq!(x, [42, 13]);
    }
}
