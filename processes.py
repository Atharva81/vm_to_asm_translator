import os
from vals import clean_lines
from push_pop import process_push_pop
from arithmetic import process_arithmetic

def initialization(filename):
    ret = ['@256', 'D=A', '@SP', 'M=D']
    ret.extend(process_call("Sys.init",0, filename, 0))
    return ret

def process_return():
    ret = [
        '@LCL', 'D=M', '@R14', 'M=D',
        '@5', 'A=D-A', 'D=M', '@R15', 'M=D',
        '@ARG', 'D=M', '@0', 'D=D+A', '@R13', 'M=D', '@SP', 'AM=M-1', 'D=M', '@R13', 'A=M', 'M=D', 
        '@ARG', 'D=M', '@SP', 'M=D+1'
    ]
    for addr in ['@THAT', '@THIS', '@ARG', '@LCL']:
        ret.extend([
            '@R14', 'AMD=M-1', 
             'D=M', 
            addr, 'M=D'
        ])
    ret.extend(['@R15', 'A=M', '0;JMP'])
    return ret

def process_function(arg1, arg2):
    ret = ['({})'.format(arg1)]
    for _ in range(int(arg2)):
        ret.extend([
             '@0', 'D=A',
            '@SP', 'A=M', 'M=D', 
            '@SP', 'M=M+1'
        ])
    
    return ret

def process_call(arg1, arg2, filename, call_count):
    new_label = '{}.RET_{}'.format(filename, call_count)
    ret = [
        '@{}'.format(new_label),
        'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'
    ]
    for address in ['@LCL', '@ARG', '@THIS', '@THAT']:
        ret.append(address)
        ret.extend(['D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1'])
    
    ret.extend(['@SP', 'D=M', '@LCL', 'M=D'])
    ret.extend(['@{}'.format(int(arg2)+5), 'D=D-A', '@ARG', 'M=D']) 
    ret.extend(['@{}'.format(arg1), '0;JMP']) 
    ret.append('({})'.format(new_label))
    return ret


def process_line(line, filename, l_no, state):
    tokens = line.strip().split()
    command = tokens[0]
    
    if len(tokens) == 1:
        if command == 'return':
            ret = process_return()
        elif command in ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'):
            ret = process_arithmetic(command, filename, l_no, state)
        else:
            raise SyntaxError("{} is not a valid command. File {}. Line {}".format(command, filename, l_no))
    
    elif len(tokens) == 2:
        if command == 'label':
            ret = ['({}{})'.format(state[2], tokens[1])]
        elif command == 'goto':
            ret = ['@{}{}'.format(state[2], tokens[1]), '0;JMP']
        elif command == 'if-goto':
            ret = ['@SP','M=M-1','A=M','D=M', '@{}{}'.format(state[2], tokens[1]), 'D;JNE']
              
    elif len(tokens) == 3:
        if command in ('push', 'pop'):
            ret = process_push_pop(*tokens, filename, l_no)
        elif command == 'call':
            ret = process_call(tokens[1], tokens[2], filename, state[1])
            state[1] += 1
        elif command == 'function':
            ret = process_function(tokens[1], tokens[2])
            state[2] = '{}$'.format(tokens[1])
        else:
            raise SyntaxError("{} is not a valid command. File {}. Line {}".format(command, filename, l_no))
    
    else:
        raise SyntaxError("{} is not a valid command. File {}. Line {}".format(command, filename, l_no))
    
    return ret

def translate_vm_to_asm(inp, outname=None):
    is_dir = False
    if os.path.isdir(inp):
        is_dir = True
        if not outname:
            if inp.endswith('/'):
                inp = inp[:-1]
            outname = '{}.asm'.format(os.path.split(inp)[-1])
            outname = os.path.join(inp, outname)
    else:
        if not outname:
            outname = '{}.asm'.format(os.path.splitext(inp)[0])
    
    output = initialization(os.path.splitext(os.path.split(outname)[-1])[0])
    if is_dir:
        for file in os.listdir(inp):
            pth = os.path.join(inp, file)
            if not os.path.isfile(pth):
                continue
            if os.path.splitext(pth)[-1] != '.vm':
                continue
            with open(pth, 'r+') as f:
                vm_code = clean_lines(f.readlines())
            
            tmp = process_file(pth)
            output.extend(tmp)
            
    else:
        output.extend(process_file(inp))
    out_str = '\n'.join(output)
    with open(outname, 'w') as f:
        f.write(out_str)

def process_file(filename):
    with open(filename, 'r+') as f:
        vm_code = clean_lines(f.readlines())
    
    filename = os.path.split(filename)[-1]
    filename = filename.replace('.vm', '')
    state = [0, 0, ''] 
    
    output = [x for i, line in enumerate(vm_code) for x in process_line(line, filename, i, state)]
    return output
