# Rust 学习手册

> 面向有一定编程基础（如 C++/Python/Go）的学习者。
> 目标：覆盖 Rust 最核心、最需要掌握的知识点，配代码示例，学完后能独立写中小型项目。
>
> 使用方式：每章先读讲解，再动手敲一遍示例（`rustc xxx.rs` 或放进 cargo 项目），最后去 `rustlings/exercises/` 做对应练习。

---

## 目录

- 第一部分：核心所有权体系（劝退点 1）
  - 第 1 章 所有权 Ownership
  - 第 2 章 借用与引用 Borrowing
  - 第 3 章 生命周期 Lifetimes
- 第二部分：类型系统与抽象
  - 第 4 章 结构体与 impl
  - 第 5 章 枚举与模式匹配
  - 第 6 章 错误处理
  - 第 7 章 泛型
  - 第 8 章 Trait
- 第三部分：日常编码必备
  - 第 9 章 常用集合类型
  - 第 10 章 迭代器与闭包（劝退点 2）
  - 第 11 章 智能指针
  - 第 12 章 模块系统与 Cargo
- 第四部分：进阶
  - 第 13 章 并发
  - 第 14 章 常用 trait 速查
  - 第 15 章 测试
- 附录：常见编译错误速查 & 学习路线

---

# 第一部分：核心所有权体系

这一部分是整个 Rust 的基石。理解了它，后面的内容都是顺水推舟；不理解它，写每一行代码都会和编译器打架。

## 第 1 章 所有权（Ownership）

### 1.1 为什么需要所有权

| 语言 | 内存管理方式 | 代价 |
|---|---|---|
| C/C++ | 手动 malloc/free | 悬垂指针、双重释放、内存泄漏 |
| Java/Python/Go | GC 垃圾回收 | 运行时开销、停顿 |
| **Rust** | **所有权 + 编译期检查** | 学习曲线，但零运行时开销 |

### 1.2 三条铁律

1. Rust 中**每个值都有一个所有者**（owner）。
2. 同一时间**只能有一个**所有者。
3. 所有者离开作用域，值被**自动 drop**（释放）。

```rust
fn main() {
    let s = String::from("hello"); // s 是所有者
    // s 在这里有效
} // s 离开作用域，String 的堆内存被自动释放 —— 不需要 free，也不需要 GC
```

### 1.3 Move 语义：赋值即转移

```rust
let s1 = String::from("hello");
let s2 = s1;              // 所有权从 s1 转移给 s2
// println!("{}", s1);    // 编译错误！s1 已失效，防止双重释放
println!("{}", s2);       // OK
```

这和 C++ 的 `std::move` 类似，但 Rust 是**默认行为**且编译器强制失效旧变量。

**为什么？** 如果 `s1` 和 `s2` 都有效，离开作用域时会释放同一块堆内存两次（double free）。Rust 在编译期直接让 `s1` 失效，根除这个问题。

### 1.4 Copy 类型：栈上小数据的例外

实现了 `Copy` trait 的类型（整数、浮点、布尔、字符、元组 of Copy）是**按位复制**，不转移所有权：

```rust
let x = 5;
let y = x;           // 复制，x 依然有效
println!("{} {}", x, y); // OK
```

### 1.5 clone：显式深拷贝

```rust
let s1 = String::from("hello");
let s2 = s1.clone();   // 堆内存也复制一份，两个都有效
```

> 性能意识：`clone` 有堆分配开销，能借用就别 clone。

### 1.6 函数传参与返回值同样遵循 move

```rust
fn takes_ownership(s: String) {  // s 获得所有权
    println!("{}", s);
} // s 被 drop

fn gives_ownership() -> String { // 所有权通过返回值移交
    String::from("hello")
}
```

**心法**：所有权系统的本质是——把「谁负责释放内存」这件事从程序员的脑子里，转移到编译器的检查里。

---

## 第 2 章 借用与引用（Borrowing）

每次都转移所有权太繁琐，所以 Rust 允许「借」。

### 2.1 不可变引用 `&T`

```rust
fn main() {
    let s = String::from("hello");
    let len = calculate_length(&s);  // 借用，不转移所有权
    println!("'{}' 长度是 {}", s, len); // s 依然有效
}

fn calculate_length(s: &String) -> usize {
    s.len()
} // s 是引用，离开作用域不会 drop 任何东西
```

### 2.2 可变引用 `&mut T`

```rust
fn main() {
    let mut s = String::from("hello");
    change(&mut s);
    println!("{}", s); // "hello, world"
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

### 2.3 借用检查器的两条铁律（重点！）

在**同一作用域、同一时刻**：

1. 可以有**任意多个不可变引用** `&T`；**或者**
2. 只能有**一个可变引用** `&mut T`。

二者**不可兼得**：

```rust
let mut s = String::from("hello");

let r1 = &s;
let r2 = &s;        // OK：多个不可变引用
// let r3 = &mut s; // 编译错误！已有不可变引用，不能再借可变的

println!("{} {}", r1, r2); // r1、r2 最后一次使用后，借用结束（NLL）
let r3 = &mut s;    // OK：此时不可变引用已结束
```

**为什么？** 这就是 Rust 在编译期消除**数据竞争**的机制。读写冲突在编译期就被拦下，而不是运行期偶发崩溃。

> NLL（Non-Lexical Lifetimes）：引用的有效期到**最后一次使用**为止，而不是到作用域结束。

### 2.4 悬垂引用：编译器帮你堵的 C++ 经典 bug

```rust
fn dangle() -> &String {      // 编译错误！
    let s = String::from("hi");
    &s                        // s 马上被 drop，返回它的引用 = 悬垂
}
```

C++ 里这段代码能编译，运行时崩溃；Rust 直接编译失败。

### 2.5 字符串切片 `&str`

```rust
let s = String::from("hello world");
let hello = &s[0..5];   // "hello"，借用原字符串的一部分，零拷贝
```

- `String`：拥有所有权的堆字符串，可增长。
- `&str`：字符串切片，是「借来的视图」。
- 函数参数优先用 `&str` 而不是 `&String`（更通用，`&String` 可自动 deref 成 `&str`）：

```rust
fn first_word(s: &str) -> &str {  // 既能收 String 也能收字面量
    // ...
}
```

---

## 第 3 章 生命周期（Lifetimes）

### 3.1 生命周期是什么

生命周期不是「语法特性」，而是**借用检查器推理的依据**。大多数时候编译器能自动推导；推不出来时，需要你用 `'a` 标注帮它说明「这些引用的存活关系」。

> 生命周期标注**不改变**任何引用的存活时间，只是向编译器**描述**关系。

### 3.2 什么时候必须标注：函数返回引用

```rust
// 编译错误：返回的引用到底来自 x 还是 y？编译器不知道
fn longest(x: &str, y: &str) -> &str { ... }

// 正确：标注表示「返回值活得和参数中较短的那个一样久」
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

### 3.3 结构体持有引用时必须标注

```rust
struct ImportantExcerpt<'a> {
    part: &'a str,  // 这个结构体不能比它引用的数据活得更久
}

fn main() {
    let novel = String::from("第一章。很多内容……");
    let first = novel.split('。').next().unwrap();
    let i = ImportantExcerpt { part: first };
} // OK：i 在 novel 之前 drop
```

### 3.4 生命周期省略规则（Elision）

编译器满足这三条时不用手写：

1. 每个引用参数获得独立生命周期；
2. 只有一个引用参数时，它的生命周期赋给所有输出；
3. 有 `&self` / `&mut self` 的方法，输出生命周期跟 self 走。

所以 `fn first_word(s: &str) -> &str` 不用标注。

### 3.5 `'static`

整个程序期间有效。字符串字面量就是 `&'static str`。

**常见误区**：遇到生命周期报错就加 `'static`——这是错的。正确思路是**理清谁拥有数据**，通常该改设计（比如让函数返回 `String` 而不是 `&str`）。

### 3.6 避坑指南

- 函数返回引用时，问自己：这个引用指向的数据是谁的？
- 如果指向的是函数内部创建的局部变量 → 返回 owned 类型（`String` 而非 `&str`）。
- 如果指向的是参数 → 标注生命周期。
- struct 想持有引用 → 先考虑能不能持有 owned 值；确实需要零拷贝再加生命周期参数。

---

# 第二部分：类型系统与抽象

## 第 4 章 结构体与 impl

### 4.1 定义与实例化

```rust
#[derive(Debug)]
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

fn build_user(email: String, username: String) -> User {
    User {
        username,          // 字段初始化简写：变量名 = 字段名时省略
        email,
        sign_in_count: 1,
        active: true,
    }
}
```

其他形态：

```rust
struct Color(i32, i32, i32);  // 元组结构体
struct Unit;                   // 单元结构体（占位/标记用）

// 结构体更新语法
let user2 = User { email: String::from("a@b.com"), ..user1 };
// 注意：String 字段被 move，user1 部分失效
```

### 4.2 方法

```rust
impl Rectangle {
    // 方法：第一个参数是 self
    fn area(&self) -> u32 {           // &self：只读借用
        self.width * self.height
    }

    fn enlarge(&mut self, factor: u32) {  // &mut self：可变借用
        self.width *= factor;
        self.height *= factor;
    }

    // 关联函数（无 self，类似静态方法/构造函数）//静态方法，构造矩形
    fn square(size: u32) -> Rectangle {
        Rectangle { width: size, height: size }
    }
}

let mut rect = Rectangle { width: 30, height: 50 };
println!("面积: {}", rect.area());   // 自动解引用，无需 (*rect).area()
rect.enlarge(2);
let sq = Rectangle::square(10);      // 关联函数用 :: 调用
```

`self` 三种形态对照：

| 写法 | 含义 | 典型用途 |
|---|---|---|
| `&self` | 只读借用 | 绝大多数方法 |
| `&mut self` | 可变借用 | 修改状态 |
| `self` | 夺取所有权 | 转换、链式构建器消费自身 |

---

## 第 5 章 枚举与模式匹配

### 5.1 Rust 的 enum 是「代数数据类型」

C 的 enum 只是整数标签，Rust 的 enum 每个变体可以**携带不同类型和数量的数据**：

```rust
enum Message {
    Quit,                        // 无数据
    Move { x: i32, y: i32 },     // 结构体式
    Write(String),               // 元组式
    ChangeColor(i32, i32, i32),
}

impl Message {
    fn call(&self) { /* 方法 */ }
}
```

### 5.2 `Option<T>`：Rust 没有 null

```rust
enum Option<T> {
    Some(T),
    None,
}
```

null 引用被称为「十亿美元的错误」。Rust 用 `Option` 把「可能没有值」**编码进类型系统**，强制你处理 None 分支。

```rust
let x: Option<i32> = Some(5);
// let sum = x + 1;      // 编译错误：Option<i32> 不能直接加

// 正确的打开方式
if let Some(v) = x {
    println!("值是 {}", v);
}

let v = x.unwrap_or(0);      // None 时用默认值
```

### 5.3 match：穷尽性检查

```rust
enum Coin { Penny, Nickel, Dime, Quarter }

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    } // 少写一个分支就编译失败 —— 重构时的安全保障
}
```

带数据的匹配与 `_` 通配：

```rust
match msg {
    Message::Move { x, y } => println!("移动到 {}, {}", x, y),
    Message::Write(s) => println!("文本: {}", s),
    _ => (),   // 其余全部忽略
}
```

### 5.4 常用匹配工具

```rust
// if let：只关心一个分支
if let Some(v) = opt { println!("{}", v); }

// let-else（Rust 1.65+）：守卫式提前返回
let Some(v) = opt else { return; };

// matches! 宏：返回 bool
if matches!(msg, Message::Quit) { ... }

// match 守卫
match num {
    Some(n) if n > 0 => println!("正数"),
    Some(_) => println!("非正数"),
    None => (),
}
```

---

## 第 6 章 错误处理

### 6.1 两类错误

- **不可恢复**：`panic!`，程序终止。用于 bug、契约违反。
- **可恢复**：`Result<T, E>`，函数签名即错误契约。

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

### 6.2 `?` 运算符：Rust 错误处理的精髓

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;  // Err 时提前 return
    let mut s = String::new();
    f.read_to_string(&mut s)?;             // 同上
    Ok(s)
}
```

`?` 等价于：

```rust
let mut f = match File::open("hello.txt") {
    Ok(f) => f,
    Err(e) => return Err(e),
};
```

### 6.3 实战选择

| 场景 | 推荐 |
|---|---|
| 库代码 | 返回 `Result<T, E>`，用 `thiserror` 定义错误类型 |
| 应用代码 | `anyhow::Result<T>` 统一错误 |
| 示例/测试 | `unwrap()` / `expect("说明")` 可接受 |
| 明确的不变量 | `expect("这里绝不应该是 None，因为...")` |

```rust
// 实际项目中最常见的形态
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let text = std::fs::read_to_string("config.toml")
        .context("读取 config.toml 失败")?;  // 附加上下文
    let cfg: Config = toml::from_str(&text)?;
    Ok(cfg)
}
```

**原则**：`panic!` 是给 bug 用的；`Result` 是给「预期会发生的失败」（IO、网络、解析）用的。

---

## 第 7 章 泛型

### 7.1 基本用法

```rust
fn largest<T: PartialOrd>(list: &[T]) -> &T {
    let mut largest = &list[0];
    for item in list {
        if item > largest { largest = item; }
    }
    largest
}

struct Point<T> {
    x: T,
    y: T,
}

impl<T> Point<T> {
    fn x(&self) -> &T { &self.x }
}

// 可以只对具体类型实现方法
impl Point<f32> {
    fn distance_from_origin(&self) -> f32 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

### 7.2 关键认知

- **零成本抽象**：泛型在编译期单态化（monomorphization），每个用到的类型生成一份专门代码，运行时无开销。
- 泛型参数靠 **trait bound** 约束能力：`T: PartialOrd` 表示「T 必须能比较大小」。

---

## 第 8 章 Trait

Trait 是 Rust 最重要的抽象机制，约等于「接口 + 类型类」。

### 8.1 定义与实现

```rust
trait Summary {
    fn summarize(&self) -> String;           // 必须实现

    fn preview(&self) -> String {            // 默认实现，可覆盖
        format!("(阅读更多) {}", self.summarize())
    }
}

struct Tweet { username: String, content: String }

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}
```

> 孤儿规则（Orphan Rule）：trait 和类型至少有一个是本地定义的才能 impl。不能给外部类型实现外部 trait（如 `impl Display for Vec<T>` 不行）。

### 8.2 Trait bound 三种写法

```rust
// 1. 泛型约束
fn notify<T: Summary>(item: &T) { ... }

// 2. impl Trait 语法糖（参数位置）
fn notify(item: &impl Summary) { ... }

// 3. where 子句（约束多时更清晰）
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{ ... }
```

返回值也可以用 `impl Trait`（但只能返回一种具体类型）：

```rust
fn make_summarizable() -> impl Summary {
    Tweet { username: "horse".into(), content: "of course".into() }
}
```

### 8.3 条件实现：泛型 + trait 的化学反应

```rust
// 标准库真实模式：只有 T 实现了 Display，Pair<T> 才有 to_string
impl<T: Display> ToString for T { ... }
```

### 8.4 Trait 对象：运行时多态

泛型是**编译期单态化**（静态分发，快，类型固定）；`dyn Trait` 是**运行时多态**（动态分发，类型可混合）：

```rust
trait Draw { fn draw(&self); }

struct Button;
struct TextField;
impl Draw for Button { fn draw(&self) { /*...*/ } }
impl Draw for TextField { fn draw(&self) { /*...*/ } }

// 异构集合：必须靠 trait 对象
let components: Vec<Box<dyn Draw>> = vec![
    Box::new(Button),
    Box::new(TextField),
];
for c in components { c.draw(); }
```

选择原则：性能敏感 + 类型已知 → 泛型；需要异构集合 / 插件式扩展 → `Box<dyn Trait>`。

---

# 第三部分：日常编码必备

## 第 9 章 常用集合类型

### 9.1 `String` vs `&str`（高频困惑点）

| | `String` | `&str` |
|---|---|---|
| 所有权 | 拥有 | 借用 |
| 可增长 | 是 | 否 |
| 存储 | 堆 | 任意（堆切片/字面量/静态区） |
| 场景 | 需要持有、修改 | 函数参数、只读视图 |

```rust
let mut s = String::from("hello");  // 拥有
s.push_str(" world");
let slice: &str = &s[0..5];         // 借用
let s2 = slice.to_string();         // 借用 → 拥有
let s3: String = "literal".into();  // 字面量 → String
```

### 9.2 `Vec<T>`

```rust
let mut v = vec![1, 2, 3];
v.push(4);

// 两种取值方式，区别在越界行为
let third: &i32 = &v[2];           // 越界会 panic
let third: Option<&i32> = v.get(2); // 越界返回 None，更安全

for i in &v { print!("{} ", i); }      // 不可变遍历
for i in &mut v { *i += 10; }          // 可变遍历
```

> 经典借用冲突：`v.push()` 时若持有 `v` 元素的引用会编译失败——push 可能触发扩容重新分配，旧引用就悬垂了。这就是借用检查器的价值。

### 9.3 `HashMap<K, V>`

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);

// entry API：「没有就插入」的惯用写法
scores.entry(String::from("Blue")).or_insert(50);
*scores.entry(String::from("Yellow")).or_insert(0) += 1;

// 统计词数
let mut map = HashMap::new();
for word in "hello world hello".split_whitespace() {
    *map.entry(word).or_insert(0) += 1;
}
```

---

## 第 10 章 迭代器与闭包（劝退点 2）

### 10.1 迭代器核心：惰性 + 消费

```rust
let v = vec![1, 2, 3];

let iter = v.iter();          // 惰性：什么都不会发生
let total: i32 = iter.sum();  // 消费适配器才真正执行
```

三种迭代方式：

| 方法 | 产出 | 等价于 |
|---|---|---|
| `.iter()` | `&T` | 不可变借用遍历 |
| `.iter_mut()` | `&mut T` | 可变借用遍历 |
| `.into_iter()` | `T` | 夺取所有权遍历 |

### 10.2 高频适配器

```rust
let v = vec![1, 2, 3, 4, 5, 6];

// 链式管道：过滤 → 变换 → 收集
let result: Vec<i32> = v.iter()
    .filter(|x| *x % 2 == 0)   // 留偶数
    .map(|x| x * x)            // 平方
    .collect();                // 收集成 Vec
// [4, 16, 36]

v.iter().find(|&&x| x > 3);          // Option<&i32>
v.iter().any(|&x| x > 5);            // bool
v.iter().fold(0, |acc, x| acc + x);  // 累加
v.iter().enumerate();                // (下标, 元素)
v.iter().zip(other.iter());          // 两两配对
```

> 性能认知：迭代器是零成本抽象，编译后等价于手写循环，甚至比循环更优（编译器能消除边界检查）。

### 10.3 闭包

```rust
let add = |x, y| x + y;              // 类型自动推导
let double = |x: i32| -> i32 { x * 2 };
```

闭包按捕获方式分三个 trait（编译器自动推导，从严到松）：

| Trait | 捕获方式 | 场景 |
|---|---|---|
| `Fn` | 只读借用 `&T` | 普通回调 |
| `FnMut` | 可变借用 `&mut T` | 修改外部状态 |
| `FnOnce` | 夺取所有权 | 只能调用一次 |

```rust
let s = String::from("hello");
let print = move || println!("{}", s); // move：把 s 的所有权移进闭包
print();
// println!("{}", s);  // 编译错误：s 已被 move
```

`move` 典型场景：开线程时把数据所有权移入闭包。

---

## 第 11 章 智能指针

普通引用 `&T` 只是借用；智能指针**拥有**数据，还带额外能力。

### 11.1 `Box<T>`：堆分配，单一所有权

```rust
let b = Box::new(5);  // 5 存在堆上，b 是栈上的指针

// 递归类型必须靠 Box（编译器需要知道大小）
enum List {
    Cons(i32, Box<List>),
    Nil,
}
```

### 11.2 `Rc<T>`：引用计数，单线程共享所有权

```rust
use std::rc::Rc;

let a = Rc::new(String::from("shared"));
let b = Rc::clone(&a);  // 计数 +1，不是深拷贝
let c = Rc::clone(&a);
println!("引用数: {}", Rc::strong_count(&a)); // 3
// 计数归零时数据被释放
```

### 11.3 `RefCell<T>`：内部可变性（绕过编译期借用规则，运行期检查）

```rust
use std::cell::RefCell;

let data = RefCell::new(vec![1, 2, 3]);
data.borrow_mut().push(4);        // 运行期借用检查
println!("{:?}", data.borrow());  // [1, 2, 3, 4]
// 若同时存在 borrow() 和 borrow_mut() → 运行期 panic（不是编译错误）
```

### 11.4 组合模式速查

| 需求 | 组合 |
|---|---|
| 单线程共享只读 | `Rc<T>` |
| 单线程共享可修改 | `Rc<RefCell<T>>` |
| 多线程共享只读 | `Arc<T>` |
| 多线程共享可修改 | `Arc<Mutex<T>>` |

> 抉择顺序：能用 `&T` 就别用智能指针；先 `Box`，共享再 `Rc`，可变共享加 `RefCell`，跨线程换 `Arc`/`Mutex`。

---

## 第 12 章 模块系统与 Cargo

### 12.1 模块层级

```
crate
 └── front_of_house/          // mod（目录）
      ├── hosting/            // 子模块
      └── serving/
```

```rust
// src/lib.rs
mod front_of_house;            // 声明模块（加载对应文件）

pub use crate::front_of_house::hosting; // 重导出，简化外部路径

pub fn eat_at_restaurant() {
    hosting::add_to_waitlist();
}
```

关键规则：

- 所有项**默认私有**，`pub` 才对外可见。
- 子模块能访问父模块的私有项，反之不行。
- `use` 引入路径，`pub use` 再导出。
- struct 的字段默认私有（即使 struct 是 pub）；enum 变体随 enum 的可见性。

### 12.2 Cargo 必会命令

```bash
cargo new my_project       # 新建
cargo build --release      # 发布构建（优化）
cargo test                 # 跑测试
cargo clippy               # lint（写出地道 Rust 的教练）
cargo fmt                  # 格式化
cargo add serde            # 加依赖
cargo doc --open           # 生成并打开文档
```

---

# 第四部分：进阶

## 第 13 章 并发

### 13.1 线程

```rust
use std::thread;
use std::time::Duration;

let handle = thread::spawn(move || {   // move 把数据所有权移进线程
    for i in 1..5 {
        println!("子线程 {}", i);
        thread::sleep(Duration::from_millis(1));
    }
});
handle.join().unwrap();   // 等待结束
```

### 13.2 消息传递：channel（Go 风格）

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send(String::from("hello from thread")).unwrap();
});

let received = rx.recv().unwrap();
println!("收到: {}", received);
```

### 13.3 共享状态：`Arc<Mutex<T>>`

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();  // 加锁
        *num += 1;
    }); // 锁在这里自动释放（RAII）
    handles.push(handle);
}

for h in handles { h.join().unwrap(); }
println!("结果: {}", *counter.lock().unwrap()); // 10
```

### 13.4 `Send` 与 `Sync`：编译期线程安全保证

- `Send`：所有权可安全地转移到另一个线程。
- `Sync`：可被多个线程同时引用（`&T` 可 Send）。

这两个是自动实现的标记 trait。`Rc` 不是 Send/Sync（计数非原子），`Arc` 是。**编译器不允许你把非线程安全的数据跨线程用**——这就是「无畏并发」（fearless concurrency）。

## 第 14 章 常用 trait 速查

| Trait | 作用 | 备注 |
|---|---|---|
| `Debug` | `{:?}` 打印 | `#[derive(Debug)]` 一把梭 |
| `Display` | `{}` 打印 | 需手写 fmt |
| `Clone` | `.clone()` 深拷贝 | 可 derive |
| `Copy` | 隐式按位复制 | 仅栈上小类型，与 Drop 互斥 |
| `Drop` | 析构（自定义清理） | 类似 RAII 的钩子 |
| `Deref` | 自定义解引用 `*x` | 智能指针的基础 |
| `Default` | `::default()` | 可 derive |
| `PartialEq/Eq` | 相等比较 | 可 derive |
| `PartialOrd/Ord` | 排序比较 | 可 derive |
| `From/Into` | 类型转换 | 实现 From 自动获得 Into |
| `Iterator` | 迭代器 | 实现 `next()` 即可 |
| `Send/Sync` | 线程安全标记 | 自动实现 |
| `AsRef<Path>` 等 | 参数多态 | 让 API 同时接受 String/&str/PathBuf |

## 第 15 章 测试

```rust
// src/lib.rs 内：单元测试
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    #[should_panic(expected = "must be positive")]
    fn it_panics() {
        do_something(-1);
    }

    #[test]
    fn it_returns_result() -> Result<(), String> {  // 用 ? 的测试
        let v = fallible_op()?;
        assert!(v > 0);
        Ok(())
    }
}
```

```
tests/           # 集成测试目录（每个文件一个独立 crate）
 └── integration_test.rs
```

```bash
cargo test              # 全部
cargo test it_works     # 按名字过滤
cargo test -- --nocapture  # 显示 println! 输出
```

---

# 附录 A：常见编译错误速查

| 错误 | 含义 | 解法 |
|---|---|---|
| `cannot move out of borrowed content` | 想从引用后面拿走所有权 | clone，或改设计返回 owned |
| `cannot borrow as mutable more than once` | 多个可变引用 | 缩短借用范围、分开使用点 |
| `borrowed value does not live long enough` | 引用的数据先 drop 了 | 调整作用域顺序、返回 owned |
| `expected &str, found String` | 类型不匹配 | `&s` 或 `s.as_str()` |
| `no method named ... found` | 缺 trait 导入 | `use xxx::Trait;` |
| `the trait bound is not satisfied` | 泛型缺少能力约束 | 加 trait bound 或实现该 trait |
| `cannot infer type` | 推导不出类型（常见于 collect） | 显式标注 `let v: Vec<_> = ...` |
| `cannot be shared between threads safely` | 类型不是 Send/Sync | Rc→Arc，RefCell→Mutex |

# 附录 B：学习路线建议

1. **第 1–3 章**（所有权/借用/生命周期）读两遍，配合 `rustlings` 对应练习全做。这是全部的地基。
2. **第 4–6 章**（struct/enum/错误处理）学完就可以写命令行小工具了。
3. **第 8、10 章**（trait、迭代器闭包）是写出「地道 Rust」的分水岭，慢即是快。
4. **第 11 章**智能指针用到再回来精读，第一遍混个脸熟即可。
5. 实战项目建议：CLI 工具（clap）→ 文件处理 → 简易 HTTP 服务 → 小型爬虫。
6. 把报错当教学：每条编译错误读懂「编译器在防什么 bug」，三个月后回头看会觉得受益无穷。

# 附录 C：速查卡片

```rust
// 所有权三问：谁拥有？借给谁？活多久？
// 借用两律：多读单写，互斥
// 字符串：参数 &str，拥有 String
// 错误：库用 Result，bug 用 panic，? 传播
// 共享：单线程 Rc<RefCell<T>>，多线程 Arc<Mutex<T>>
// 迭代：iter() 借，into_iter() 拿，iter_mut() 改
// 抽象：泛型静态快，dyn Trait 动态活
```
