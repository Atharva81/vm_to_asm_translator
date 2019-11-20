def process_arithmetic(command, filename, l_no, state):
    ret = []
    symb = {'add':'+', 'sub':'-', 'and':'&', 'or':'|', 'neg': '-', 'not':'!', 'eq':'JNE', 'lt':'JGE', 'gt':'JLE'}
    if command in ('neg', 'not'):
        return [
            '@SP', 'A=M-1', 
            'M={}M'.format(symb.get(command)), 
        ]
    ret.extend([
        '@SP', 'AM=M-1', 
        'D=M', 'A=A-1'
    ])
    
    if command in ('add', 'sub', 'and', 'or'):
        ret.append('M=M{}D'.format(symb.get(command)))
    elif command in ('eq', 'gt', 'lt'):
        ret.extend([
            'D=M-D',
            '@FALSE_{}'.format(state[0]),
            'D;{}'.format(symb.get(command)), 
            '@SP', 'A=M-1', 'M=-1', '@CONTINUE_{}'.format(state[0]), '0;JMP', 
            '(FALSE_{})'.format(state[0]), '@SP', 'A=M-1', 'M=0',
            '(CONTINUE_{})'.format(state[0])
        ])
        state[0] += 1
    else:
        raise SyntaxError('File {}. Line {}'.format(filename, l_no))
    return ret
