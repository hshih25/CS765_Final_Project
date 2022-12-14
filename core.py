import matplotlib.pyplot as plt
import pandas as pd




class CheckSampleSizeModel:
    def __init__(self, data, user_selected:dict, min_sample_size=0):
        self.min_sample_size = min_sample_size
        self.user_selected = user_selected
        self.group_column = "group_column"
        self.data = data
        self.category_dict = {
            "Sex": [1, 2],
            "Employment": [1, 2],
            "Race": [1, 2, 3],
            "Single": [1, 2, 3],
            "Age": [[0, 21], [21, 65], [65, 86]]
        }
        self.valid = False
        self.category_group = None
    
    def _build_categories(self, use_sex=False, use_employment_status=False, \
                     use_race=False, use_single=False, use_age=False):
        type_list = list()
        def helper(type_list, category_label):
            if category_label not in self.category_dict:
                raise Exception("Undefined category")
            cur_category = self.category_dict[category_label]

            if len(type_list) == 0:
                # initial group
                for i in range(len(cur_category)):
                    type_list.append({category_label: cur_category[i]})
            else: 
                dup = len(cur_category) 
                cur_len = len(type_list) 
                # extend total group
                for _ in range(dup - 1): 
                    for i in range(cur_len):
                        type_list.append(type_list[i].copy()) 

                # add additional condition
                for j in range(dup): 
                    for i in range(cur_len): 
                        type_list[j * cur_len + i][category_label] = cur_category[j]
        if use_sex:
            helper(type_list, "Sex")

        if use_employment_status:
            helper(type_list, "Employment")

        if use_race:
            helper(type_list, "Race")

        if use_single:
            helper(type_list, "Single")

        if use_age:
            helper(type_list, "Age")
        return type_list
                


    def _categorise(self, row, group_infos):
        for idx, group_info in enumerate(group_infos):
            check_group = True
            for k, v in group_info.items():
                if check_group == False:
                    break
                if k != "Age":
                    if row[k] != v:
                        check_group = False
                        break
                else:
                    if v[0] > row[k] or row[k] >= v[1]:
                        check_group = False
                        break

            if check_group:
                return idx
        return -1
    
    def validate_sample_size(self):
        use_sex, use_employment_status, use_race, use_single, use_age = \
            self.user_selected["Sex"], self.user_selected["Employment"],\
            self.user_selected["Race"], self.user_selected["Single"], self.user_selected["Age"]   
            
        self.category_group = self._build_categories(use_sex, use_employment_status, use_race, use_single, use_age)
        self.data[self.group_column] = self.data.apply(lambda row: self._categorise(row, self.category_group), axis=1)
        
        # check every group include at least minimum sample size
        check_group = self.data[self.data["group_column"] != -1].groupby(["group_column"]).count()["TUCASEID"]
        
        self.valid = True
        for group_num in check_group:
            if group_num < self.min_sample_size:
                self.valid = False
                break
        
        return {"msg": "valid"} if self.valid else {"msg": "invalid"}
    
    def get_group_data(self):
        if not self.valid:
            return {"msg": "validate sample size before getting data"}
        return {"data": self.data, "category_group": self.category_group}
        


class Vis:
    def __init__(self, data=None, category_group=None, dependent=None, bin_num=None):
        self.category_group = category_group # list from build_categories
        self.data = data
        self.dependent = dependent
        self.bin_num = bin_num
        self.group_column = "group_column"
    
    def _get_bin(self, n, col_name):
        min_ = self.data[col_name].min()
        max_ = self.data[col_name].max()
        bin_arr = []
        divi = (max_ - min_) // n
        for i in range(n + 1):
            bin_arr.append(min_ + i * divi)
        return bin_arr
    
    def _bin_categorise(self, row, g, category_name):
        for i in range(1, len(g)):
            if row[category_name] < g[i]:
                return i - 1
        
    def distribution_plot(self):
        fig_list = list()
        
        temp_data = self.data[self.data[self.group_column] != -1].copy()
        fig, axs = plt.subplots(len(self.dependent))
        
        # draw multiple plot if there are more than one dependent variable
        for plot_n in range(len(self.dependent)):
            dependent_variable = self.dependent[plot_n] #
            bin_arr = self._get_bin(self.bin_num, dependent_variable)
            
            bin_group_name = dependent_variable + "_group"
            temp_data[bin_group_name] = temp_data.apply(
                lambda row: self._bin_categorise(
                    row, bin_arr, dependent_variable), axis=1)

            # draw line chart for each group in each plot
            for idx in temp_data[self.group_column].unique():
                use_data = temp_data[temp_data[self.group_column] == idx].copy()
                use_data = use_data.groupby(
                    [bin_group_name], as_index=False).count()
                # print(len(use_data))

                if len(self.dependent) == 1:
                    axs.plot(use_data[bin_group_name], use_data["t13"])
                else:
                    axs[plot_n].plot(use_data[bin_group_name], use_data["t13"])
                    

        fig_list.append(fig)
        return fig_list
            