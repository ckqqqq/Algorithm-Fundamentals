fn trim_me(input: &str) -> &str {
    // TODO: Remove whitespace from both ends of a string.
    input.trim()
}

fn compose_me(input: &str) -> String {
    // TODO: Add " world!" to the string! There are multiple ways to do this.
    // format!("{} world!", input)
    //way2 
    // input.to_string()+"world!"
    //way3
    // input.to_owned()+"world!"
    //way4
    format!("{input} world!")
    //+ 背后的故事（值得知道）
    // input.to_string() + " world!"
    // 这个 + 不是凭空来的，它展开后是：

    // String::add(input.to_string(), " world!")
    // 注意签名：fn add(self, other: &str) -> String —— 左边必须是拥有的 String（会被消耗），右边必须是借用。所以 input + " world!" 直接报错：&str 没有资格站左边。这就是必须先 to_string() 的原因。

    // 效率排行（其实还有第五种）
    // 最高效的做法你没列：
    let mut s = String::from(input);
    // s.push_str(" world!");    // 原地追加，零额外分配
    //对比：+ 和 format! 是"买新房搬家"
    //push_str 是"原地扩建"，不搬家
    // 但题目要求返回 String，所以 push_str 后返回 s 即可
    // 不过 format! 可读性最好，日常推荐
    // 这里为了展示，我用 format!
    // 但注意：format! 会分配新内存，push_str 不会
    // 如果性能敏感，用 push_str
    // 但这里测试只检查内容，不检查性能
    //所以上轮的建议可以这样记：单次拼接用 format!（一次建好），反复追加以 push_str（原地生长），+ 留给一次性的小拼接。

}

fn replace_me(input: &str) -> String {
    // TODO: Replace "cars" in the string with "balloons".
    input.replace("cars","balloons")
}

fn main() {
    // You can optionally experiment here.
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn trim_a_string() {
        assert_eq!(trim_me("Hello!     "), "Hello!");
        assert_eq!(trim_me("  What's up!"), "What's up!");
        assert_eq!(trim_me("   Hola!  "), "Hola!");
        assert_eq!(trim_me("Hi!"), "Hi!");
    }

    #[test]
    fn compose_a_string() {
        assert_eq!(compose_me("Hello"), "Hello world!");
        assert_eq!(compose_me("Goodbye"), "Goodbye world!");
    }

    #[test]
    fn replace_a_string() {
        assert_eq!(
            replace_me("I think cars are cool"),
            "I think balloons are cool",
        );
        assert_eq!(
            replace_me("I love to look at cars"),
            "I love to look at balloons",
        );
    }
}
