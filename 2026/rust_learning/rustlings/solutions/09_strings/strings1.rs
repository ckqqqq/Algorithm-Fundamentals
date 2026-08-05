fn current_favorite_color() -> String {
    // Equivalent to `String::from("blue")`
    "blue".to_string()//重新进行堆分配
    // "blue"//&str类型，只是借用·
}

fn main() {
    let answer = current_favorite_color();
    println!("My current favorite color is {answer}");
}
