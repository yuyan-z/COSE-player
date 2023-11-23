import csv
import json
import os


def form_section_data(data, routes, rd, section, field):
    result = []
    for route in routes:
        result.append(data[route + ' ' + rd + ' ' + field + str(section)])
    return result


def form_section_result(routes, rd, section, prices, sales, profits):
    result = {}
    for i, route in enumerate(routes):
        result[route + ' ' + rd + ' Price' + str(section)] = prices[i]
        result[route + ' ' + rd + ' Sale' + str(section)] = sales[i]
        result[route + ' ' + rd + ' Profit' + str(section)] = profits[i]
    return result


def read_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def write_dic(dic, csv_path):
    if os.path.exists(csv_path):
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            fieldnames = list(dic.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerows([dic])
    else:
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(dic.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([dic])
