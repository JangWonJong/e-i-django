import random

from domains import Member
from domains import my100, myRandom, members

class Quiz00:
    def quiz00calculator(self)-> float:
        a = my100()
        b = my100()
        opcode = ['+','-','*','/']
        ran = opcode[myRandom(0,3)]
        if ran=='+': res = a + b
        elif ran=='-': res = a - b
        elif ran=='*': res = a * b
        elif ran=='/' : res = a / b
        print(f' 출력값: {a} {ran} {b} = {res}')

        return None

    def quiz01bmi(self)-> float :
        this = Member()
        m = members[myRandom(0,23)]
        w = myRandom(40,100)
        h = myRandom(140,200)
        bmi = w / (h * h) * 10000

        if bmi >= 35:
            res = f'고도비만'
        elif bmi >= 29.9:
            res = f'중도 비만 (2단계 비만)'
        elif bmi >= 24.9:
            res = f'경도 비만 (1단계 비만)'
        elif bmi >= 22.9:
            res = f'과체중'
        elif bmi >= 22.9:
            res = f'정상'
        else:
            res = f'저체중'

        print(f'이름 : {m}, 키 : {h}, 몸무게 : {w}, BMI 상태 : {res}')
        return None

    def quiz02dice(self)->int:
        res = myRandom(1,6)
        print(f'주사위 결과는 {res}입니다')

    def quiz03rps(self)->int:
        c = myRandom(0,2)
        u = myRandom(0,2)
        r = u - c
        # 1 가위 2 바위 3 보
        rps = ['가위', '바위', '보']
        if r == 0:
            res = f'플레이어: {rps[u]} ㅣ 컴퓨터: {rps[c]} ☞ 무승부'
        elif r == -1 or r == 2:
            res = f'플레이어: {rps[u]} ㅣ 컴퓨터: {rps[c]} ☞ 패배'
        elif r == 1 or r == -2:
            res = f'플레이어: {rps[u]} ㅣ 컴퓨터: {rps[c]} ☞ 승리'

        print(f'{res}')
        return None

    def quiz04leap(self)->int:
        year = myRandom(0,3000)
        '''
        s = "윤년" if year % 4 == 0 and year % 100 != 0 else "평년"
        s2 = "윤년" if year % 400 == 0 else "평년"
        JAVA style String s = : () ? : ;
        s = (year % 4 == 0 && year % 100 != 0) ? "윤년" : (year % 400 ==0) ? "윤년" : "평년"
        
        내가 했던거
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            res = '윤년'
        else:
            res = '평년'
        '''
        #파이썬 3항연산자 활용
        s3 = "윤년" if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else "평년"
        print(f'{year}년은 {s3}입니다')
        return None

    def quiz05grade(self)->float:
        m = members[myRandom(0,23)]
        kor = myRandom(0,100)
        eng = myRandom(0,100)
        math = myRandom(0,100)
        total = kor+eng+math
        avg = total/3
        #grade = ['A','B','C','D','E','F']
        if avg >= 60 :
            res = '합격'
        else:
            res = '불합격'

        print(f'{m}의 언어점수 : {kor} 영어점수 : {eng} 수학점수 : {math}\n'
              f'총점 : {total}\n평균 : {avg}\n합격여부 : {res}')
        return None

    @staticmethod
    def quiz06member_choice()->float:
        return members[myRandom(0,23)]



    def quiz07lotto(self)->float:
        print(random.sample(range(1,46),6))
        return None

    def quiz08bank(self)->str:
        Account.main()

    def quiz09gugudan(self)->float:

        print('구구단 출력')
        for i in range(1, 10):  # 6단~9단
            for j in range(2, 6):
                print(f' {j} * {i} = {i * j}', end=" ")
            print()
        print('------------------------------------------------')
        for i in range(1, 10):  # 6단~9단
            for j in range(6, 10):
                print(f' {j} * {i} = {i * j}', end=" ")
            print('')

        '''for i in [1,6]: #2단~5단
            for j in range(1,10):
                for k in range(2,6):
                    print(f' {k} * {j} = {k*j}' ,end=" ")
                print('')
            print('------------')'''




        '''res = ''
        for i in [2, 6]:
            for j in range(1, 10):
                for k in range(0, 4):
                    res += f'{i + k} * {j} = {(i + k) * j}\t'
                res += '\n'
            res += '\n' '''

        #return print(res)



'''
은행이름은 비트은행
입금자 이름(name), 계좌번호(account_number), 금액(money) 속성값으로 계좌를 생성한다. 
계좌번호는 3자리-2자리-6자리 형태로 랜덤하게 생성된다
123-12-123456
이름 우리반 금액 랜덤
'''
class Account(object):
    def __init__(self, name, account_number, money):
        self.BANK_NAME = '비트은행'
        #self.name = Quiz00().quiz06memberChoice()
        self.name = members[myRandom(0, 23)] if name == None else name
        #self.account_number= f'{myRandom(0,1000):0>3}-{myRandom(0,100):0>2}-{myRandom(0,1000000):0>6}'
        self.account_number = self.creat_account_number() if account_number == None else account_number
        self.money = myRandom(0, 10000000) if money == None else money



    def to_string(self):
        return f'은행 : {self.BANK_NAME}\n' \
               f'입금자 : {self.name}\n' \
               f'계좌번호 : {self.account_number}\n' \
               f'금액 : {self.money}원'
               #f'계좌번호 : {account_number:0>3} - {account_number:0>2}{account_number:0>6}' \

    def creat_account_number(self):

       '''ls = [str(myRandom(0,10)) for i in range(3)]
       ls.append("-")
       ls += [str(myRandom(0,10)) for i in range(2)]
       ls.append("-")
       ls += [str(myRandom(0,10)) for i in range(6)]'''
       return "".join(['-' if i == 3 or i == 6 else str(myRandom(0, 10)) for i in range(13)])
       #return "".join([str(myRandom(0,10)) if i != 3 and i != 6 else '-'  for i in range(13)]) #랜덤값 앞으로 뺏을때

    def deposit(self):
        print(f'계좌번호 :  입금액 :  ')

    @staticmethod
    def find_account(ls, account_number):
        #return "".join([j.to_string() if j.account_number == account_number else '' for i,j in enumerate(ls)])
        for i, j in enumerate(ls):
            if j.account_number == account_number:
                return ls[i].to_string()

    @staticmethod
    def add_account(ls, account_number):
        # return "".join([j.to_string() if j.account_number == account_number else '' for i,j in enumerate(ls)])
        for i, j in enumerate(ls):
            if j.account_number == account_number:
                return ls[i].money
    @staticmethod
    def min_account(ls, account_number):
        # return "".join([j.to_string() if j.account_number == account_number else '' for i,j in enumerate(ls)])
        for i, j in enumerate(ls):
            if j.account_number == account_number:
                return ls[i].money
    @staticmethod
    def del_account(ls, account_number):
        for i, j in enumerate(ls):
            if j.account_number == account_number:
                del ls[i]

    @staticmethod
    def main():
        ls = []
        while 1 :
            menu = input('0.종료 1. 계좌개설 2.계좌목록 3.입금 4.출금 5.계좌해지 6.계좌 조회')
            if menu == '0':
                break
            if menu == '1':
                acc = Account(None,None,None)
                print(f'{acc.to_string()}...개설되었습니다.\n')
                ls.append(acc)
            elif menu == '2':
               #ab = [Account().to_string() for i in ls ]
               #print("".join([acc.to_string() for acc in ls]))
               print("".join([i.to_string() for i in ls]))
            elif menu == '3':
                print(Account.add_account(ls,input('입금할 계좌번호')) + int(input('입금액')))

            elif menu == '4':
                print(Account.min_account(ls, input('입금할 계좌번호')) - int(input('출금액')))
                '''account_number = input('입금할 계좌번호')
                mon = int(input('출금액'))
                print(Account.find_account(ls,input('입금할 계좌번호')) - int(input('출금액')))'''
            elif menu == '5':
                Account.del_account(ls, input('탈퇴할 계좌번호'))
            elif menu == '6':
                print(Account.find_account(ls, input('검색할 계좌번호')))
            else:
                print('Wrong Number.. Try Again')
                continue