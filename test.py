import unittest
from complier.complier import tokenizer, parser, transformer, codeGenerator


input = '(add 2 (subtract 4 2))'
output = 'add(2, subtract(4, 2));'

tokens = [
    {'type': 'paren',  'value': '('},
    {'type': 'name',   'value': 'add'},
    {'type': 'number', 'value': '2'},
    {'type': 'paren',  'value': '('},
    {'type': 'name',   'value': 'subtract'},
    {'type': 'number', 'value': '4'},
    {'type': 'number', 'value': '2'},
    {'type': 'paren',  'value': ')'},
    {'type': 'paren',  'value': ')'}
]

ast = {
    'type': 'Program',
    'body': [{
        'type': 'CallExpression',
        'name': 'add',
        'params': [{
            'type': 'NumberLiteral',
            'value': '2'
        }, {
            'type': 'CallExpression',
            'name': 'subtract',
            'params': [{
                'type': 'NumberLiteral',
                'value': '4'
            }, {
                'type': 'NumberLiteral',
                'value': '2'
            }]
        }]
    }]
}

newAst = {
    'type': 'Program',
    'body': [{
        'type': 'ExpressionStatement',
        'expression': {
            'type': 'CallExpression',
            'callee': {
                'type': 'Identifier',
                'name': 'add'
            },
            'arguments': [{
                'type': 'NumberLiteral',
                'value': '2'
            }, {
                'type': 'CallExpression',
                'callee': {
                    'type': 'Identifier',
                    'name': 'subtract'
                },
                'arguments': [{
                    'type': 'NumberLiteral',
                    'value': '4'
                }, {
                    'type': 'NumberLiteral',
                    'value': '2'
                }]
            }]
        }
    }]
}


class TestDict(unittest.TestCase):

    def test_tokenizer(self):
        self.assertEqual(tokens, tokenizer(input), 'Tokenizer should turn `input` string into `tokens` array')

    def test_parser(self):
        self.assertEqual(ast, parser(tokens), 'Parser should turn `tokens` array into `ast`')

    def test_transformer(self):
        self.assertEqual(newAst, transformer(ast), 'Transformer should turn `ast` into a `newAst`')

    def test_codeGenerator(self):
        self.assertEqual(output, codeGenerator(newAst),  'Code Generator should turn `newAst` into `output` string')


        