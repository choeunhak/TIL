#�հ� �ڼ��� ����
#��� ������ ����

library(MASS)
survey

#1
WriteClap=xtabs(~W.Hnd+Clap,data=survey)
chisq.test(WriteClap)
fisher.test(WriteClap)
#ī�̽����� �׽�Ʈ�� ���� ��Ȯ���� ���� �� �ֱ� ������ fishertest�� ����Ͽ���.
#pvalue�� 0.05���� �۱⶧���� ���谡 �ִ�.
#�븳������ ä���Ѵ�.


#������ ��
#�۾��� ���¼հ� �ڼ�ĥ�� ���ΰ��� �� ���̿� ���谡 �ִ�


#2
ExerSmoke=xtabs(~Exer+Smoke,data=survey)
ExerSmoke
chisq.test(ExerSmoke)
fisher.test(ExerSmoke)
#ī�̽����� �׽�Ʈ�� ���� ��Ȯ���� ���� �� �ֱ� ������ fishertest�� ����Ͽ���.
#pvalue�� 0.05���� ũ�⶧���� ���谡 ����
#�͹������� ä���Ѵ�.

#������ ��
#��� ���� ���̿� ���谡 ����