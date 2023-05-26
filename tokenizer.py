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

if __name__ == "__main__":
    input = 'hello "world"'
    print(tokenizer(input))

