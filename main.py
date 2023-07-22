import numpy as np
import random
import math


# 涉及到了一种多臂老虎机的变体：
# 在多臂老虎机上运行，一次运行多个臂，且臂与臂之间存在着相互的影响。把“协同一定比单独运行这个臂的奖励大”作为前提条件，并且这里的臂对应“老参与者”,群组内部全为老参与者，不考虑认知水平的提高。
# 这样下来，目标就是通过程序的运行，得到程序推算的协作度与真实的协作度的差别，看看是否可行。
# 从结果来看，对整体的贡献的评判还是比较准确的。
class Bandit:
    def __init__(self, n):
        self.n = 0  # 臂的标号
        self.mu = 1  # 臂的结果均值
        self.sigma = 0.01  # 臂的结果方差

    def play(self):
        result = np.random.normal(self.mu, self.sigma, 1)  # 扳动老虎机的摇杆
        # result = self.mu
        return result


# 需要同时多个老虎机进行工作，总体可以先设置10个候选人，5个群组成员。由epsilon1来决定换下哪位群组成员，由epsilon2决定换上哪位成员。然后就是需要定义协作度！！！
# 定义一个数组，表示将要运行的老虎机的标号
# 定义一个二维矩阵，表示老虎机之间的协作度关系


def random_unit(p: float):
    return random.random() < p



def work_once(relation, work_machine, n=5):
    ans = 0
    for i in range(n):
        tmp = 0
        for j in range(n):
            if i != j:
                tmp += Bandit(work_machine[i]).play() * relation[i][j]
        ans += tmp / (n - 1)
    return ans / n

# n = 5

def assign_value(relation_amount, relation_n, work_machine, res, n=5):
    for i in range(n):
        for j in range(n):
            if i != j:
                relation_amount[work_machine[i]][work_machine[j]] += res
                relation_n[work_machine[i]][work_machine[j]] += 1



relation = np.array([[0.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 4.5],
                     [2.0, 0.0, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 1.7, 4.0],
                     [2.0, 1.7, 0.0, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 3.5],
                     [2.0, 1.7, 0.7, 0.0, 1.5, 1.5, 1.5, 1.5, 1.5, 3.0],
                     [2.0, 1.7, 0.7, 1.5, 0.0, 0.7, 0.6, 1.1, 1.5, 2.5],
                     [2.0, 1.7, 0.7, 1.5, 0.7, 0.0, 0.9, 1.2, 1.2, 2.0],
                     [2.0, 1.7, 0.7, 1.5, 0.6, 0.9, 0.0, 0.5, 1.2, 1.5],
                     [2.0, 1.7, 0.7, 1.5, 1.1, 1.2, 0.5, 0.0, 1.5, 1.0],
                     [2.0, 1.7, 0.7, 1.5, 1.5, 1.2, 1.2, 1.5, 0.0, 0.5],
                     [4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0]])  # 协作度关系-暗矩阵
epsilon = 0.9



# 这里我假设有m个候选人，n个群组成员
m, n = 10, 5
while True:
    relation_amount = np.zeros([m, m])  # 协作度总数值-明矩阵
    relation_n = np.zeros([m, m])  # 协作度尝试次数-明矩阵
    relation_pre = np.zeros([m, m])  # 协作度关系-明矩阵
    work_machine = np.arange(n)
    res = 0
    t = int(input("The turns of train: "))
    for i in range(t):
        a = random_unit(epsilon)
        if a is True:
            pos_choice = random.randint(0, n-1)
            num_choice = random.randint(0, m-1)  # 不能自己和自己协作！
            if num_choice not in work_machine:
                work_machine[pos_choice] = num_choice
        res = work_once(relation, work_machine, n)
        assign_value(relation_amount, relation_n, work_machine, res, n)

    for i in range(m):
        for j in range(m):
            if relation_n[i][j] == 0:
                relation_pre[i][j] = round(relation_amount[i][j], 3)
            else:
                relation_pre[i][j] = round(relation_amount[i][j] / relation_n[i][j], 3)
    print(relation_pre)
