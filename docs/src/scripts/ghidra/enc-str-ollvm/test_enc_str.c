#include <stdio.h>

static const unsigned char str1[] = "secret";
static const unsigned char str2[] = "hidden";

int main(void) {
  printf("%s\n", str1);
  printf("%s\n", str2);
  return 0;
}
