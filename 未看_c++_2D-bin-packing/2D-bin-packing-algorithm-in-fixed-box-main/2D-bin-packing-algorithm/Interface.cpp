#include "Interface.h"

void CBlockLayout::Rank(vector<vector<int>>& bInfo)
{
    // �����Ű��㷨
    cout << "����ǰ" << endl;
    cout << "-------------------------------------------------" << endl;
    PrintBlocks(bInfo);
    SortByMaxside(bInfo);
    cout << "�����" << endl;
    cout << "-------------------------------------------------" << endl;
    PrintBlocks(bInfo);
}

void CBlockLayout::Fit(int BG_W, int BG_H, vector<vector<int>> bInfo)
{
    C_BG_W = BG_W;
    C_BG_H = BG_H;
    vector<Block*> blocks;
    Node* root = CreateNode(0, 0, BG_W, BG_H);

    // �����̶����ο�
    for (int i = 0; i < bInfo.size(); i++)
    {
        Block* loopBlock = CreateBlock(bInfo[i][0], bInfo[i][1], bInfo[i][2]);
        blocks.push_back(loopBlock);
    }

    // �����ο������ӵ��Ű�ռ䣨������
    for (int j = 0; j < blocks.size(); j++)
    {
        Block* block = blocks[j];
        Node* node = nullptr;
        if (node = findNode(root, block->width, block->height))
        {
            block->fit = splitNode(node, block->width, block->height);
        }
    }

    // ���Ű��Ľ���洢�� CAns ��
    cout << "�Ű��������id" << endl;
    cout << "-------------------------------------------------" << endl;
    for (int k = 0; k < blocks.size(); k++)
    {
        if (blocks[k]->fit)
        {
            vector<int> tmp = { blocks[k]->fit->x, blocks[k]->fit->y, blocks[k]->id };
            CAns.push_back(tmp);
            cout << "x:" << blocks[k]->fit->x << " "
                << "y:" << blocks[k]->fit->y << " "
                << "id:" << blocks[k]->id << endl;
        }
        else
        {
            cout << "block" << k << "dont fit in board!" << endl;
        }
    }
}

int CBlockLayout::getX(int id)
{
    for (int i = 0; i < CAns.size(); i++)
    {
        if (CAns[i][2] == id)
        {
            return CAns[i][0];
        }
    }
    return INT_MIN;    // ��ʾ�Ų��¸þ���
}

int CBlockLayout::getY(int id)
{
    for (int i = 0; i < CAns.size(); i++)
    {
        if (CAns[i][2] == id)
        {
            return CAns[i][0];
        }
    }
    return INT_MIN;
}