struct Point {
    x: usize, 
    y: usize,
}
 
impl Point{
    // 关联函数
    fn new(x: usize, y: usize) -> Point{
        Point { x, y }
    }
    fn sum(&self) -> usize{
        self.x+self.y
    }
}
fn main(){
    let p=Point::new(1,2);
    let p2=Point::new(3,4);
    println!("p.sum={}",p.sum());
    println!("sum={}",p2.sum());
}

