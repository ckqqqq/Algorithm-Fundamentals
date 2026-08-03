use std::convert::From;

#[derive(Debug)]
struct Number {
    value: i32,
}
// 是 implementation（实现） 的缩写，意 
//    思是"给某个类型/特征写具体实现"。主要两种 
//    用法：      
// Rust 结构体本质只存数据，方法写到impl块里面

impl From<i32> for Number {
    fn from(item: i32) -> Self {// for 后面是结果
        Number { value: item }//标准库有一条通用规则：任何实现了 From<T> 的类型自动实现 Into<T>，不用重复劳动。 
    }//教会 Rust 怎么把 A 变成 B
}

fn main() {
    let num = Number::from(30);//                                 
    // 本质上没差别——Number 就是一个 i32 套了个壳，内 存里占的空间和 i32 一模一样（4 字节），运行时零额外开销。      
    println!("My number is {:?}", num);
    println!("My number is {:?}", std::any::type_name_of_val(&num));
}

