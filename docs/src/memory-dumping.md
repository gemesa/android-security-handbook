# Memory dumping

## Use case

Capture the mapped memory of a process to recover values from RAM.

## Explanation

The list of mapped regions is available through `/proc/<pid>/maps`. The content of these regions can be read via `/proc/<pid>/mem`. It is a good idea to freeze the process first, then dump the memory. For now, we only dump `rw-p` regions.

## Example

TODO

## Code

```rust
{{#include ../../src/dumpmem/src/main.rs}}
```

[View on GitHub](https://github.com/gemesa/android-security-handbook/blob/src/dumpmem/src/main.rs).
