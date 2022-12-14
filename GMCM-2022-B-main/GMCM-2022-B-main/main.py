# -*- coding: utf-8 -*-
"""
@author: MinhZou
@date: 2022-10-11
@e-mail: 770445973@qq.com
"""

import algo as g
from utils import visualizer, data_loader
from utils.solution import solution
from utils.PSO import PSO
from utils.save_results import save_to_cut_program, save_efficiency, save_to_sum_order
import time

def min_run(best_efficiency,dataset,dataset_id,less_bins,best_bin,sorting_flag,rotation_flag,init_split,sorting_heuristic,split_heuristic,heuristic):
    if dataset == 'A':
        M = g.BinManager(2440, 1220, bin_algo='bin_best_fit', pack_algo=pack_algo, heuristic=heuristic,
                         split_heuristic=split_heuristic, rotation=rotation, rectangle_merge=False,
                         sorting=sorting, sorting_heuristic=sorting_heuristic, init_split=init_split)
        data = data_loader.load_data(dataset, dataset_id)
        data = M.add_items(*data)
        M.execute()
        path = 'results/' + dataset + str(dataset_id) + '/' + pack_algo + '/' + heuristic + \
               '/' + rotation_flag + '/' + sorting_flag + '/' + split_heuristic + '/' + \
               sorting_heuristic + '/' + str(init_split)
        return M,path
    else:
        # batched_data, batch_info = data_loader.data_batched(dataset, dataset_id)
        # batched_data, batch_info = data_loader.data_batched_cluster(dataset, dataset_id)
        batched_data, batch_info = data_loader.data_batched_conditional_dbscan(dataset, dataset_id)
        print('Total batch: {}'.format(len(batch_info)))
        total_area = 0
        free_area = 0
        path = 'results/' + dataset + str(dataset_id) + '/' + pack_algo + '/' + heuristic + \
               '/' + rotation_flag + '/' + sorting_flag + '/' + split_heuristic + '/' + \
               sorting_heuristic + '/' + str(init_split)
        bin_num = 0
        for b, batch in enumerate(batched_data.items()):
            print('Processing batch {}, total sample {}'.format(b, batch_info[batch[0]]['batch_num']))
            # batch[1] refer to the data in batch
            if len(batch[1]) > 1:
                print('Something error.')
                break
            batch_data = batch[1][0]
            for k, m_data in enumerate(batch_data.items()):
                print('Processing material: {}, len: {}'.format(m_data[0], len(m_data[1])))
                M = g.BinManager(2440, 1220, bin_algo='bin_best_fit', pack_algo=pack_algo, heuristic=heuristic,
                                 split_heuristic=split_heuristic, rotation=rotation, rectangle_merge=False,
                                 sorting=sorting, sorting_heuristic=sorting_heuristic, init_split=init_split)
                data = M.add_items(*m_data[1])
                M.execute()
                ####??????????????????????????????    ??????????????????
                solu = solution(M.bins, data)
                pso = PSO(solu, M, pack_algo, heuristic, split_heuristic, rotation, sorting,
                          sorting_heuristic, init_split)
                if len(pso.newbins) <= len(M.bins):
                    M.bins = pso.newbins
                bin_num += len(M.bins)
                for i in range(len(M.bins)):
                    bins = M.bins[i].items
                    total_area += M.bins[i].bin_stats()['area']
                    free_area += M.bins[i].bin_stats()['free_area']
                    if path is not None:
                        save_to_sum_order(b, i, bins, path)
                    # floor_plan = visualizer.Visualizer()
                    # floor_plan.visualize(b, i, bins, M.bins[0].x, M.bins[0].y, prefix_path=path)
            # print(count)
        if less_bins > bin_num:
            less_bins = bin_num
        total_efficiency = (total_area - free_area) / total_area
        if total_efficiency > best_efficiency:
            best_efficiency = total_efficiency
            best_sets = '{}-{}-{}-{}-{}-{}'.format(heuristic, rotation_flag, sorting_flag,
                                                   split_heuristic, sorting_heuristic,
                                                   init_split)
        print('total_efficiency: {}'.format(total_efficiency))
        end_time = time.time()
        if path is not None:
            save_efficiency('total_efficiency: {:.4f}'.format(total_efficiency), path)
        print('Running time: {:.5f} Seconds'.format(end_time - start_time))

if __name__ == '__main__':
    start_time = time.time()
    #heuristics = ['best_area','best_short_side', 'best_long_side','worst_area','worst_short_side','worst_long_side']
    rotations = [True]
    sortings = [True]
    #split_heuristics = ['SplitSameAsPreviousAxis']    #??????????????????????????????
    #sorting_heuristics = ['DESCSS']
    #init_splits = [0]
    heuristics = ['best_area','best_long_side']
    # rotations = [True, False]
    #sortings = [True, False]
    # split_heuristics = ['SplitSameAsPreviousAxis', 'SplitShorterLeftoverAxis',
    #                     'SplitLongerLeftoverAxis', 'SplitMinimizeArea',
    #                     'SplitMaximizeArea', 'SplitShorterAxis', 'SplitLongerAxis','Split2LongerLeftoverAxis']
    #
    # sorting_heuristics = ['ASCA', 'DESCA', 'ASCSS', 'DESCSS', 'ASCLS', 'DESCLS', 'ASCPERIM', 'DESCPERIM',
    #                       'ASCDIFF', 'DESCDIFF', 'ASCRATIO', 'DESCRATIO']
    sorting_heuristics = ['DESCA', 'DESCLS', 'ASCA', 'DESCSS']
    split_heuristics = ['SplitSameAsPreviousAxis', 'Split2LongerLeftoverAxis']

    init_splits = [0,1]   #????????????????????????
    pack_algo = 'guillotine'
    dataset = 'A'
    dataset_id =1

    best_efficiency = 0
    best_sets = ''
    less_bins = 10000
    best_bin=[]
    best_path=''
    for heuristic in heuristics:
        for rotation in rotations:
            for sorting in sortings:
                for split_heuristic in split_heuristics:
                    for sorting_heuristic in sorting_heuristics:
                        for init_split in init_splits:
                            if rotation:
                                rotation_flag = 'rotated'
                            else:
                                rotation_flag = 'non_rotated'
                            if sorting:
                                sorting_flag = 'sorting'
                            else:
                                sorting_flag = 'non_sorting'
                            print('{}-{}-{}-{}-{}-{}'.format(heuristic, rotation_flag, sorting_flag,split_heuristic, sorting_heuristic, init_split))
                            M,path=min_run(best_efficiency,dataset,dataset_id,less_bins,best_bin,sorting_flag,rotation_flag,init_split,sorting_heuristic,split_heuristic,heuristic)
                            if less_bins > len(M.bins):
                                less_bins = len(M.bins)
                                best_bin = M.bins
                                best_path = path
                            total_area = 0
                            free_area = 0
                            for i in range(len(M.bins)):
                                bins = M.bins[i].items
                                total_area += M.bins[i].bin_stats()['area']
                                free_area += M.bins[i].bin_stats()['free_area']
                                # if path is not None:
                                #     save_to_cut_program(i, bins, path)
                                # ?????????
                                # floorplan = visualizer.Visualizer()
                                # floorplan.visualize(0, i, bins, M.bins[0].x, M.bins[0].y, prefix_path=path)
                            total_efficiency = (total_area - free_area) / total_area
                            if total_efficiency > best_efficiency:
                                best_efficiency = total_efficiency
                                best_sets = '{}-{}-{}-{}-{}-{}'.format(heuristic, rotation_flag, sorting_flag,
                                                                       split_heuristic, sorting_heuristic, init_split)
                            print('total_efficiency: {:.4f}'.format(total_efficiency))
                            end_time = time.time()
                            # if path is not None:
                            #     save_efficiency('total_efficiency: {:.4f}'.format(total_efficiency), path)
                            print('Running time: {:.5f} Seconds'.format(end_time - start_time))
    ###
    path=best_path
    M.bins=best_bin
    ###???????????????????????????????????????????????????    (????????????bug)
    # data = data_loader.load_data(dataset, dataset_id)
    # solu = solution(M.bins, data)
    # pso = PSO(solu, M, pack_algo, heuristics, split_heuristics, rotations[0], sortings[0], sorting_heuristics, init_splits)
    # if len(pso.newbins) <= less_bins:
    #     less_bins = len(pso.newbins)
    #     M.bins = pso.newbins
    #     best_bin = M.bins
    #     best_path = path
    for i in range(len(M.bins)):
        bins = M.bins[i].items
        # ?????????
        floorplan = visualizer.Visualizer()
        floorplan.visualize(0, i, bins, M.bins[0].x, M.bins[0].y, prefix_path=path)
    print('less_bins:', less_bins)
    print('best_efficiency:', best_efficiency)
    print('best_sets:', best_sets)
