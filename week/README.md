# rweek Cheatsheet

## Installation
On Linux or WSL, after building the cargo `cargo build --release`, copy the task program unde the `/usr/local/bin`

## Usage
In the `.aliases` file, linked to the `.zshrc` file, the following aliases are declared :
``` 
alias week='rweek -w | xargs nvim'
alias nweek='rweek -n | xargs nvim'
alias pweek='rweek -p | xargs nvim'
alias numweek='rweek --number $1 | xargs nvim'
```

The commands are the following :
* `week` Opens/creates the current week file from Monday to Sunday
* `nweek` Opens the next week file
* `nweek` Opens the previous week file
* `nunweek arg` Opens the arg number week file
