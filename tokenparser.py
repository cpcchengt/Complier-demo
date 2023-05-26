import os
from . import tokenizer

def parser(tokens) :
    current = 0;


    def walk():
        token = tokens[current]
        if token['type'] == 'number' :
            current+=1

            return {
                'type': 'NumberLiteral',
                'value': token['value'],
            };
        


        if token['type'] == 'string':
            current+=1

            return {
                'type': 'StringLiteral',
                'value': token['value'],
            }


        if token['type'] == 'paren' and token['value'] == '(':
            current +=1 
            token = tokens[current]


            node = {
                'type': 'CallExpression',
                'name': token['value'],
                'params': [],
            };

            current +=1 
            token = tokens[current]


            while token['type'] != 'paren' or token['type'] == 'paren' and token['value'] != ')':
                node['params'].append(walk())
                token = tokens[current]


            current +=1
            return node

        raise TypeError(token['type'])

    ast = {
        'type': 'Program',
        'body': [],
    }


    while current < len(tokens):
        ast['body'].append(walk())
    
    return ast

if __name__ == "__main__":
    input = 'hello "world"'
    print(tokenizer(input))
    print(parser(tokenizer.tokenizer(input)))

