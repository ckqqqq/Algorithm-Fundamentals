fn vec_loop(input: &[i32]) -> Vec<i32> {
    // 传入数组切片的不可变借用～因为是借用，函数不能修改院士数据。
    //我们创建一个新的向量来存储结果。 
    // let mut output = Vec::new();
    // for element in input {
    //     // `element` is a reference (&i32), so dereference and multiply
    //     output.push(*element * 2);//解开引用并乘以2，将结果加到output里面
    //     //map(|x| x * 2) —— 注意这里闭包里写 x * 2 就行
    //     //等价于更加地道的写法nums.iter().map(|x|x*2)
    //     // map 的传入参数， 变量和表达式
    //     // 解引用并计算*element —— 解引用：顺着引用取出它指向的真实值 i32。 为什么要解引用？因为 &i32 * 2 没有意义（引用是"地址"，不能直接做乘法），必须先 * 拿到值。 （i32 实现了 Copy，所以 *element 实际是复制一份值，合法且便宜。）* 2 —— 值乘以 2。
    // }
    // output
    // 
    let mut output =Vec::new();
    for element in input{
        output.push(*element* 2);
    }
    output
    //不是返回引用

    // for element in input {
    //     input.push(*element * 2);
    // }
    // input
}

fn vec_map_example(input: &[i32]) -> Vec<i32> {
    // An example of collecting a vector after mapping.
    // We map each element of the `input` slice to its value plus 1.
    // If the input is `[1, 2, 3]`, the output is `[2, 3, 4]`.
    // 这是一个示例，展示了如何通过映射收集一个向量。
    // 我们将 `input` 切片中的每个元素映射为其值加 1。
    // 如果输入是 `[1, 2, 3]`，输出是 `[2, 3, 4]`。
    // input.iter().map(|element| element + 1).collect()
    // input.iter().map(|element|element+1).collect()
    input.iter().map(|element|element+1).collect()
    // iter()把切片变成迭代器，然后链式调用适配器方法，这是rust 处理集合的惯用方法
    // 代替显式for 循环+ push
    // map 接受一个闭包。 ｜element｜element+1 对每个元素做变换
    //element 的类型是&i64
    //map 本身不做任何计算直到 collect 消费它才真正执行， collect 的类型推断，。 collect 可以吧迭代器做成多个集合
    // 这里返回类型Vec<i32> 决定了collect 收集成Vec<i32>
}
//时间为数不多啦~

fn vec_map(input: &[i32]) -> Vec<i32> {
    // TODO: Here, we also want to multiply each element in the `input` slice
    // by 2, but with iterator mapping instead of manually pushing into an empty vector.
    // See the example in the function `vec_map_example` above.
    input
        .iter()
        // destructure the reference to get the i32, then multiply
        .map(|&element| element * 2)
        .collect()

    // input.iter().map(|&element|element*2).collect()    
    // input.iter().map(|&elemen|element*2).collect()
}

fn main() {
    // You can optionally experiment here.
    // println!("{}",vec_map(&[2,4,6,8,10]))

}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vec_loop() {
        let input = [2, 4, 6, 8, 10];
        let ans = vec_loop(&input);
        assert_eq!(ans, [4, 8, 12, 16, 20]);
    }

    #[test]
    fn test_vec_map_example() {
        let input = [1, 2, 3];
        let ans = vec_map_example(&input);
        assert_eq!(ans, [2, 3, 4]);
    }

    #[test]
    fn test_vec_map() {
        let input = [2, 4, 6, 8, 10];
        let ans = vec_map(&input);
        assert_eq!(ans, [4, 8, 12, 16, 20]);
    }
}
