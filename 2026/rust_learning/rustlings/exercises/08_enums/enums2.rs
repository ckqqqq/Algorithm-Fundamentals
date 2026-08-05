#[derive(Debug)]
struct Point {
    x: u64,
    y: u64,
}

#[derive(Debug)]// 
enum Message {
    // TODO: Define the different variants used below.
    Resize{width:i64,height:i64},
    Move(Point),
    Echo(String),
    ChangeColor(u8,u8,u8),
    Quit
}
//枚举的变体（variant）可以携带不同类型的数据：
// Resize 带两个 i64 字段（结构体风格）
// Move 带一个 Point 结构体（元组风格）
// Echo 带一个 String
// ChangeColor 带三个 u8
// Quit 不带数据
//整段代码就是：把五种形状各异的消息装进同一个数组，统一遍历、统一打印——enum 的意义就在这：数组元素类型都是 Message，但每个元素肚子里的数据各不相同。

impl Message {
    fn call(&self) {
        println!("{self:?}");
    }//代码长什么样子原样输出
}
//println!("{self:?}") 里的 :? 是 Debug 格式打印——把值按"代码长什么样"原样输出。它能用是因为头上写了 #[derive(Debug)]（让编译器自动生成 Debug 实现）。
fn main() {
    let messages = [
        Message::Resize {
            width: 10,
            height: 30,
        },
        Message::Move(Point { x: 10, y: 15 }),
        Message::Echo(String::from("hello world")),
        Message::ChangeColor(200, 255, 255),
        Message::Quit,
    ];

    for message in &messages {//打印代码本身牛
        message.call();
    }
}// rust 的特点，随用随定义


