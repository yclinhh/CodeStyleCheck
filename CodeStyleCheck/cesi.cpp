# include <stdio.h>
# include <math.h> /*因为要用到求平方函数sqrt()，所以要包含头文件 math.h*/
int main(void)
{
    //把三个系数保存到计算机中
    int a = 1;  // “=”不表示相等，而是表示赋值
    int b = 2;
    int c = 1;
    double delta;   //delta存放的是b*b - 4*a*c的值
    double x1, x2;  //分别用于存放一元二次方程的两个解
    delta = b*b - 4*a*c;
    if (delta > 0)
    {
        x1 = (-b + sqrt(delta)) / (2*a);
        x2 = (-b - sqrt(delta)) / (2*a);
        printf("该一元二次方程有两个解，x1 = %f, x2 = %f\n", x1, x2);
    }
    else if (0 == delta)
    {
        x1 = (-b) / (2*a);
        x2 = x1;  //左边值赋给右边
        printf("该一元二次方程有一个唯一解，x1 = x2 = %f\n", x1);
    }
    else
    {
        printf("无解\n");
    }
    return 0;
}