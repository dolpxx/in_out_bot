import json


def write():
    with open('sample/test.json', 'w') as f:
        w_data = {}
        w_data['num'] = 0
        w_data['str'] = 'Hello'
        w_data['array'] = []
        w_data['array'].append(31231)
        w_data['array'].append(2)
        w_data['array'].append(3)

        json.dump(w_data, f, indent=2)
        print('WRITE:')
        print(w_data)


def read():
    with open('sample/test.json', 'r') as f:
        r_data = json.load(f)
        print('READ')
        print(r_data)


write()
read()

# WRITE:
# {'num': 0, 'str': 'Hello', 'array': [1, 2, 3]}
# READ
# {'num': 0, 'str': 'Hello', 'array': [1, 2, 3]}
