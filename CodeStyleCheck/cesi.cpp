# include <stdio.h>
# include <math.h> /*��ΪҪ�õ���ƽ������sqrt()������Ҫ����ͷ�ļ� math.h*/
int main(void)
{
    //������ϵ�����浽�������
    int a = 1;  // ��=������ʾ��ȣ����Ǳ�ʾ��ֵ
    int b = 2;
    int c = 1;
    double delta;   //delta��ŵ���b*b - 4*a*c��ֵ
    double x1, x2;  //�ֱ����ڴ��һԪ���η��̵�������
    delta = b*b - 4*a*c;
    if (delta > 0)
    {
        x1 = (-b + sqrt(delta)) / (2*a);
        x2 = (-b - sqrt(delta)) / (2*a);
        printf("��һԪ���η����������⣬x1 = %f, x2 = %f\n", x1, x2);
    }
    else if (0 == delta)
    {
        x1 = (-b) / (2*a);
        x2 = x1;  //���ֵ�����ұ�
        printf("��һԪ���η�����һ��Ψһ�⣬x1 = x2 = %f\n", x1);
    }
    else
    {
        printf("�޽�\n");
    }
    return 0;
}