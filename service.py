import copy
import json

import requests


def get_gpa(msg):
    gp = 0
    credit = 0
    for item in msg:
        if item[6] != "任选课":
            gp = gp + item[4] * item[5]
            credit = credit + item[4]
    if credit != 0:
        return round(gp / credit, 4)
    else:
        return 0


def beautify_msg(msg):
    for item in msg:
        item[1] = "{0}({1}%)".format(item[1], 100 - item[7])
        item[2] = "{0}({1}%)".format(item[2], item[7])
    return msg


def error(msg):
    print(msg)


def get_json(url):
    headers = {
        "Host": "api.jh.zjut.edu.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.88 Safari/537.36 Edg/79.0.309.54 "
    }
    content = requests.get(url, headers=headers).content.decode().encode("GBK")
    result = json.loads(content)
    retry = 10
    while result["status"] != "success" and retry > 0:
        retry = retry - 1
        error('查询错误')
        content = requests.get(url, headers=headers).content.decode().encode("GBK")
        result = json.loads(content)
    return result


def get_score_detail(cfg):  # 返回成绩信息的res
    url = "http://api.jh.zjut.edu.cn/student/scoresDetailZf.php?ip=164&username={0}&password={1}&year={2}&term={3}". \
        format(cfg[0], cfg[1], cfg[2], cfg[3])
    score_detail = get_json(url)
    score_summary = {}
    value = {}
    for each in score_detail["msg"]:
        if not (score_summary.__contains__(each['kcmc'])):
            value.clear()
        value[each['xmblmc']] = each['成绩']
        score_summary[each['kcmc']] = copy.deepcopy(value)
    score_list = []
    for k in score_summary.items():
        score_item = [0, 0, 0, 0, 0, 0, 0, 0]  # 课程名称，平时成绩，期末成绩，总评，学分，学分绩点，是否计入,期末考占比
        score_item[0] = k[0]
        for score in k[1].items():
            if "平时" in score[0]:
                score_item[1] = score[1]
            if "期末" in score[0]:
                score_item[2] = score[1]
                score_item[7] = eval(score[0].split("(")[1].split("%")[0])
            if "总评" in score[0]:
                score_item[3] = score[1]
        score_list.append(score_item)
    return score_list


def get_gpa_info(cfg, res):  # 为res添加GPA信息
    url = "http://api.jh.zjut.edu.cn/student/scoresZf.php?ip=164&username={0}&password={1}&year={2}&term={3}". \
        format(cfg[0], cfg[1], cfg[2], cfg[3])
    score_detail = get_json(url)
    for score in score_detail["msg"]:
        for item in res:
            if item[0] == score["kcmc"]:
                item[4] = eval(score["xf"])
                item[5] = eval(score["jd"])
                item[6] = score["kcxzmc"]
    return res
