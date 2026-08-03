fn main() {
    // Suffixed literals, their types are known at initialization
    let x = 1u8;
    let y = 2u32;
    let z = 3f32;

    // Unsuffixed literals, their types depend on how they are used
    let i = 1;
    let f = 1.0;

    // `size_of_val` returns the size of a variable in bytes
    println!("size of `x` in bytes: {}", std::mem::size_of_val(&x));//1字节
    println!("size of `y` in bytes: {}", std::mem::size_of_val(&y));//4字节
    println!("size of `z` in bytes: {}", std::mem::size_of_val(&z));//4字节
    println!("size of `i` in bytes: {}", std::mem::size_of_val(&i));//4字节
    println!("size of `f` in bytes: {}", std::any::type_name_of_val(&i));
    println!("size of `f` in bytes: {}", std::mem::size_of_val(&f));//8字节
}