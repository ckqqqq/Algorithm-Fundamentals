//智能推断inference；

fn main(){
    let test=5u8;
    let mut vec= Vec::new();// automatically infers the type of the vector
    vec.push(test);
    println!("vec={:?}",vec);
}