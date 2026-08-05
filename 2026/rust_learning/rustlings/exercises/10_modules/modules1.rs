// TODO: Fix the compiler error about calling a private function.
mod sausage_factory {//mod 声明模块，文件即模块，如果写了，rust就去找同名文件
    
    // Don't let anybody outside of this module see this!
    fn get_secret_recipe() -> String {
        String::from("Ginger")
    }

    pub fn make_sausage() {//公开的函数
        get_secret_recipe();
        println!("sausage!");
    }
}

fn main() {
    sausage_factory::make_sausage();
}
