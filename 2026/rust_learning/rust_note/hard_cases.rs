#[derive(Debug)]
struct Point {
    x: u64,
    y: u64,
}

#[derive(Debug)]
enum Message {
    Resize { width: u64, height: u64 },
    Move(Point),
    Echo(String),
    ChangeColor(u8, u8, u8),
    Quit,
}

// 被操作的对象：一个窗口
struct Window {
    width: u64,
    height: u64,
    x: u64,
    y: u64,
    color: (u8, u8, u8),
    open: bool,
}

impl Window {
    fn new() -> Self {
        Window { width: 100, height: 100, x: 0, y: 0, color: (0, 0, 0), open: true }
    }
}

// 处理器：消息在这里"兑现"
impl Window {
    // 处理器，消息在这里兑现
    fn handle(&mut self, message: &Message) {
        match message {
            Message::Resize { width, height } => {
                self.width = *width;      // 真的改了！
                self.height = *height;
                println!("窗口调整为 {width}x{height}");
            }
            Message::Move(p) => {
                self.x = p.x;
                self.y = p.y;
                println!("窗口移动到 ({}, {})", p.x, p.y);
            }
            Message::Echo(s) => {
                println!("窗口说：{s}");
            }
            Message::ChangeColor(r, g, b) => {
                self.color = (*r, *g, *b);
                println!("窗口变色 ({r}, {g}, {b})");
            }
            Message::Quit => {
                self.open = false;
                println!("窗口关闭");
            }
        }
    }
}

fn main() {
    let messages = [
        Message::Resize { width: 10, height: 30 },
        Message::Move(Point { x: 10, y: 15 }),
        Message::Echo(String::from("hello world")),
        Message::ChangeColor(200, 255, 255),
        Message::Quit,
    ];

    let mut window = Window::new();

    for message in &messages {
        if !window.open {
            println!("窗口已关闭，忽略消息：{message:?}");
            break;
        }
        window.handle(message);
    }

    println!("最终状态：宽{} 高{} 位置({},{}) 颜色{:?} 开着={}",
        window.width, window.height, window.x, window.y, window.color, window.open);
}