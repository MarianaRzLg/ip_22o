x = '((X - 3))'
x = x.replace(' ','')
y = list(x)
p = []
E = 0
for i in range(len(y)):
  if y[i] == '(':
    p.append(y[i])
  if y[i] == ')':
    if len(p)>0: 
      p.pop()
    else:
      print('Sintaxis incorrecta')
      E = 1
  #print(y)
if len(p) == 0 and E == 0: 
  print('Sintaxis correcta')
if len(p)> 0: 
  print('Sintaxis incorrecta')