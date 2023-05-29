import re

def tokenizer(input):
    current = 0
    tokens = []
    while current < len(input):
        char = input[current]
        if char == '(' :
            tokens.append({'type':'paren', 'value': '('})
            current+=1
            continue
        
        if char == ')' :
            tokens.append({'type':'paren', 'value': ')'})
            current+=1
            continue
        

        WHITESPACE = r'\s'
        if re.match(WHITESPACE, char):
            current+=1
            continue

        NUMBER = r'\d'
        if re.match(NUMBER, char):
            value = ''
            while re.match(NUMBER, char):
                value += char
                current += 1
                if current < len(input):
                    char = input[current]
                else:
                    break


            
            tokens.append({'type':'number', 'value': value})
            continue

        if char == '"':
            value = ''
            current += 1
            char = input[current]
            while char != '"':
                value += char
                current += 1
                if current < len(input):
                    char = input[current]
                else:
                    break
            
            current += 1
            if current < len(input):
                char = input[current]
    
            tokens.append({'type':'string', 'value': value})
            continue
        
        LETTERS = r'[a-zA-Z]'
        if re.match(LETTERS, char):
            value = ''
            while re.match(LETTERS, char):
                value += char
                current += 1
                if current < len(input):
                    char = input[current]
                else:
                    break
            
            tokens.append({'type':'name', 'value': value})
            continue
        
        raise TypeError('I dont know what this character is: ' + char)
    return tokens


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



def traverseArray(array, parent, visitor):
    for i in array:
        traverseNode(i, parent, visitor)



def traverseNode(node, parent, visitor):
    methods = visitor.get(node['type'])

    if methods and methods['enter']:
        methods['enter'](node, parent)

    if node['type'] == 'Program':
        traverseArray(node['body'], node, visitor)
        return
    elif node['type'] == 'CallExpression':
        traverseArray(node['params'], node, visitor)
        return
    elif node['type'] == 'NumberLiteral':
        pass
    elif node['type'] == 'StringLiterall':
        return
    else:
        raise TypeError(node['type'])

    if methods and methods.get('exit'):
        methods['exit'](node, parent)

def traverser(ast, visitor):
    traverseNode(ast, None, visitor)


def number_enter(node, parent):
    parent['_context'].append({
        'type': 'NumberLiteral',
        'value': node['value'],
    })

def string_enter(node, parent):
    parent['_context'].append({
        'type': 'StringLiteral',
        'value': node['value'],
    })

def call_enter(node, parent):

    expression = {
        'type': 'CallExpression',
        'callee': {
            'type': 'Identifier',
            'name': node['name'],
        },
        'arguments': [],
    }

    node['_context'] = expression['arguments'];
    if parent['type'] != 'CallExpression':
        expression = {
            'type': 'ExpressionStatement',
            'expression': expression,
        }

    parent['_context'].append(expression);

def transformer(ast):
    newAst = {
        'type': 'Program',
        'body': []
    }

    ast['_context'] = newAst['body']

    visitor = {
        'NumberLiteral': {
            'enter': number_enter
        },
        'StringLiteral': {
            'enter': string_enter
        },
        'CallExpression': {
            'enter': call_enter
        },
    }

    traverser(ast, visitor)

    return newAst



def codeGenerator(node):
    if node['type'] == 'Program':
        return '\n'.join(map(codeGenerator, node['body']))
    elif node['type'] == 'ExpressionStatement':
        return codeGenerator(node['expression']) + ';'
    elif node['type'] == 'CallExpression':
        return codeGenerator(node['callee']) + '(' + ', '.join(map(codeGenerator, node['arguments'])) + ')'
    elif node['type'] == 'Identifier':
        return node['name']
    elif node['type'] == 'NumberLiteral':
        return node['value']
    elif node['type'] == 'StringLiteral':
        return '"' + node['value'] + '"'
    else:
        raise TypeError(node['type'])

if __name__ == "__main__":
    input = '(add 2 (subtract 4 2))'
    print(tokenizer(input))
    print(parser(tokenizer(input)))
    print(transformer(parser(tokenizer(input))))
    print(codeGenerator(transformer(parser(tokenizer(input)))))

