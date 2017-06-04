# -*- coding: utf-8 -*-
# @Time  : 2017/6/1 16:31
# @Author: FSOL
# @File  : xxxx.py
import jieba
import jieba.analyse
import json

prebuilt_q = {
    '询问定义': ['有什么', '是什么', '有哪些', '指什么'],
    '询问数量': ['哪几个', '有几层', '多少'],
    '询问方法': ['用什么', '怎么'],
    '询问时间': ['什么时候', '时间是什么'],
    '询问地点': ['位置是什么', '在哪儿', '起源于'],
    '询问原因': []
}
prebuilt_a = {
    '询问定义': ['为', '是', '亦称为', '也是', '指'],
    '询问数量': ['数量词', '不少'],
    '询问方法': ['用', '以', '通过'],
    '询问时间': ['于', '在', '从', '时间词'],
    '询问地点': ['位于', '处于', '在', '到', '靠近'],
    '询问原因': ['由于', '考虑到', '因为', '由此', '因此']
}

def parse_normal(str):
    ans_list = jieba.lcut(str, cut_all=True, HMM=True)
    return ans_list


def parse_search(str):
    ans_list = jieba.lcut_for_search(str, HMM=True)
    return ans_list


def parse_TFIDF(str):
    ans_list = jieba.analyse.extract_tags(str, topK=10, withWeight=True)
    return ans_list


def parse_TextRank(str):
    ans_list = jieba.analyse.textrank(str, topK=10, withWeight=True)
    return ans_list


def luis_part(str):
    with open("que.txt", 'r') as f:
        x = f.read()
    js = json.loads(x)
    return js['topScoringIntent'], js['entities']

# ------


def i_tester(question, answers):
    intent, entities = luis_part(question)
    f1_set = []
    for answer in answers:
        if intent_test(intent['intent'], answer) == 1:
            f1_set.append(answer)
    print(f1_set)
    for entity in entities:
        if "信号词" in entity['type']:
            f2_set = []
            fro_lis = parse_search(question[:entity['startIndex']])
            aft_lis = parse_search(question[entity['endIndex']+1:])
            fin_lis = []
            if len(fro_lis) < 2:
                fin_lis.extend(fro_lis)
            else:
                fin_lis.extend(fro_lis[-2:])
            if len(aft_lis) < 2:
                fin_lis.extend(aft_lis)
            else:
                fin_lis.extend(aft_lis[:2])
            print(fin_lis)
            for answer in answers:
                flag = False
                ans_lis = parse_search(answer)
                for keyword in fin_lis:
                    if keyword in ans_lis:
                        f2_set.append(answer)
                        flag = True
                        break
                if flag:
                    break
            print(f2_set)



def intent_test(intent, answer):
    search_ans_list = parse_search(answer)
    if answer in prebuilt_a[intent]:
        return True


def tester():
    counter = 0
    for i in ask:
        flag = False
        l = parse_search(i)
        for p in l:
            for q in prebuilt_q.keys():
                if p in prebuilt_q[q]:
                    counter+=1
                    flag = True
                    break
            if flag:
                break
