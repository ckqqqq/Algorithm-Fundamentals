fn main() {
    // You can optionally experiment here.
    let a = [1, 2, 3, 4, 5];
    let nice_slice = &a[1..4];//# 数组的切片，借用数组的一部分，不是拷贝
    let python_slice = &a[a.len()-2..];//[4,5]//类型是切片引用类型：&[i32]
    // let python_slice = &a[a.len()-1..];//5 
    // let python_slice = &a[a.len()-1..];//[]
    //如果只是想复制元素到可变容器，通常用 Vec：
    println!("{:?}",nice_slice);
    assert_eq!([2, 3, 4], nice_slice);
    println!("{:?}",python_slice)
    
}

#[cfg(test)]
mod tests {
    #[test]
    fn slice_out_of_array() {
        let a = [1, 2, 3, 4, 5];
        let nice_slice = &a[1..4];

        println!("{:?}",nice_slice);

        assert_eq!([2, 3, 4], nice_slice);
    }
}