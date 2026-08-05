fn main() {
    let cat = ("Furry McFurson", 3.5);
    // TODO: Destructure the `cat` tuple in one statement so that the println works.
    // let /* your pattern here */ = cat;
    let (name,age)=cat;
    //rust的元祖解构，这点从python学到精髓了
    println!("{name} is {age} years old");
}
