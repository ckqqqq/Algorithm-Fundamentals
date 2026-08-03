#![allow(overflowing_literals)]
fn main() {
    let decimal = 65.4321_f32;
    // Error! No implicit conversion
    //let integer: u8 = decimal;
    // Explicit conversion
    let integer = decimal as u8;
    let character = integer as char;

    println!("Casting: {} -> {} -> {}", decimal, integer, character);

    // when casting any value to an unsigned type, T,
    // T::MAX + 1 is added or subtracted until the value fits into T
    println!("1000 as a u16十六进制 is: {}", 1000 as u16);//u是无符号整数， N表示位宽
    println!("1000 as a u8 is : {} and 64 {}", 1000 as u8,);//  u8 只有 8 位，最大 255，放不下 1000，Rust 的 as 转换规则是取模（模 256）：
    println!("-1 as a u8 is : {}", -1i8 as u8);//
    println!("1000 as a i16 is: {}", 1000 as i16);//有符号整数二进制
    println!("1000 as a i8 is : {}", 1000 as i8);//有符号整数二进制

    // when casting to a signed type, the (bitwise) result is the same as first casting to the corresponding unsigned type. If the most significant bit of that value is 1, then the value is negative.
    println!("128 as a i16 is: {}", 128 as i16);//有符号整数16位数
    println!("128 as a i8 is : {}", 128 as i8);//有符号整数8位数
    println!("232 as a i8 is : {}", 232 as i8);//有符号整数8位数
    
}