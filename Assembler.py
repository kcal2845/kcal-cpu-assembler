print("16비트 CPU 어셈블러 (https://github.com/kcal2845/Logisim-16bit-CPU)")
f = open('./format.txt','r')
# 설정 플래그
SLASH = ':' #슬래시

# fotmat.txt에서 포맷 불러옴
instruction_format = dict() #명령어 포맷
f.readline()

while True:
    line = f.readline()
    if not line: break

    #공백, 개행 문자 제거
    line=line.replace('\n','');line=line.replace('\r\n','');line=line.replace(' ','');

    # 슬래시 기준으로 잘라서 저장
    splited=line.split(SLASH)
    
    # 포맷 추가
    instruction_format[splited[0]] = splited[1]

print('명령어 형식 등록 완료')
f.close()

# 포맷으로 어셈블
# 프로그램명 입력받기
print("프로그램명 입력:")
programLink = input()

try:
    f = open(programLink+'.txt','r')
except FileNotFoundError:
    print(programLink+" = 이런 파일이 존재하지 않습니다.")
    quit()

line = f.readline()

# 첫줄 어드래스 비트 검색
line=line.replace(' ','')
if line.find('addressbit:') == -1 :
    print('address bit를 지정해주세요.');exit()

# 어드래스 비트 저장
addressbit = int(line.split(':')[1])

# 어드래스 비트 만큼 translated 배열 선언
translated=[0]*(2**addressbit)

print(programLink+'.txt '+'어셈블리어 -> 기계어 변환...')
i = 0

while True:
    bined = '0b'
    # 명령어 읽어오기
    line = f.readline()
    if not line: break

    # 주석, 엔터 제거
    line = line[:line.find('#')]
    line=line.replace('\n','');line=line.replace('\r\n','')
    
    # 공백 기준으로 자르기
    lines = line.split(' ')

    # ORG 처리
    if lines[0] == 'ORG':
        i = int(lines[1],16)
        print("\nORG %x" %i)

    elif lines[0] != '\n' and lines[0] != '' and lines[0] != ' ':
        # 문자열 처리
        if line[0] == "[":
            print(line + '->')
            x = 1
            while True:
                if line[x] == "]": break
                character = hex(ord(line[x])).replace("0x","")
                print(str(hex(i).replace("0x",""))+": "+character)
                translated[i] = character
                x += 1
                i += 1

        # 명령어,상수 처리
        else:
            for p in range(len(lines)):
                if lines[p] != '' :
                    # 포멧에 있으면 그 값으로 변환, 숫자라면(그 이외에는) 2진수화
                    if lines[p] in instruction_format :
                        bined = bined + instruction_format[lines[p]]
                    else :
                        if lines[p].find("0b") != -1: numbers = lines[p].replace("0b","")
                        elif lines[p].find("0x") != -1: numbers = bin(int(lines[p],16)).replace("0b","")
                        else : numbers = bin(int(lines[p])).replace("0b","")
                
                        # 모자라는 0 채워주기
                        for a in range(addressbit - len(numbers)):
                            numbers = '0'+numbers
                        
                        bined = bined + numbers

            # 2진수를 10진수로 변경 후 16진수로 변경
            hexed = hex(int(bined,2)).replace("0x","")
                
            print(str(hex(i).replace("0x",""))+": "+line + ' -> ' +hexed)
            translated[i] = hexed
            i = i+1

f.close()

# text 조립
text = ''
for i in range(2**addressbit):
    text = text + str(translated[i]) + ' '

print("변환 완료")

f = open(programLink+'_Assembled.txt','w')
f.write('v2.0 raw\n')
f.write(text)
f.close()
print(programLink+"_Assembled.txt로 저장")
    

