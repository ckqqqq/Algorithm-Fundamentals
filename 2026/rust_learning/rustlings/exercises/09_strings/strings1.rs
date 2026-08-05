// TODO: Fix the compiler error without changing the function signature.
fn current_favorite_color() -> String {
    "blue".to_string()
    // "blue“ 的类型是&str
    // "blue".to_string()           // 通用，任何 &str 都能转
    // String::from("blue")         // 同上，构造器风格
    // "blue".to_owned()            // 语义更明确："变成拥有的"
    // "blue".into()                // 靠目标类型推断转换


}

fn main() {
    let answer = current_favorite_color();
    println!("My current favorite color is {answer}");
}
