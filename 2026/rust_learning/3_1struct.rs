// struct Point {
//     x: i32,
//     y: i32,
// }
// struct Rectangle{
//     p1: Point,
//     p2: Point,
// }

#[derive(Debug)]
struct Person{
    name:String,
    age:u8,
}
struct Unit;
struct Pair(i32,f32);

#[derive(Debug)]
struct Point{
    x:f32,
    y:f32,
}

#[derive(Debug)]
struct Rectangle{
    top_left:Point,
    bottom_right:Point,
}


fn main(){
    let name = String::from("Peter");
    let age = 27;
    let peter = Person{name,age};
    println!("{:?}",peter);
    println!("peter.name={},peter.age={}",peter.name,peter.age);
    let point: Point = Point{x:0.3,y:0.4};
    let another_point: Point = point;
    // println!("{:?}",point) 无法打印，值传递
    println!("{:?}",another_point);
    let bottom_right = Point{x:4.3,..another_point};// 如果字段是String Vec 这种拥有所有权的类型，会被move走，another_point之后就失效
    println!("{:?}",bottom_right);
    println!("{:?}",another_point);
    

    println!("Rectangle: {:?}",Rectangle{top_left:Point{x:0.3,y:0.4},bottom_right:Point{x:4.3,y:4.5}});
}
