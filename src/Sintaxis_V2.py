x = '((X - 3))'  #Implemnetar un stack con Clase Lista Python.. /ED.Lista
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
      break
  #print(y)
else:
    if len(p) == 0:
        print('Sintaxis correcta')
    else:
        print('Sintaxis incorrecta')