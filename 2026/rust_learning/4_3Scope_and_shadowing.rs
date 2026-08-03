fn main(){
    let long_lived_binding=1;
    let be_shadowed="kounijiwa";
    {
        let be_shadowed= true;
        let test_bool=if be_shadowed==true { true } else { false };
        println!("test_bool={}",test_bool);
        println!("inner be_shadowed={}",be_shadowed);
        let long_lived_binding=2;
        let test=1;
        println!("inner long_lived_binding={}",long_lived_binding);
    }//作用域仅限于{}内
    println!("outer long_lived_binding={}",long_lived_binding);
    println!("inner long_lived_binding={}",long_lived_binding);

    println!("be_shadowed={}",be_shadowed);

    // println!("test={}",test);//test is not in scope
}