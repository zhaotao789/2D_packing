#include "Interface.h"

int main()
{
    CBlockLayout Interface;
    vector<vector<int>> bInfo = { {50, 50, 0},
                                  {250, 200, 1},
                                  {500, 200, 2},
                                  {300, 200, 3} };
    Interface.Rank(bInfo);
    Interface.Fit(700, 400, bInfo);

    cout << endl;
    cout << "idΪ3�ľ��ο��y����Ϊ��" << Interface.getY(3) << endl;
    cout << "idΪ0�ľ��ο��x����Ϊ��" << Interface.getX(0) << endl;

    return 0;
}