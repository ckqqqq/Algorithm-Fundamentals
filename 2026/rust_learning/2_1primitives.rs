fn main(){
    let logical = true;
    let afloat = 3.14;
    let a_int=5000000000000000000i64;
    let b_int:i64 = 500000000000000000;
    let mut inferred_type = 12;//可变变量～，不过不能改变量类型
    println!("inferred_type={}",inferred_type);
    inferred_type= 1111;
    println!("inferred_type={}",inferred_type);
    let inferred_type:u32 = 12;//不可变变量
    println!("inferred_type={}",inferred_type);
    println!("logical={}",logical);
    println!("afloat={}",afloat);
    println!("a_int={}",a_int);
    println!("b_int={}",b_int);
    let my_array: [i32; 5] = [1, 2, 3, 4, 5];
    println!("my_array={:?}",my_array);// this will print the entire array ,? mean debug model,for developer, for each kind of types. 
    println!("my_array={:#?}",my_array);
    let my_tuple= (500i32, 6.4f64, 1u8);
    println!("my_tuple={:?}",my_tuple);
}