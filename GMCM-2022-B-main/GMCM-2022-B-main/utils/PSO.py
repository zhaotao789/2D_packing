import random
import numpy as np
import algo as g
from tqdm import tqdm
#随机打乱顺序，未使用粒子群优化
class PSO:
    def __init__(self,solution,M,pack_algo,heuristic,split_heuristic,rotation,sorting,sorting_heuristic,init_split):
        self.pack_algo, self.heuristic, self.split_heuristic, self.rotation, self.sorting, self.sorting_heuristic, self.init_split = pack_algo, heuristic, split_heuristic, rotation, sorting, sorting_heuristic, init_split
        self.best_solution=solution
        self.pcount =200   #迭代次数
        self.M=M
        self.init_ror=10     #初始化随机翻转粒子数
        self.sur_ratio = 0.01  #初始阈值
        self.sur_step = 0.005  #阈值步长
        self.init_ror_max = 200  # 游走长度
        self.items=self.M.items
        self.newbins = []
        self.list_length=len(solution.bestlist)
        self.list_seq = solution.bestlist
        self.init_popution()

    def computer_ratio(self):
        # 计算每个bins的利用率
        bins_rate = []
        for i in range(len(self.M.bins)):
            bin = self.M.bins[i]
            bins_rate.append(bin.free_area / bin.area)
        bins_rate = np.array(bins_rate)
        idx = np.where(bins_rate < self.sur_ratio)
        return idx

    def delete_item(self,items):
        for item in items:
            self.list_seq.remove(item.idx)
        print('还剩：'+str(len(self.list_seq))+'个订单')
    def additem(self):
        items=[]
        for item in self.items:
            if item.idx in self.list_seq:
                items.append(item)
        self.items=items
        print('新任务执行时，还有：'+str(len(self.items))+'个订单')

    def additem_seq(self,it_st):
        items=[]
        for item in it_st:
            if item in self.list_seq:
                items.append(item)
        return items

    def init_popution(self):
        count=0
        while True:
            sorting_heuristic = self.sorting_heuristic[0]
            split_heuristic = self.split_heuristic[0]
            init_split = self.init_split[0]
            heuristic = self.heuristic[0]
            idx=self.computer_ratio()
            if count%3==0:
                sorting_heuristic = self.sorting_heuristic[random.randint(0, len(self.sorting_heuristic)-1)]
                split_heuristic = self.split_heuristic[random.randint(0, len(self.split_heuristic)-1)]
                init_split = self.init_split[random.randint(0, len(self.init_split)-1)]
            count+=1
            if len(idx[0]):
                self.sur_ratio = 0.01
                for i in idx[0]:
                    self.newbins.append(self.M.bins[i])
                    self.delete_item(self.M.bins[i].items)
                self.M = g.BinManager(2440, 1220, bin_algo='bin_best_fit', pack_algo=self.pack_algo,
                                      heuristic=heuristic,
                                      split_heuristic=split_heuristic, rotation=self.rotation,
                                      rectangle_merge=False,
                                      sorting=self.sorting, sorting_heuristic=sorting_heuristic,
                                      init_split=init_split)
                self.additem()
                self.M.add_items(*self.items)
                self.M.execute()
                #self.run()
            else:
                self.sur_ratio=self.sur_ratio+self.sur_step
            if len(self.items)<=0:
                break


    def run(self):
        init_pop = []
        init_solution = []
        basic_list = self.list_seq
        self.bestfiness=len(self.M.bins)
        self.list_length=len(basic_list)
        data = self.M.items
        for i in tqdm(range(self.pcount)):
            bc = basic_list.copy()
            it_st=data.copy()
            ror_list=random.sample(self.list_seq,self.init_ror)
            ror_len=np.random.randint(-1*self.init_ror_max,self.init_ror_max,self.init_ror)
            self.M = g.BinManager(2440, 1220, bin_algo='bin_best_fit', pack_algo=self.pack_algo, heuristic=self.heuristic[0],
                             split_heuristic=self.split_heuristic, rotation=self.rotation, rectangle_merge=False,
                             sorting=self.sorting, sorting_heuristic=self.sorting_heuristic, init_split=self.init_split)
            data_ = self.M.add_items(*data)
            for j in range(len(ror_list)):
                p_=ror_list[j]
                id=np.where(np.array(self.list_seq)==p_)[0][0]
                temp=self.list_seq[id]
                p=max(0,min(self.list_length-1,id+ror_len[j]))
                bc[id]=bc[p]
                bc[p]=temp
                temp_list=it_st[id]
                it_st[id]=it_st[p]
                it_st[p]=temp_list
            init_pop.append(bc)
            self.M.items=it_st
            self.M.execute()
            init_solution.append(len(self.M.bins))
            if len(self.M.bins)<self.bestfiness:
                print(len(self.M.bins))
                break




