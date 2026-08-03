// From / Into 的实际用途：让 API "接受任何能转换的类型"

struct Email(String);

// 教会 Rust：&str 能变成 Email
impl From<&str> for Email {
    fn from(s: &str) -> Self {
        Email(s.to_string())
    }
}

// String 也能变成 Email
impl From<String> for Email {
    fn from(s: String) -> Self {
        Email(s)
    }
}

// API 写成"接受任何能转成 Email 的东西"
fn send(to: impl Into<Email>) {
    let email: Email = to.into();
    println!("发送到 {}", email.0);
}

fn main() {
    let name = "alice";

    send("a@b.com");                    // &str，直接用
    send(String::from("c@d.com"));      // String，直接用
    send(format!("{}@b.com", name));    // format! 的结果，直接用
    send(Email("e@f.com".to_string())); // 本身就是 Email，也能用

    // from 和 into 两种写法等价，零性能差异
    let e1 = Email::from("x@y.com"); // 从目标出发：Email 从哪来
    let e2: Email = "x@y.com".into(); // 从源出发：这个值要变成什么
    println!("{} == {}", e1.0, e2.0);
}
