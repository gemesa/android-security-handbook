#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
  int a = argc > 1 ? atoi(argv[1]) : 7;
  int b = argc > 2 ? atoi(argv[2]) : 3;
  printf("or=%d", a | b);
  return 0;
}
