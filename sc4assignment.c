#include <stdio.h>
int main() 
{
 int a,qty,rate,total=0,i;
 menu:
 printf("\nMENU CARD \nSelect your food.. \n\t1.pizza = 180 \n\t2.burger = 100 \n\t3.dhosa = 120  \n\t4. edli = 50 \n please enter your choice...");
 scanf("%d",&a);
 switch(a)
 {
  case 1:
    printf("\nYou have selected pizza.\n Enter the quantity :");
    scanf("%d",&qty);
    rate=180;
    total=total+(qty*rate);
    printf("\nTotal amount :%d ",total);
    
    break;
  case 2:
    printf("\nYou have selected burger.\n Enter the quantity :");
    scanf("%d",&qty);
    rate=100;
    total=total+(qty*rate);
    printf("\nTotal amount :%d \n",total);
    break;
  case 3:
    printf("\nYou have selected dhosa.\n Enter the quantity :");
    scanf("%d",&qty);
    rate=120;
    total=total+(qty*rate);
    printf("\nTotal amount :%d \n",total);
    break;
  case 4:
    printf("\nYou have selected edli.\n Enter the quantity :");
    scanf("%d",&qty);
    rate=50;
    total=total+(qty*rate);
    printf("\nTotal amount :%d \n",total);
    break;
 
  default:
    printf("\nSorry Unavailable...%d",a);
    break;
 }
 
 printf("you want any order press 1 : ");
 scanf("%d",&i);
 
 if(i==1)
 {
 	goto menu; 	
 }
 
 printf("\n total amount: %d",total);
 
return 0;
}

