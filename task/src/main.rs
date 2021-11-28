use std::env;
use chrono::{Datelike, NaiveDate, Weekday};

extern crate argparse;

use argparse::{ArgumentParser, StoreTrue};

use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
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
    let pattern : Vec<String> = env::args().collect();
    // println!("Task Manager");
    // println!("{:?}",pattern);
   
    let path = Path::new("/mnt/c/000/Calendar");
    let today = chrono::Utc::today();
    
    let mut week = false;
    let mut calendar =false; 
    let mut todo = false; 
    let mut ret : &str = ""; 

    {  // this block limits scope of borrows by ap.refer() method
        let mut ap = ArgumentParser::new();
        ap.set_description("Task Manager");
        ap.refer(&mut week)
            .add_option(&["-w", "--week"], StoreTrue, "Week tasks");
        ap.refer(&mut calendar)
            .add_option(&["-c","--calendar"], StoreTrue, "Calendar tasks");
        ap.refer(&mut todo)
            .add_option(&["-t","--todo"], StoreTrue, "Todo tasks");
        ap.parse_args_or_exit();
    }

    // Week
    
    let d = chrono::Utc::today();
    let w = d.iso_week().week();
    // println!("{:?}, {:?}",d,w);

    if calendar {
        let yfd = format!("{}{}",d.year(),".md");

        let fd = path.join(yfd);
        let display = path.display();
        
        println!("{:?}",fd);
        process::exit(1);
    }

    if todo {

    }
    
    if week {
        let yfd = format!("{}",d.year());
        let wfd = format!("{}{}{}","W",today.iso_week().week(),".md");

        let fd = path.join(yfd).join(wfd);
        let display = path.display();
        // println!("{:?}",display);
        // println!("{:?}",fd);
        // println!("{:?}",path.exists());
        
        // If files exists
        if !fd.exists(){
            // println!("File({:?}) is being created!",fd);
            let mut file = match File::create(&fd) {
                Err(why) => panic!("couldn't create {}: {}", display, why),
                Ok(file) => file,
            };

            let year : &str = &today.year().to_string();
            let wk : &str = &today.iso_week().week().to_string();
            let mon : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Mon).format("%A, %e %B %Y").to_string();
            let tue : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Tue).format("%A, %e %B %Y").to_string();
            let wed : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Wed).format("%A, %e %B %Y").to_string();
            let thu : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Thu).format("%A, %e %B %Y").to_string();
            let fri : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Fri).format("%A, %e %B %Y").to_string();
            let sat : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Sat).format("%A, %e %B %Y").to_string();
            let sun : &str = &NaiveDate::from_isoywd(today.year(), today.iso_week().week(), Weekday::Sun).format("%A, %e %B %Y").to_string();

            
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

            match file.write_all(text.render().unwrap().as_bytes()) {
                Err(why) => panic!("couldn't write to {}: {}", display, why),
                Ok(_) => println!("successfully wrote to {}", display),
            }
        } 
        //open with Nvim
        println!("{:?}",fd);
        process::exit(1);
    }
        

}
//https://github.com/tailhook/rust-argparse
