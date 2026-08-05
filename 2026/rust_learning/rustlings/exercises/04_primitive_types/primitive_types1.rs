// Booleans (`bool`)

fn main() {
    let is_morning = true;
    if is_morning {
        println!("Good morning!");
    }

    // TODO: Define a boolean variable with the name `is_evening` before the `if` statement below.
    let is_evening=!is_morning;
    // The value of the variable should be the negation (opposite) of `is_morning`.
    // let …
    if is_evening {
        println!("Good evening!");
    }
}
