def process_push_pop(command, arg1, arg2, fname, l_no):
    mapping = {'local':'@LCL', 'argument':'@ARG', 'this':'@THIS','that':'@THAT', 
               'static':16, 'temp' : 5, 'pointer': 3}
    ret = []
    if arg1 == 'constant':
        if command == 'pop':
            raise SyntaxError('Can\'t change memory segment. File {}. Line {}'.format(fname, l_no))
        ret.extend([
            '@{}'.format(arg2),
        ])
    elif arg1 == 'static':
        ret.extend([
            '@{}.{}'.format(fname, arg2) 
        ])
    elif arg1 in ('temp', 'pointer'):
        if int(arg2) > 10:
            raise SyntaxError('Invalid location for segment. File {}. Line {}'.format(fname, l_no))
        ret.extend([
            '@R{}'.format(mapping.get(arg1)+int(arg2))
        ])
    elif arg1 in ('local', 'argument', 'this', 'that'):
        ret.extend([
            mapping.get(arg1), 'D=M', '@{}'.format(arg2), 'A=D+A'
        ])
    else:
        raise SyntaxError('{} is invalid memory segment. File {}. Line {}'.format(arg1, fname, l_no))
    
    if command == 'push':
        if arg1 == 'constant':
            ret.append('D=A')
        else:
            ret.append('D=M')
        ret.extend([
            '@SP', 'A=M', 'M=D',
            '@SP', 'M=M+1' 
        ])
    else:
        ret.extend(['D=A', 
            '@R13', 'M=D', 
            '@SP', 'AM=M-1',
            'D=M', 
            '@R13', 'A=M', 'M=D' 
        ])
    
    return ret