#pragma once
#include "Algorithm.h"
#include "Struct.h"

class CBlockLayout
{
public:
    CBlockLayout() {}
    ~CBlockLayout() {}

    void Rank(vector<vector<int>>& bInfo);    // �����Ű��㷨

    void Fit(int BG_X, int BG_Y, vector<vector<int>> bInfo);    // ������������

    int getX(int id);    // ��ȡָ�� id �ľ��ο�� x ����
    int getY(int id);    // ��ȡָ�� id �ľ��ο�� y ����

private:
    vector<vector<int>> CAns;    // �Ű���
                                 // CAns ��һ�� n*3 �Ķ�ά����
                                 // ���� n ��Ԫ�طֱ��ʾ��ͬ���ο�� {x, y, id}

    int C_BG_W{ 0 };    // �������ο�Ŀ�
    int C_BG_H{ 0 };    // �������ο�ĸ�
};
