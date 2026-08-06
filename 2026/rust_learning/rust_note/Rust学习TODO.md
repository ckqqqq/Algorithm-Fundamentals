# Rust 学习 TODO 清单

> 按优先级分四个梯队，建议逐层击破。配合 `rustlings/` 练习效果更佳。

## 第一梯队：核心中的核心（决定了你能不能写出 Rust）

- [ ] **所有权（Ownership）**：每个值有唯一所有者，离开作用域即 drop
- [ ] **借用与引用（Borrowing）**：`&T` / `&mut T`，可变引用独占、不可变可共享
- [ ] **生命周期（Lifetimes）**：`'a` 标注，理解借用检查器在防什么（悬垂引用）
- [ ] **结构体与 impl**：struct、方法、`self / &self / &mut self`
- [ ] **枚举与模式匹配**：enum、`match`、`if let`、`Option` / `Result`
- [ ] **错误处理**：`Result` + `?` 运算符，panic 与可恢复错误的边界

## 第二梯队：日常编码绕不开

- [ ] **Trait**：定义/实现、泛型约束 `T: Trait`、trait bound vs `impl Trait`
- [ ] **常用标准库类型**：`String` vs `&str`、`Vec`、`HashMap`
- [ ] **迭代器与闭包**：`map/filter/collect`、`move` 闭包
- [ ] **泛型**：泛型函数/结构体/枚举
- [ ] **智能指针**：`Box`、`Rc`、`RefCell`、内部可变性模式
- [ ] **模块系统**：`mod`、`use`、`pub`、crate 结构
- [ ] **Cargo 工程化**：依赖管理、workspace、`cargo test/clippy/fmt`

## 第三梯队：进阶，写出地道的 Rust

- [ ] **并发**：`thread`、`Arc`、`Mutex`、channel；`Send` / `Sync`
- [ ] **常用 derive / 标记 trait**：`Clone`、`Copy`、`Debug`、`Display`、`Drop`、`Deref`
- [ ] **trait 对象**：`Box<dyn Trait>`、动态分发 vs 静态分发
- [ ] **高级生命周期**：多个标注、struct 中的引用、生命周期省略规则
- [ ] **测试**：单元测试、集成测试、文档测试

## 第四梯队：按需深入

- [ ] **async/await**：`Future`、tokio 生态
- [ ] **unsafe Rust**：裸指针、FFI
- [ ] **宏**：`macro_rules!`、过程宏
- [ ] **常用生态库**：serde、thiserror / anyhow

---

## 学习建议

- 第一梯队 + 第二梯队的「迭代器与闭包」是 Rust 劝退点集中区，优先投入时间。
- 心法：编译器报错大多是在帮你堵住 C++ 里要靠经验避开的内存 bug，把 borrow checker 当教练而不是敌人。
- 练习路径：`rustlings` → The Book（官方教程）对应章节 → 自己写小项目验证。
