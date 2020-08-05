import requests
import csv


def fetch_data(url):
    try:
        req = requests.get(url=url)
        return req.json()
    except Exception as e:
        return []


def find_id(list_apartment):

    dict_count = {}
    list_id = []
    result = {}
    try:
        for x in list_apartment:
            item = x['infor_broker']
            list_id.append(item['id'])
        list_id.sort()
        count = 1
        sum = len(list_id)

        index_of_last_id = 0
        for i in range(len(list_id) - 1):
            if list_id[i] == list_id[i + 1]:
                count += 1
            else:
                dict_count[count] = list_id[i]
                index_of_last_id = i + 1
                count = 1

        dict_count[sum - index_of_last_id+1] = list_id[index_of_last_id]
        print(dict_count)
        avg = int(sum / len(dict_count))
        for x in dict_count.keys():
            if x >= 3:
                # result.append({x:dict_count[x]})
                result[x] = dict_count[x]
        return result

    except Exception as e:
        print(e)


def show_result(list_apartment, list_result):
    result = []
    try:
        for id in list_result.keys():
            for value in list_apartment:
                if value['infor_broker']['id'] == list_result[id]:
                    result.append({'name': value['infor_broker']['name'], 'phone_number': value['phone_number'],
                                   'count_apartment': id})
                    break
        return result
    except Exception as e:
        print(e)

def write_file_csv(list_result):
    with open('./result.csv', 'w', encoding='utf8', newline='') as output_file:
        fc = csv.DictWriter(output_file, fieldnames=list_result[0].keys(), )
        fc.writeheader()
        fc.writerows(list_result)
    print('create file successfully !')


if __name__ == '__main__':
    url = 'http://localhost:1337/apartments?_limit=-1'

    list_apartment = fetch_data(url)
    list_result_id = find_id(list_apartment)
     #print(show_result(list_apartment,list_result_id))

    list_result = show_result(list_apartment, list_result_id)
    #print(list_result)
    write_file_csv(list_result)
