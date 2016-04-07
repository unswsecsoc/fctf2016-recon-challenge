#include <stdio.h>

int main() {
  printf("enter a number!\n");
  int number;
  scanf("%d", &number);
  if (number == 0x41) {
    printf("Nice work! Here's the flag: ");
    printf("<insert flag here>");
    printf("\n");
  }
  return 0;
}
