use std::fmt;
use std::iter::repeat;

#[derive(Debug)]
struct Table {
  host_bits: u8,
  networks_expo: String,
  networks: u64,
  subnet_hosts: u64,
  subnet_hosts_expo: String,
  subnet_mask: String,
}

impl Table {
  fn new(class: char, net_bits: u8, current_iter: u8) -> Self {
    Table {
      host_bits: net_bits,
      networks_expo: Table::format_network_expo(current_iter),
      networks: Table::calc_networks(current_iter),
      subnet_hosts: Table::calc_subnet_hosts(net_bits),
      subnet_hosts_expo: Table::format_subnet_hosts_expo(net_bits),
      subnet_mask: Table::calc_subnet_mask(class, net_bits),
    }
  }

  fn format_network_expo(current_iter: u8) -> String {
    format!("2^{}", current_iter)
  }

  fn calc_networks(current_iter: u8) -> u64 {
    2_u64.pow(current_iter as u32)
  }

  fn format_subnet_hosts_expo(net_bits: u8) -> String {
    format!("2^{}-2", 32 - net_bits)
  }

  fn calc_subnet_hosts(net_bits: u8) -> u64 {
    (2_u64.pow(32 - net_bits as u32)) - 2
  }

  fn calc_subnet_mask(class: char, net_bits: u8) -> String {
    let subnet_mask: [u8; 4];

    let (net_bits, pos) = modify_net_bits_from_class(class, net_bits);
    let mut last_octet = String::new();

    for i in 0..8 {
      if i < net_bits {
        last_octet.push_str("1");
      } else {
        last_octet.push_str("0");
      }
    }
    let last_octet: u8 = u8::from_str_radix(&last_octet, 2).unwrap();
    match pos {
      2 => subnet_mask = [255, last_octet, 0, 0],
      3 => subnet_mask = [255, 255, last_octet, 0],
      4 => subnet_mask = [255, 255, 255, last_octet],
      _ => subnet_mask = [255, 255, 255, last_octet],
    }

    format!(
      "{:>3}.{:>3}.{:>3}.{:>3}",
      subnet_mask[0], subnet_mask[1], subnet_mask[2], subnet_mask[3]
    )
  }
}

impl fmt::Display for Table {
  fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
    write!(
      f,
      "|{:>12}|{:>15}|{:>15}|{:>15}|{:>15}|{:>20}|",
      self.host_bits,
      self.networks_expo,
      self.networks,
      self.subnet_hosts,
      self.subnet_hosts_expo,
      self.subnet_mask
    )
  }
}

fn modify_net_bits_from_class(class: char, net_bits: u8) -> (u8, u8) {
  if class == 'a' {
    if net_bits >= 24 {
      // subnet_mask = [255, 255, 255, 0];
      (net_bits - 24, 4)
    } else if net_bits >= 16 {
      // subnet_mask = [255, 255, 0, 0];
      (net_bits - 16, 3)
    } else {
      // subnet_mask = [255, 0, 0, 0];
      (net_bits - 8, 2)
    }
  } else if class == 'b' {
    if net_bits >= 24 {
      // subnet_mask = [255, 255, 255, 0];
      (net_bits - 24, 4)
    } else {
      // subnet_mask = [255, 255, 0, 0];
      (net_bits - 16, 3)
    }
  // Class C
  } else {
    // subnet_mask = [255, 255, 255, 0];
    (net_bits - 24, 4)
  }
}

fn main() {
  loop {
    println!("Schreibe a, b oder c");
    let mut input = String::new();
    std::io::stdin()
      .read_line(&mut input)
      .expect("Failed to read line");
    let input = input.trim().parse::<char>().expect("Expected char");
    let (net_bits, class) = match input {
      'a' => (8, 'a'),
      'b' => (16, 'b'),
      'c' => (24, 'c'),
      _ => panic!("expected char `a`, `b` or `c`"),
    };
    print_table(net_bits, class);
  }
}

fn print_table(mut net_bits: u8, class: char) {
  println!(
    "|{:>12}|{:>15}|{:>15}|{:>15}|{:>15}|{:>20}|",
    "Netz_ID-Bits", "Anzahl Netze", "Anzahl Netze", "Anzahl Hosts", "Anzahl Hosts", "Subnetzmaske"
  );
  let abgrenzung = repeat("=").take(13 + 16 * 4 + 20).collect::<String>();
  println!("|{}|", abgrenzung);
  for i in 0..=(30 - net_bits) {
    let row = Table::new(class, net_bits, i);
    println!("{}", row);
    net_bits += 1;
  }
  println!("|{}|", abgr