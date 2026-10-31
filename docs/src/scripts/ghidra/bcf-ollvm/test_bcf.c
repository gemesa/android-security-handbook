#include <stdio.h>
#include <stdlib.h>

__attribute__((noinline)) static int mix(int a, int b) {
  int r = 0;
  for (int i = 0; i < b; i++) {
    if (i & 1)
      r += a ^ i;
    else
      r -= a & i;
  }
  return r;
}

int main(int argc, char **argv) {
  int a = argc > 1 ? atoi(argv[1]) : 7;
  int b = argc > 2 ? atoi(argv[2]) : 3;
  int r;

  if (a > b)
    r = a - b;
  else
    r = mix(a, b);

  printf("r=%d\n", r);
  return 0;
}
