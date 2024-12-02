# Advent of Code 2024

## Structure
The solution for each day is found in the relevant day sub directory (i.e., day 1's solution is present in `day1/`).

## Installation
This repo uses nix, and provides a flake for the relevant tooling installation. The first time you spin up this repo, run:

```
$ nix develop
```

Followed by 
```
$ pip install -r requirements.txt
```

This repo also uses [direnv](https://direnv.net/) to be able spin up the nix shell whenever you `cd` into the repo (see the `.envrc`) file. You can whitelist the repo if you want direnv to automatically activate the nix shell when you enter the repo. 
