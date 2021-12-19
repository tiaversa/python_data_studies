# Enter your code here. Read input from STDIN. Print output to STDOUT
n, m = [9,27]
def add_lines(num):
    row = ''
    for i in range(num):
        row+='-'
    return row

def add_symble(num):
    row = ''
    for i in range(num):
        row+='.|.'
    return row

    
if((5<n<101)&(15<m<303)):
    line = m - 3
    symble = 1
    for i in range(n):
        row = ''
        if i==((n-1)/2):
            row+=add_lines(int((m-7)/2))
            row+='WELCOME'
            row+=add_lines(int((m-7)/2))
            print(row)
        else:
            row+=add_lines(int(line/2))
            row+=add_symble(symble)
            row+=add_lines(int(line/2))
            print(row)
            if(i<=((n-4)/2)):#problem 
                line-=6
                symble+=2
            elif(i>=((n-1)/2)):
                line+=6
                symble-=2