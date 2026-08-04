fn main() {
    let mut names = vec![(1, 1), (2, 2), (2, 3), (2, 4)];
    for i in names.iter_mut() {
        match i {
            (2, 4) => *i = (2, 5),   // 修改：解引用后整体赋值
            _ => println!("非目标修改数，i={:?}", i),
        }
    }
    println!("{:?}", names); // [(1, 1), (2, 2), (2, 3), (2, 5)]
}

