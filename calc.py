def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
  while index < len(line) and line[index].isdigit():
    number += int(line[index]) * keta
    keta /= 10
    index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index

def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1

def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1

def readMult(line, index):
  token = {'type': 'MULTIPLE'}
  return token, index + 1

def readDiv(line, index):
  token = {'type': 'DIVISION'}
  return token, index + 1

def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readMult(line, index)
    elif line[index] == '/':
      (token, index) = readDiv(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens

def preevaluate(tokens):
  index = 0
  preindex = 0
  pretokens = []
  while index < len(tokens):
    if tokens[index]['type'] == 'MULTIPLE':
      pretokens[preindex-1]['number'] *= tokens[index+1]['number']
      index += 2
      while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLE':
          pretokens[preindex-1]['number'] *= tokens[index+1]['number']
          index += 2
        elif tokens[index]['type'] == 'DIVISION':
          pretokens[preindex - 1]['number'] /= tokens[index + 1]['number']
          index += 2
        else:
          break
    elif tokens[index]['type'] == 'DIVISION':
      pretokens[preindex - 1]['number'] /= tokens[index + 1]['number']
      index += 2
      while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLE':
          pretokens[preindex-1]['number'] *= tokens[index+1]['number']
          index += 2
        elif tokens[index]['type'] == 'DIVISION':
          pretokens[preindex - 1]['number'] /= tokens[index + 1]['number']
          index += 2
        else:
          break
    else:
      pretokens.insert(preindex,tokens[index])
      preindex += 1
      index += 1
  return pretokens


def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
  tokens = preevaluate(tokens)
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer

def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))

# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  # 足し算
  test("1+2")
  test("10+20")
  test("1.0+2.1")
  test("1+2.1+36")

  # 引き算
  test("2-1")
  test("1-2")
  test("20-10")
  test("10-20")
  test("2.1-1.0")
  test("1.0-2.1")
  test("1-2.1-36")

  # 掛け算
  test("1*2")
  test("10*20")
  test("1.0*2.1")
  test("1*2.1*36")

  # 割り算
  test("4/2")
  test("2/4")

  # 複合
  test("1+2.1-36")
  test("1+2.1*36")
  test("1+2.1/7")
  test("1-2.1*36")
  test("1-21/0.7")
  test("1+2.1*36/3-6")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
