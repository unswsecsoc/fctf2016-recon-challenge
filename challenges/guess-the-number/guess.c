#include <stdio.h>

int main() {
  FILE* filein = fopen("flag.txt", "r");
  char flag[20];
  fscanf(filein, "%s", flag);

  printf("enter a number!\n");
  int number;
  scanf("%d", &number);
  if (number == 0x41) {
    printf("Nice work! Here's the flag: ");
    printf("%s", flag);
    printf("\n");
  }
  return 0;
}
