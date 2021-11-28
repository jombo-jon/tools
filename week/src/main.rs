use std::env;
use chrono::{Utc, Datelike, NaiveDate, Weekday, Duration};
use chrono::prelude::*;

extern crate argparse;

use argparse::{ArgumentParser, StoreTrue, Store};

use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::process::Command;
use std::process;

use askama::Template; // bring trait in scope

#[derive(Template)] // this will generate the code...
#[template(path = "weekly.md")] 
// #[template(source = "(Calendar)[../calendar{{ year }}.md]\n\
//                 # Week {{ week }}\n\
//                 \n\
//                 ## {{ mon }}\n\
//                 ")]

struct WeeklyTemplate<'a>{
   year: &'a str,
   week: &'a str,
   mon: &'a str,
   tue: &'a str,
   wed: &'a str,
   thu: &'a str,
   fri: &'a str,
   sat: &'a str,
   sun: &'a str,
}

fn main(){
    // println!("Task Manager");
    // println!("{:?}",pattern);
   
    let path = Path::new("/mnt/c/000/Calendar");
    
    let mut week = false;
    let mut prev =false; 
    let mut next = false;  
    let mut number = 0;  

    {  // this block limits scope of borrows by ap.refer() method
        let mut ap = ArgumentParser::new();
        ap.set_description("Week Manager");
        ap.refer(&mut week)
            .add_option(&["-w", "--week"], StoreTrue, "Current Week's tasks");
        ap.refer(&mut prev)
            .add_option(&["-p","--previous"], StoreTrue, "Previous Week's tasks");
        ap.refer(&mut next)
            .add_option(&["-n","--next"], StoreTrue, "Next Week's tasks");
        ap.refer(&mut number)
            .add_option(&["--number"], Store, "Number of the week");
        ap.parse_args_or_exit();
    }

    // Week
    let dd = chrono::Utc::today();
    let pd = dd - Duration::days(7);
    let nd = dd + Duration::days(7);

    let mut day = dd;//= format!("{}{}{}","W",dd.iso_week().week(),".md");

    if week || (!prev && !next && number == 0){
        day = dd;
    } else if prev {
        day = pd;
        // println!("{:?}",day);
    } else if next {
        day = nd;
        // println!("{:?}",day);
    } else if number > 0 && number < 54 {
        day = Utc.isoywd(dd.year(),number,Weekday::Mon);
        // println!("{:?}",day);
    } else {
        process::exit(1);
    }
    
    // For all 
    let yfd = format!("{}",day.year());
    let wfd = format!("{}{}{}","W",day.iso_week().week(),".md");

    let fd = path.join(yfd).join(wfd);
    let display = path.display();
    
    // If files exists
    if !fd.exists(){
        // println!("File({:?}) is being created!",fd);
        let mut file = std::fs::File::create(&fd).unwrap();
        // let mut file = match File::create(&fd) {
        //     Err(why) => panic!("couldn't create {}: {}", display, why),
        //     Ok(file) => file,
        // };

        let year : &str = &day.year().to_string();
        let wk : &str = &day.iso_week().week().to_string();
        let mon : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Mon).format("%A, %e %B %Y").to_string();
        let tue : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Tue).format("%A, %e %B %Y").to_string();
        let wed : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Wed).format("%A, %e %B %Y").to_string();
        let thu : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Thu).format("%A, %e %B %Y").to_string();
        let fri : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Fri).format("%A, %e %B %Y").to_string();
        let sat : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Sat).format("%A, %e %B %Y").to_string();
        let sun : &str = &NaiveDate::from_isoywd(day.year(), day.iso_week().week(), Weekday::Sun).format("%A, %e %B %Y").to_string();

        let text = WeeklyTemplate { 
                year: year,
                week: wk,
                mon: mon,
                tue: tue,
                wed: wed,
                thu: thu,
                fri: fri,
                sat: sat,
                sun: sun};

        //println!("{:?}",text.render().unwrap());
        match file.write_all(text.render().unwrap().as_bytes()) {
        // match file.write_all(text.as_bytes()) {
            Err(why) => panic!("couldn't write to {}: {}", display, why),
            Ok(_) => (),
        }
        file.flush();
        // file.close();
    }
    //open with Nvim
    println!("{:?}",fd);
    process::exit(1);
}
//https://github.com/tailhook/rust-argparse
