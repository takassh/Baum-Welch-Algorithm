import math
import sys
import random as r
import numpy as np

L = 30000
COUNT = 100


def make_default(length):
    rands = [r.random() for _ in range(length)]
    for i in range(len(rands)):
        rands[i] = rands[i]/sum(rands)

    return rands


def make_sample(states, tp, ep, length):
    rand = r.random()
    numbers = ""
    hiddens = ""
    if rand < 0.5:
        hiddens += "F"
        numbers += make_number(ep["F"])
    else:
        hiddens += "L"
        numbers += make_number(ep["F"])

    for _ in range(length-1):
        rand_1 = r.random()
        if rand_1 < tp[hiddens[-1]]["F"]:
            hiddens += "F"
            numbers += make_number(ep["F"])
        else:
            hiddens += "L"
            numbers += make_number(ep["L"])

    # print("実際\n{}".format(hiddens))
    return hiddens, numbers


def make_number(prob):
    rand = r.random()
    if rand < prob["1"]:
        return "1"
    rand -= prob["1"]
    if rand < prob["2"]:
        return "2"
    rand -= prob["2"]
    if rand < prob["3"]:
        return "3"
    rand -= prob["3"]
    if rand < prob["4"]:
        return "4"
    rand -= prob["4"]
    if rand < prob["5"]:
        return "5"
    rand -= prob["5"]
    if rand < prob["6"]:
        return "6"
    rand -= prob["6"]


def viterbi(observs, states, sp, tp, ep):
    T = {}
    for st in states:
        T[st] = (0 + sp[st] + ep[st][observs[0]], [st])
    for ob in observs[1:]:
        T = next_state(ob, states, T, tp, ep)

    return T


def next_state(ob, states, T, tp, ep):
    U = {}
    for next_s in states:
        U[next_s] = (-float('inf'), [])
        for now_s in states:
            p = ep[next_s][ob] + T[now_s][0] + tp[now_s][next_s]
            if p > U[next_s][0]:
                U[next_s] = [p, T[now_s][1]+[next_s]]
    return U


def forward_scaling(observs, states, sp, tp, ep):
    T = {}
    si = 0
    e = 0
    all_T = []

    # for l in states:
    #     e = ep[l][observs[0]]
    #     f = tp["F"][l]
    #     si += e*f

    # for st in states:
    #     T[st] = [0, 0]
    #     f = tp["F"][st]
    #     T[st][0] = (1/si)*ep[st][observs[0]]*f
    #     T[st][1] = si

    T["F"] = [0, 0]
    T["L"] = [0, 0]
    T["F"][0] = 1
    T["L"][0] = 0

    # all_T.append(T)

    for ob in observs:
        T = next_scale(ob, states, T, tp, ep)
        if T["F"][1] == 0 or T["L"][1] == 0:
            print(T)
        all_T.append(T)

    return all_T


def next_scale(ob, states, T, tp, ep):
    U = {}
    si = 0
    e = 0

    for l in states:
        f = 0
        e = ep[l][ob]
        for k in states:
            f += T[k][0]*tp[k][l]
        si += e*f

    for next_st in states:
        f = 0
        U[next_st] = [0, 0]
        for k in states:
            f += T[k][0]*tp[k][next_st]
        U[next_st][0] = (1/si)*ep[next_st][ob]*f
        # U[next_st][1] = T[next_st][1]*si
        U[next_st][1] = si

    return U


def backward_scaling(observed, states, tp, ep):
    T = {}
    si = 0
    all_T = []

    # for k in states:
    #     si += tp[k]["F"]*ep["F"][observed[0]]

    # for st in states:
    #     T[st] = [0, 0]
    #     f = tp[st]["F"]*ep["F"][observed[0]]
    #     T[st][0] = (1/si)*f
    #     T[st][1] = si

    T["F"] = [0, 0]
    T["L"] = [0, 0]
    T["F"][0] = 1
    T["L"][0] = 1

    all_T.insert(0, T)

    for ob in observed[1:len(observed)]:
        T = back_s(ob, states, T, tp, ep)
        if T["F"][1] == 0 or T["L"][1] == 0:
            AssertionError
        all_T.insert(0, T)
        # all_T.append(T)

    return all_T


def back_s(ob, states, T, tp, ep):
    U = {}
    si = 0
    for k in states:
        for l in states:
            si += tp[k][l]*ep[l][ob]*T[l][0]

    for back_st in states:
        f = 0
        U[back_st] = [0, 0]
        for l in states:
            f += tp[back_st][l]*ep[l][ob]*T[l][0]
        U[back_st][0] = (1/si)*f
        # U[back_st][1] = T[back_st][1]*si
        U[back_st][1] = si

    return U


def calculate(predict, real):
    array = []
    for i in range(len(real)):
        if predict[i] == real[i]:
            array.append(1)
        else:
            array.append(0)

    accuracy = sum(array)/len(array)

    # print("予測\n{}".format(predict))
    return accuracy


if __name__ == "__main__":
    f = open('observed.txt')
    observed = f.read()
    f.close()

    # accuracies = [[],[],[]]
    # for _ in range(COUNT):
    sum_s = 0
    before_s = -float("inf")
    count = 0

    # rand_e_F = make_default(6)
    # rand_e_L = make_default(6)
    # rand_a_F = make_default(2)
    # rand_a_L = make_default(2)

    states = ("F", "L")
    start_prob = {"F": 0.5, "L": 0.5}

    # predict_e = {"F":{str(i):rand_e_F[i-1]  for i in range(1, 7)},"L":{str(i):rand_e_L[i-1]   for i in range(1, 7)}}
    # predict_a = {"F": {"F": rand_a_F[0], "L": rand_a_F[1]},
    #         "L": {"F": rand_a_L[0], "L": rand_a_L[1]}}
    # print("初期a=>{}".format(predict_a))
    # print("初期e=>{}".format(predict_e))

    predict_e = {'F': {'1': 5/20, '2': 3/20, '3': 2/20, '4': 7/20, '5': 1/20, '6': 2/20},
         'L': {'1': 1/20, '2': 2/20, '3': 3/20, '4': 8/20, '5': 1/20, '6': 5/20}}
    predict_a = {"F": {"F": 0.5, "L": 0.5},
         "L": {"F": 0.5, "L": 0.5}}

    ans_e = {'F': {'1': 1/6, '2': 1/6, '3': 1/6, '4': 1/6, '5': 1/6, '6': 1/6},
             'L': {'1': 1/10, '2': 1/10, '3': 1/10, '4': 1/10, '5': 1/10, '6': 1/2}}
    ans_a = {"F": {"F": 0.95, "L": 0.05},
             "L": {"F": 0.1, "L": 0.9}}

    hiddens, observed = make_sample(states, ans_a, ans_e, L)

    while abs(sum_s-before_s) > 0.1:
        count += 1
        before_s = sum_s

        all_F = forward_scaling(observed, states,
                                start_prob, predict_a, predict_e)

        all_B = backward_scaling(''.join(list(reversed(observed))), states,
                                 predict_a, predict_e)

        assert len(all_F) == len(all_B)

        A = {"F": {"F": 0, "L": 0},
             "L": {"F": 0, "L": 0}}
        E = {"F": {str(i): 0 for i in range(1, 7)}, "L": {
            str(i): 0 for i in range(1, 7)}}

        for k in states:
            for l in states:
                for i in range(len(observed)-1):
                    # if i+1<len(observed):
                    A[k][l] += (1/all_F[i+1][l][1])*all_F[i][k][0] * \
                        predict_a[k][l]*predict_e[l][observed[i+1]]*all_B[i+1][l][0]


        for k in states:
            for i in range(len(observed)):
                E[k][observed[i]] += all_F[i][k][0]*all_B[i][k][0]


        predict_a = {"F": {"F": 0, "L": 0},
             "L": {"F": 0, "L": 0}}
        predict_e = {"F": {str(i): 0 for i in range(1, 7)}, "L": {
            str(i): 0 for i in range(1, 7)}}
        

        for k in states:
            sum_a = 0
            for l in states:
                sum_a += A[k][l]
            for l in states:
                predict_a[k][l] = A[k][l]/sum_a

        for k in states:
            sum_e = 0
            for b in range(1, 7):
                sum_e += E[k][str(b)]
            for b in range(1, 7):
                predict_e[k][str(b)] = E[k][str(b)]/sum_e

        print("{}回目".format(count))
        print(predict_a)
        print(predict_e)

        sum_s = 0
        for i in range(len(all_F)):
            sum_s += math.log(all_F[i]["F"][1])

        print("sum_s=>{}".format(sum_s))
        if sum_s-before_s >= 0:
            print("増加-----------------")
        else:
            print("減少-----------------")
            # break

    #     states = ("F", "L")
    #     start_prob = {"F": math.log(0.5), "L": math.log(0.5)}
    #     transit_prob = {"F": {"F": math.log(0.95), "L": math.log(0.05)},
    #                     "L": {"F": math.log(0.1), "L": math.log(0.9)}}
    #     emission_prob = {'F': {'1': math.log(1/6), '2': math.log(1/6), '3': math.log(1/6), '4': math.log(1/6), '5': math.log(1/6), '6': math.log(1/6)},
    #                     'L': {'1': math.log(1/10), '2': math.log(1/10), '3': math.log(1/10), '4': math.log(1/10), '5': math.log(1/10), '6': math.log(1/2)}}

    #     v = viterbi(observed, states,
    #                 start_prob, transit_prob, emission_prob)

    #     post_pi = ""
    #     for i in range(len(observed)):
    #         _pi = {"F": 0, "L": 0}
    #         for st in states:
    #             _pi[st] = all_F[i][st][0]*all_B[i][st][0]
    #         post_pi += max(_pi, key=_pi.get)

    #     viterbi_pi = ""
    #     if v["F"][1] > v["L"][1]:
    #         viterbi_pi = "".join(v["F"][1])
    #     else:
    #         viterbi_pi = "".join(v["L"][1])

    #     post_viterbi_pi = ""
    #     for i in range(len(observed)):
    #         _pi = {"F": 0, "L": 0,"FL":0,"LF":0}
    #         _pi["F"] = all_F[i]["F"][0]*all_B[i]["F"][0]
    #         _pi["FL"] = all_F[i]["F"][0]*all_B[i]["L"][0]
    #         _pi["L"] = all_F[i]["L"][0]*all_B[i]["L"][0]
    #         _pi["LF"] = all_F[i]["L"][0]*all_B[i]["F"][0]
    #         max_st = max(_pi, key=_pi.get)
    #         if max_st == "F" or max_st == "L":
    #             post_viterbi_pi += max_st
    #         else:
    #             post_viterbi_pi += viterbi_pi[i]

    #     accuracies[0].append(culculate(post_pi, hiddens))
    #     accuracies[1].append(culculate(viterbi_pi, hiddens))
    #     accuracies[2].append(culculate(post_viterbi_pi, hiddens))

    # assert len(accuracies[0])==COUNT and len(accuracies[1])==COUNT and len(accuracies[2])==COUNT
    # print("posterior 精度:{}".format(sum(accuracies[0])/COUNT))
    # print("viterbi 精度:{}".format(sum(accuracies[1])/COUNT))
    # print("post_viterbi 精度:{}".format(sum(accuracies[2])/COUNT))
