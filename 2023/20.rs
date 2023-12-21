use std::collections::{HashMap, VecDeque};
use std::fmt::format;
use std::io::{self, BufRead};
use std::iter;
use std::ops::BitXorAssign;

enum Module {
    Forward,
    FlipFlop(bool),
    Conjuction(Vec<bool>),
}

fn parse_module(s: &str) -> (Module, String) {
    let mut chars = s.chars();
    let first = chars.next().unwrap();
    match first {
        '%' => (Module::FlipFlop(false), chars.collect()),
        '&' => (Module::Conjuction(Vec::new()), chars.collect()),
        _ => (Module::Forward, iter::once(first).chain(chars).collect()),
    }
}

fn parse() -> HashMap<String, Vec<String>> {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());
    
    let mut symbols = HashMap::new();
    for line in lines {
        let mut parts = line.split("->");
        let input = parts.next().unwrap().trim();
        let outputs = parts.next().unwrap();
        symbols.insert(input.to_string(), outputs.split(",").map(|o| o.trim().to_owned()).collect());
    }
    symbols
}

fn lookup(name: &String, names: &Vec<String>) -> Option<usize> {
    names.iter().position(|n| n == name)
}

fn compile(symbols: &HashMap<String, Vec<String>>) -> (Vec<Vec<usize>>, Vec<Vec<usize>>, Vec<Module>, Vec<String>) {
    let mut modules = Vec::new();
    let mut names = Vec::new();

    // create all names & modules
    let mut inputs = Vec::new();
    for (symbol, _) in symbols.iter() {
        let (module, name) = parse_module(symbol);
        modules.push(module);
        names.push(name);
        inputs.push(Vec::new());
    }
    
    // add any missing targets
    for (_, output_names) in symbols.iter() {
        for name in output_names {
            if lookup(name, &names).is_none() {
                println!("Auto-creating target: {}", name);
                modules.push(Module::Forward);
                names.push(name.to_owned());
                inputs.push(Vec::new());
            }
        }
    }
    // create outputs & inputs
    let mut outputs = Vec::new();
    for (id, (name, module)) in names.iter().zip(modules.iter()).enumerate() {
        let empty = Vec::new();
        let symbol = match module {
            Module::Forward => name.clone(),
            Module::Conjuction(_) => format!("&{name}"),
            Module::FlipFlop(_) => format!("%{name}"),
        };
        let output_names = &symbols.get(&symbol).or(Some(&empty)).unwrap();
        let targets: Vec<usize> = output_names.iter().map(|name| lookup(name, &names).unwrap()).collect();
        for t in targets.iter() {
            inputs[*t].push(id);
        }
        outputs.push(targets);
    }

    // Resize conjunction modules
    for (index, module) in modules.iter_mut().enumerate() {
        if let Module::Conjuction(memory) = module {
            memory.resize(inputs[index].len(), LOW);
        }
    }

    (inputs, outputs, modules, names)
}

const LOW: bool = false;
const HIGH: bool = true;

fn push(inputs: &Vec<Vec<usize>>, outputs: &Vec<Vec<usize>>, modules: &mut Vec<Module>, start: (usize, usize, bool), names: &Vec<String>) -> [usize; 2] {
    let mut queue = VecDeque::new();
    // send start pulse
    queue.push_back(start);
    let mut counts = [0; 2];
    while let Some((from, to, pulse)) = queue.pop_front() {
        // count the pulse
        counts[pulse as usize] += 1;
        //println!("pulse {} from {} to {}", pulse, names[from], names[to]);
        println!("{} -{}-> {}", names[from], if pulse { "high" } else { "low" }, names[to]);
        match &mut modules[to] {
            Module::Forward => for output in &outputs[to] {
                queue.push_back((to, *output, pulse));
            },
            Module::FlipFlop(memory) => {
                if pulse == LOW {
                    // flip memory
                    memory.bitxor_assign(true);
                    // send pulse to all outputs
                    for output in &outputs[to] {
                        queue.push_back((to, *output, *memory));
                    }
                }
            },
            Module::Conjuction(memory) => {
                let input = inputs[to].iter().position(|input| input == &from).unwrap();
                // flip memory for input
                memory[input].bitxor_assign(true);
                let pulse = !memory.iter().all(|p| *p == HIGH);
                for output in &outputs[to] {
                    queue.push_back((to, *output, pulse));
                }
            },
        }
    }
    
    counts
}

fn main() {
    let mut symbols = parse();
    symbols.insert("button".to_string(), vec!["broadcaster".to_string()]);
    let (inputs, outputs, mut modules, names) = compile(&symbols);
    let button = lookup(&"button".to_string(), &names).unwrap();
    let broadcaster = lookup(&"broadcaster".to_string(), &names).unwrap();
    let mut total = [0; 2];
    for _ in 0..4 {
        let counters = push(&inputs, &outputs, &mut modules, (button, broadcaster, LOW), &names);
        total[0] += counters[0];
        total[1] += counters[1];
    }
    println!("{} {}", total[0], total[1]);
    println!("{}", total[0] * total[1]);
}


// too low: 791488742
