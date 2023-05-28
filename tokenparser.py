import os
from token.tokenizer import tokenizer



def walk(tokens, current):
    token = tokens[current]
    # print('-----')
    # print(current, tokens[current])
    if token['type'] == 'number' :
        current+=1
        # print('-----')
        # print(current, tokens[current])
        return {
            'type': 'NumberLiteral',
            'value': token['value'],
        }, current
    


    if token['type'] == 'string':
        current+=1
        # print('-----')
        # print(current, tokens[current])
        return {
            'type': 'StringLiteral',
            'value': token['value'],
        }, current


    if token['type'] == 'paren' and token['value'] == '(':
        current +=1 
        # print('-----')
        # print(current, tokens[current])
        token = tokens[current]


        node = {
            'type': 'CallExpression',
            'name': token['value'],
            'params': [],
        }

        current +=1 
        # print('-----')
        # print(current, tokens[current])
        token = tokens[current]


        while token['type'] != 'paren' or token['type'] == 'paren' and token['value'] != ')':
            result, current = walk(tokens, current)
            node['params'].append(result)
            token = tokens[current]


        current +=1
        return node, current

    raise TypeError(token['type'])












def parser(tokens) :

    current = 0

    ast = {
        'type': 'Program',
        'body': [],
    }


    while current < len(tokens):
        result, current = walk(tokens, current)
        ast['body'].append(result)
    
    return ast

if __name__ == "__main__":
    input = '(add 2 (subtract 4 2))'
    print(tokenizer(input))
    print(parser(tokenizer(input)))
    print(walk(tokenizer(input),0))

