#![allow(clippy::ptr_arg)]

// TODO: Fix the compiler errors without changing anything except adding or
// removing references (the character `&`).
//纠正语法错误不通过变化任何东西除了添加或删除引用，双重否定！！！！

// Shouldn't take ownership
fn get_char(data: &String) -> char {//我借用一下，不动
    data.chars().last().unwrap()
}

// Should take ownership
fn string_uppercase(mut data: String) {//我要改！！
    data = data.to_uppercase();

    println!("{data}");
}

fn main() {
    let data = "Rust is great!".to_string();

    get_char(&data);

    string_uppercase(data);
}
