fn main(){
    for n in 1..100{
        if n%15==0{
            println!("n={}",n);
        }
        else{
            print!("{} ",n);
        }
    }
}