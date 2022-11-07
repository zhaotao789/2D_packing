#pragma once
#include<vector>
#include<iostream>

using namespace std;

struct Node
{
    struct Node* parent;
    struct Node* down;    // down �Ǿ��ε��±ߵ�����
    struct Node* right;   // right �Ǿ��ε��ұߵ�����
    int used;    // �þ��οռ��Ƿ�ռ��
    int width;
    int height;
    int x;
    int y;
};

// ������ν��
Node* CreateNode(int x, int y, int w, int h);

// �����õľ��ο�
struct Block
{
    struct Node* fit;    // �ʺϸþ��ο���õ�λ�ã���Ϊ nullptr ��ʾλ�ò���
    int width;
    int height;
    int x;
    int y;
    int id;
};

// ������ο�
Block* CreateBlock(int w, int h, int i);
void PrintBlocks(vector<vector<int>> bInfo);