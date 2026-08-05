// Calls of this function should be replaced with calls of `string_slice` or `string`.
fn placeholder() {}

fn string_slice(arg: &str) {
    println!("{arg}");
}

fn string(arg: String) {
    println!("{arg}");
}

// TODO: Here are a bunch of values - some are `String`, some are `&str`.
// Your task is to replace `placeholder(…)` with either `string_slice(…)`
// or `string(…)` depending on what you think each value is.
fn main() {
    //没造新字节（只是看/裁剪已有数据）  →  &str
    // 造了新字节（分配、拷贝、变换）      →  String
    string_slice("blue");//没有操作

    string("red".to_string());//拷贝一份

    string(String::from("hi"));//拷贝一份，建立新内存

    string("rust is fun!".to_owned());//组织形式发私信变化，需要新内存

    string("nice weather".into());//组织形式发生变化，需要新内存

    string(format!("Interpolation {}", "Station"));// format! 创建新字符串，发生内存分配

    // WARNING: This is byte indexing, not character indexing.
    // Character indexing can be done using `s.chars().nth(INDEX)`.
    string_slice(&String::from("abc")[0..1]);//只是不看了

    string_slice("  hello there ".trim());//只是不看了

    string("Happy Monday!".replace("Mon", "Tues"));//发生内存分配

    string("mY sHiFt KeY iS sTiCkY".to_lowercase());//发生内存分配，新建内存，需要内存操作
}
