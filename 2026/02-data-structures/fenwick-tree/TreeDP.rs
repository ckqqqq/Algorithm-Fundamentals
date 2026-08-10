struct Fenwick{ tree:Vec<i64>}

impl Fenwick {
    fn new(n:usize)-> Self{
        Fenwick{
            tree :vec![0;n+1]
        }
    }
    fn lowbit(&self,i:usize)->usize{
        i&(!i+1)
        // 当前节点的父节点 是 i+lowbit(i)// 当前节点的子节点 是 i-lowbit(i)
    }
    fn update(&mut self, mut i:usize,delta:i64){//这里的i是下标其中，mut代表可变但是不需要值
        i+=1;
        while i<self.tree.len() && i>0 {
            self.tree[i]+=delta;
            i+=i&self.lowbit(i);
        }

    }
    fn prefix_sum(&self,mut i:usize)-> i64{//取数
        i+=1;
        let mut s=0;
        while i>0 {
            s+=self.tree[i];
            i-=i&self.lowbit(i);
        }
        s
    }
}
fn main() {
   let mut fw = Fenwick::new(10);
    fw.update(0, 5);
    fw.update(1, 3);
    fw.update(2, 2);
    println!("{}", fw.prefix_sum(2)); // 10
    println!("{}", fw.prefix_sum(3)); // 10
    println!("{}", fw.prefix_sum(1)); // 10

}