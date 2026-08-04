// 埃氏筛：找出 n 以内的所有质数
// usize 这个数据类型默认基于机器制定64位或者32位
//is_prime[x] 的下标x 必须是 usize
fn prime_sieve(n: usize) -> Vec<usize> {
    // is_prime[i] 表示 i 是否为质数，初始全为 true
    let mut is_prime = vec![true; n + 1];
    //vec![true; n + 1] 是 Rust 的快捷初始化语法，
    // 意思是：创建一个 Vec<bool>长度为 n + 1每个元素都初始化为 true
    is_prime[0] = false;
    if n >= 1 {
        is_prime[1] = false;
    }
    let mut i = 2;
    while i * i <= n {
        if is_prime[i] {
            // i 是质数，把它的所有倍数划掉
            let mut j = i * i; // 从 i*i 开始即可，更小的倍数已被划掉
            while j <= n {
                is_prime[j] = false;
                j += i;
            }
        }
        i += 1;
    }
    // 收集仍为 true 的下标
    (2..=n).filter(|&x| is_prime[x]).collect() //n
    // let mut result = Vec::new(); 等价于下面这一段代码，两者随意混用，Rust 的迭代器是"零开销抽象"，不是性能问题，纯纯taste问题
    //  for x in 2..=n {                             
    //      if is_prime[x] {                         
    //          result.push(x);                      
    //      }                                        
    //  }                  
    //"2 到 n 挨个过一遍，每个数去 is_prime 表里查一下，还是质数的 │ 留下，最后装进 Vec。
    //  .filter() 方法是迭代器适配器 ，用于从集合中选择满足特定条件的元素它使用闭包（lambda 函数）评估每个元素，该闭包返回一个布尔值（ true 表示保留该项， false 表示丢弃该项）。
}
// fn main() {
//     let numbers = vec![1, 2, 3, 4, 5, 6];
//     // .filter() takes a double reference (&&i32) here because .iter() yields &i32
//     iter()是打开遍历的开关
//     let even_numbers: Vec<&i32> = numbers
//         .iter() 
//         .filter(|&&x| x % 2 == 0) 
//         .collect(); // Transforms the iterator back into a Vector
//     let nums = vec![1, 2, 3];                                                                                               
//      let doubled: Vec<i32> = nums.iter().map(|x| x * 2).collect();
//      //                        ^^^^^^ 开启遍历（借用模式）        
//      // 打印 doubled 是 [2, 4, 6]，而 nums 还是 [1, 2, 3] 完好无损
//     println!("{:?}", even_numbers); // Output: [2, 4, 6]
// }
fn main() {
// 感叹号代表“宏”，即参数不定～
// 什么是“宏”？宏 = 编译期的代码自动生成，! 是它的调用暗号。写普通代码时把它当"功能更强的函数"用就行
    let primes = prime_sieve(50);
    println!("50 以内的质数: {:?}", primes);
    println!("共 {} 个", primes.len());
}
//性要求只有一条：                                             
                                                                  
//    • 输入：元素类型的引用（对 usize 迭代器就是 &usize，所以才有   
//      |&x| 这种拆引用写法）                                        
//    • 输出：必须是 bool                                            
                                                                  
//    ```rust                                                        
//      .filter(|&x| is_prime[x])   // ✅ 返回 bool                  
//      .filter(|&x| x)             // ❌ 编译错误：x 是 usize，不是 
//    bool                   
