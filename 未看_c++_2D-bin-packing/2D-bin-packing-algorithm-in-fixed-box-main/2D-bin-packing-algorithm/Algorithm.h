#pragma once
#include "Struct.h"
#include <algorithm>

using std::max;

// �����жϾ���������������������
Node* findNode(Node* node, int w, int h);

// ���뵱ǰ���Σ�����ָÿվ���
Node* splitNode(Node* node, int w, int h);

// �����Ű��㷨
bool cmpByMaxside(vector<int> a, vector<int> b);
void SortByMaxside(vector<vector<int>>& bInfo);