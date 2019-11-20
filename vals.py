def valid(line):
    line = line.strip()
    if not line:
        return False
    if line.startswith('//'):
        return False
    return True

def clean_lines(lines):
    lines = [line.strip() for line in lines]
    lines = [line.split('//')[0].strip() for line in lines if valid(line)]
    return lines