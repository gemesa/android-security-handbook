use std::process::exit;

fn print_string(label: &str, body: String) {
    // format specifiers:
    // https://doc.rust-lang.org/std/fmt/
    println!("        ${label:12} = {body}")
}

// deadbeef -> { DE AD BE EF }
fn hex(bytes: &[u8]) -> String {
    let pairs: Vec<String> = bytes.iter().map(|b| format!("{b:02x}")).collect();
    format!("{{ {} }}", pairs.join(" "))
}

// "285735461" --> ["28", "57", "35", "46", "1?"]
fn parse_hex(val: &str) -> Option<Vec<String>> {
    let mut pairs: Vec<String> = Vec::new();
    for i in (0..val.len()).step_by(2) {
        let pair = val.get(i..(i + 2).min(val.len()))?;
        if !pair.bytes().all(|b| b.is_ascii_hexdigit()) {
            return None;
        }
        let pair = pair.to_ascii_lowercase();
        if pair.len() == 1 {
            pairs.push(format!("{pair}?"));
        } else {
            pairs.push(pair);
        }
    }
    Some(pairs)
}

/*
rule searchmem
{
    strings:
        $ascii        = "1234" ascii nocase
        $utf16_le     = { 31 00 32 00 33 00 34 00 }
        $utf16_be     = { 00 31 00 32 00 33 00 34 }
        $int32_big    = { 00 00 04 D2 }
        $int32_little = { D2 04 00 00 }
        $int64_big    = { 00 00 00 00 00 00 04 D2 }
        $int64_little = { D2 04 00 00 00 00 00 00 }
        $hex          = { 12 34 }
        $hex_reversed = { 34 12 }
    condition:
        any of them
}
*/
fn print_rule(val: &str) {
    println!("rule searchmem");
    println!("{{");
    println!("    strings:");

    print_string("ascii", format!("\"{val}\" ascii nocase"));

    let utf16_le: Vec<u8> = val.encode_utf16().flat_map(u16::to_le_bytes).collect();
    let utf16_be: Vec<u8> = val.encode_utf16().flat_map(u16::to_be_bytes).collect();

    print_string("utf16_le", hex(&utf16_le));
    print_string("utf16_be", hex(&utf16_be));

    if let Ok(n) = val.parse::<u32>() {
        print_string("int32_le", hex(&n.to_le_bytes()));
        print_string("int32_be", hex(&n.to_be_bytes()));
    }

    if let Ok(n) = val.parse::<u64>() {
        print_string("int64_le", hex(&n.to_le_bytes()));
        print_string("int64_be", hex(&n.to_be_bytes()));
    }

    if let Some(pairs) = parse_hex(val) {
        let mut rev = pairs.clone();
        rev.reverse();
        print_string("hex", format!("{{ {} }}", pairs.join(" ")));
        print_string("hex_rev", format!("{{ {} }}", rev.join(" ")));
    }

    println!("    condition:");
    println!("        any of them");
    println!("}}");
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() != 1 || args[0].is_empty() {
        println!("usage: mkrule <value>");
        println!("e.g.: mkrule 1234 > rule.yar");
        exit(1);
    }

    print_rule(&args[0]);
}
