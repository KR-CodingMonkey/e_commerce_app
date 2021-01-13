import pymysql
import urllib.parse
from os import system
# from msvcrt import getch
from time import sleep
from datetime import datetime


##################################3
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
##########################################################

getch = _Getch()

class member:
    def __init__(self, id:str, email, pwd):
        self.id = id
        self.email = email
        self.pwd = pwd
        self.create_date = str(datetime.now())

    def __str__(self):
        return "\nID          = " + self.id + "\nEmail       = " + self.email + \
        "\nPassword    = " + self.pwd + "\nCreate Date = " + self.create_date + "\n"

class item:
    def __init__(self):
        self.product_id = ''
        self.product_name = ''
        self.product_price = 0
        self.product_qty = 0
        self.update_date = str(datetime.now())

    # 재고 증가
    def Product_Add(self, num):
        self.product_qty += num
        self.update_date = str(datetime.now())

    # 재고 감소
    def Product_Minus(self, num):
        self.product_qty -= num
        self.update_date = str(datetime.now())

def Init_Display():
    mm = 0.5;
    system('clear')

    print("┌────────────────────────────┐")
    print("└────────────────────────────┘")

    sleep(mm);
    system('clear')
    print("┌────────────────────────────┐\n")
    print("└────────────────────────────┘")
    sleep(mm);

    system('clear')
    print("┌────────────────────────────┐")
    print("        e-commerce v0.1")
    print("└────────────────────────────┘")
    sleep(mm);

def Main_Page():
    mum = 0;

    while(1):
        system('clear')
        print("┌────────────────────────────┐")
        print("        e-commerce v0.1")
        print("└────────────────────────────┘")

        mum = mum % 3;
        if mum == 0: print("\t ▶ ", end = '')
        else: print("\t ▷ ", end = '')
        print("로그인")
        if mum == 1: print("\t ▶ ", end = '')
        else: print("\t ▷ ", end = '')
        print("회원가입")
        if mum == 2: print("\t ▶ ", end = '')
        else: print("\t ▷ ", end = '')
        print("종료")

        key = ord(getch())
        if key == 27: #Special keys (arrows, f keys, ins, del, etc.)
            key = ord(getch())
            if key == 91: #Down arrow
                key = ord(getch())
                if key == 66:
                    mum += 1
                    if mum > 2: mum = 0       

                elif key == 65: #Up arrow
                    mum -= 1
                    if mum < 0: mum = 2

        elif key == 13:
            if mum == 0:
                # 로그인 메뉴 (1.관리자, 2.회원)
                Login_Page()
            elif mum == 1:
                # 회원가입 메뉴
                Singup_Page()
            else:
                # 종료
                break

def Login_Page():
    system('clear')
    print("Login page\n")

    id = input("      ID: ")
    pw = input("Password: ")

    cursor = conn.cursor()
    
    ## DB member 조회
    sql_select = """select pw from member where id = '{}'""".format(id)

    cursor.execute(sql_select)
    result = cursor.fetchone()

    # admin 계정일경우
    if id == 'admin' and pw == 'admin1234':
        cursor.close()
        Admin_Mode()

    # result값이 존재하고 회원일 경우
    elif result and result[0] == pw:
        cursor.close()
        Member_Mode(id)

    # 테이블에 존재하지 않을때
    else:
        print("아이디와 비밀번호가 일치하지 않습니다.")
        sleep(3)

        cursor.close()
        return 0

def Singup_Page():
    system('clear')
    print("-Sign up-\n")
    sleep(0.5)

    while(1):
        new_id = input("아이디: ")
        new_email = input("이메일: ")
        new_pwd = input("비밀번호: ")
        confirm_pwd = input("비밀번호 확인: ")

        if new_pwd == confirm_pwd: 

            cursor = conn.cursor()

            # 중복된 아이디가 존재한다면 다시
            sql_search = '''SELECT * FROM member where id = '{}';'''.format(new_id)  
            result = cursor.execute(sql_search)

            if result:
                print("이미 존재하는 아이디 입니다.")
                sleep(3)
                continue

            else:
                new_member = member(new_id, new_email, new_pwd)
                
                # DB member 테이블에 INSERT
                sql_insert = '''
                INSERT INTO member (id, email, pw, c_date)
                values(%s, %s, %s, %s)
                '''

                values = (new_member.id, new_member.email, new_member.pwd, new_member.create_date)
                cursor.execute(sql_insert, values)
                conn.commit()
                cursor.close()

                print("회원가입이 되었습니다.")
                print(new_member)
                sleep(5)
                break

        else:
            print("\n비밀번호를 확인해주세요!!\n")
            sleep(3)
            system('clear')
            print("-sign up-\n")

def Admin_Mode():

    # 1.전체 회원 목록 조회
    # 2.전체 주문 목록과 회원별 주문 목록을 조회할 수 있다
    # 3.상품목록에 상품을 추가할 수 있다.
    # 4.주별/월별로 가장 많은 금액을 주문한 사용자 목록을 확인할 수 있다.
    # 5.주별/월별로 가장 많이 주문된 상품 목록을 확인할 수 있다.
    mum = 0;

    while(1):    
        system('clear')
        print("┌────────────────────────────┐")
        print("    Administrator Mode v0.1")
        print("└────────────────────────────┘")

        mum = mum % 6;
        if mum == 0: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("전체회원 목록")
        if mum == 1: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '') 
        print("주문 목록")
        if mum == 2: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("상품 추가")
        if mum == 3: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("VIP고객 리스트")
        if mum == 4: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("인기 상품 리스트")
        if mum == 5: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("로그아웃\n")

        key = ord(getch())    
        if key == 27: 
            key = ord(getch())
            if key == 91:
                key = ord(getch())
                if key == 66: #Down arrow
                    mum += 1 
                    if mum > 5: mum = 0;

                elif key == 65: #Up arrow
                    mum -= 1 
                    if mum < 0: mum = 5;

        elif key == 13:
            # 전체 회원 목록
            if mum == 0:
                system("clear")
                print("-회원 목록 조회-")
                cursor = conn.cursor()
                
                # 전체 회원 조회하기
                sql_select = "SELECT * FROM member"
                cursor.execute(sql_select)
                result = cursor.fetchall()
            
                strFormat = '%-20s%-20s%-20s%-20s\n'
                strOut = strFormat % ('ID', "email", 'password', 'create_date')

                for row_data in result:
                    strOut += strFormat % (row_data[0], row_data[1], row_data[2], row_data[3])
                
                print(strOut)
                cursor.close()
                exit = input("뒤로가려면 아무키나 눌러주세요.")

            # 주문 목록
            elif mum == 1: 
                system('clear')
                cursor = conn.cursor(pymysql.cursors.DictCursor) # 딕셔너리 형태

                while True:
                    print("1: 전체 주문 목록\n2: 회원별 주문 목록")
                    num = input("원하시는 메뉴를 선택해주세요(1~2): ")

                    if num == '1':
                        system('clear')
                        print("전체 주문 목록\n")
                        sql_select = "SELECT * FROM order_list"
                        break;

                    elif num == '2':
                        system('clear')
                        member_id = input("회원의 아이디를 입력하세요: ")
                        sql_select = "SELECT * FROM order_list where memberID = '{}'".format(member_id)
                        print()
                        break;

                    else:
                        system('clear')
                        continue

                # 구매내역 조회하기
                cursor.execute(sql_select)
                select_result = cursor.fetchall()

                strFormat = '%-20s%-20s%-20s%-20s%-20s%-30s\n'
                strOut = strFormat % ('Order Number','Member ID', 'Product Name', 'Ordered Quantity', 'total Price', 'Ordered Date') + '\n'

                for row_data in select_result:
                    strOut += strFormat % (row_data['order_id'], row_data['memberID'], row_data['product_name'], row_data['order_qty'], row_data['total_price'], row_data['c_date'])
                
                print(strOut)
                exit = input("뒤로가려면 아무키나 눌러주세요.")
                cursor.close()

            # 상품 추가
            elif mum == 2:
                cursor = conn.cursor(pymysql.cursors.DictCursor) # 딕셔너리 형태
                system('clear')

                print("상품 목록\n")
                sql_select = "SELECT * FROM item"
                cursor.execute(sql_select)
                result = cursor.fetchall()
            
                strFormat = '%-20s%-20s%-20s%-20s\n'
                strOut = strFormat % ('ID', "name", 'price', 'quantity') + '\n'
                for row_data in result:
                    strOut += strFormat % (row_data['product_id'], row_data['product_name'], row_data['product_price'], row_data['product_qty'])

                print(strOut)
                cursor.close()

                while True:
                    print("새로 추가/업데이트할 상품정보를 입력하세요(exit -> q).")

                    product_id = input("상품 ID: ")
                    product_name = input("상품이름: ")
                    product_price = input("가격 : ")
                    product_qty = input("수량 : ")
                    product_update_date = datetime.now()

                    if product_id == 'q' or product_name == 'q' or product_price =='q' or product_qty == 'q':
                        break

                    try:
                        product_price = int(product_price)
                        product_qty = int(product_qty)
                    
                    except ValueError:
                        print("형식이 올바르지 않습니다.")
                        sleep(3)
                        continue
                    
                    cursor = conn.cursor()
                    sql_item_search = "select * from item where product_id = '{}'".format(product_id)
                    cursor.execute(sql_item_search)
                    search_result = cursor.fetchone()

                    if search_result:
                        cf = input("이미 있는 상품입니다. 업데이트 하시겠습니까?(y/n)")

                        if cf == 'y':
                            sql_update = "update item set product_price = {}, product_qty = {} where product_id = '{}'".format(product_price, product_qty, product_id)
                            update_result = cursor.execute(sql_update)
                            
                            if update_result:
                                print("\n업데이트 되었습니다.")
                                sleep(3)
                                conn.commit()
                             
                            else:
                                print("\n업데이트가 되지 않았습니다. 다시 시도해주세요.")
                                sleep(3)
                        cursor.close()
                        break

                    else:
                        confirm = input("확인하신 내용이 맞습니까?(y/n): ")
                        if confirm == 'y':
                            # DB 업데이트
                            # DB item 테이블에 INSERT

                            sql_insert = '''
                            INSERT INTO item (product_id, product_name, product_price, product_qty, c_date)
                            values(%s, %s, %s, %s, %s)
                            '''
                            values = (product_id, product_name, product_price, product_qty, product_update_date)
                            
                            result_insert = cursor.execute(sql_insert, values)

                            # 상품이 잘 등록 되었다면
                            if result_insert:
                                conn.commit()
                            
                                print("\n상품이 등록되었습니다.")
                                sleep(3)
                            
                            else :
                                print("\n상품등록에 실패하였습니다.")
                                sleep(3)
                            
                            cursor.close()
                            break
                    
                        # y를 누르지 않았을때
                        else:
                            print("취소 되었습니다")
                            sleep(3)
                            cursor.close()
                            break

            elif mum == 3: 

                system('clear')
                print("VIP 고객 리스트(Top 5)\n")
                cursor = conn.cursor()
                
                sql_member_total = "select memberID, sum(total_price) as total from order_list Group by memberID order by sum(total_price) desc"
                cursor.execute(sql_member_total) # 구매한 총 가격
                vip_list = cursor.fetchall()
                
                strFormat = '%-20s%-20s'
                strOut = strFormat % ('Member ID', 'total Price') + '\n\n'
                
                count = 0
                for vip in vip_list:
                    strOut += strFormat % (vip[0], vip[1]) + '\n'

                    # 상위 5종목만 표시
                    if count > 5:
                        break;
                    else:
                        count += 1
                
                print(strOut)
                exit = input("뒤로가려면 아무키나 누르세요.\n")
                cursor.close()

            elif mum == 4: 
                system('clear')
                print("인기 상품 리스트(Top 5)")
                cursor = conn.cursor()
                
                sql_member_total = "select item_id, sum(order_qty) as total_qty from order_list Group by item_id order by sum(order_qty) desc"
                cursor.execute(sql_member_total) # 구매한 총 가격
                best_list = cursor.fetchall()
                
                strFormat = '%-20s%-20s'
                strOut = strFormat % ('Item ID','sold quantity') + '\n\n'

                count = 0
                for best in best_list:
                    strOut += strFormat % (best[0], best[1]) + '\n'
                    
                    # 상위 5종목만 표시
                    if count > 5:
                        break;
                    else:
                        count += 1


                print(strOut)
                exit = input("뒤로가려면 아무키나 누르세요.\n")
                cursor.close()

            else:
                # 로그아웃
                break

def Member_Mode(id:str):
    mum = 0
    while(1):    
        system('clear')
        print("┌─────────────────────────────┐")
        print("        Member Mode v0.1")
        print("└─────────────────────────────┘")

        mum = mum % 4;
        if mum == 0: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("상품 목록 조회")
        if mum == 1: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '') 
        print("주문한 상품 조회")
        if mum == 2: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("나의 정보")
        if mum == 3: print("\t▶ ", end = '')
        else: print("\t▷ ", end = '')
        print("로그아웃\n")

        key = ord(getch())    
        if key == 27: 
            key = ord(getch())
            if key == 91 :
                key = ord(getch())
                if key == 66: #Down arrow
                    mum += 1 
                    if mum > 3: mum = 0;

                elif key == 65: #Up arrow
                    mum -= 1 
                    if mum < 0: mum = 3;

        elif key == 13:
            if mum == 0:
                
                cursor = conn.cursor(pymysql.cursors.DictCursor) # 딕셔너리 형태

                while True:
                    system('clear')

                    print("상품 목록\n")
                    sql_select = "SELECT * FROM item"
                    cursor.execute(sql_select)
                    result = cursor.fetchall()
                
                    strFormat = '%-20s%-20s%-20s%-20s\n'
                    strOut = strFormat % ('ID', "name", 'price', 'quantity') + '\n'
                    for row_data in result:
                        strOut += strFormat % (row_data['product_id'], row_data['product_name'], row_data['product_price'], row_data['product_qty'])

                    print(strOut)
 
                    # fix-it
                    print("상품 구매")
                    order_product_id = input("제품번호(exit -> q): ")  # 주문할 제품번호
                    if order_product_id == 'q':
                        break
                    
                    try:
                        order_product_qty = int(input("제품 수량: ")) # 주문할 제품수량
                    
                    except ValueError:
                        print("숫자를 입력해주세요!!")
                        sleep(4)
                        continue
                        
                    # 상품 재고 조회
                    sql_item_search = "SELECT * FROM item where product_id = '{}'".format(order_product_id)
                    cursor.execute(sql_item_search)
                    search_result = cursor.fetchone() # 회원이 고른 상품 정보

                    if not search_result:
                        print("존재하지 않는 상품입니다.")
                        sleep(3)
                        continue

                    extra_qty = search_result['product_qty'] - order_product_qty # DB 남는 재고

                    if extra_qty >= 0:
                        total_price = order_product_qty * search_result['product_price']
                        print("Total price : %d" % total_price)
                        cf = input("정말로 구매하시겠습니까?(y/n): ")

                        if cf == 'y':
                            # item update
                            sql_item_update = "update item set product_qty = {0} \
                                where product_id = '{1}'".format(extra_qty, order_product_id)
                            update_result = cursor.execute(sql_item_update)

                            # order_list update
                            sql_orderList_insert = "insert into order_list(memberID, item_id, product_name, order_qty,total_price,c_date)\
                                 values(%s, %s, %s, %s, %s, %s)"
                            values = (id, order_product_id, search_result['product_name'],order_product_qty, total_price, datetime.now())
                            insert_result = cursor.execute(sql_orderList_insert, values)
    
                            if update_result and insert_result:
                                print("구매가 완료되었습니다.")
                                conn.commit()
                                sleep(3)
                            else:
                                print("주문이 정상처리 되지 않았습니다. 다시 시도해주세요")
                                sleep(3)

                        else:
                            print("주문이 취소되었습니다.")
                            sleep(3)
                                
                    else:
                        # 재고 부족시
                        print("재고가 부족합니다.")
                        sleep(3)

                    break;

                cursor.close()                
                    
            elif mum == 1: 
                system('clear')
                print("구매 내역\n")
                cursor = conn.cursor(pymysql.cursors.DictCursor) # 딕셔너리 형태

                # 구매내역 조회하기
                sql_select = "SELECT * FROM order_list where memberID = '{}'".format(id)
                cursor.execute(sql_select)
                select_result = cursor.fetchall()

                strFormat = '%-20s%-20s%-20s%-20s%-30s\n'
                strOut = strFormat % ('Order Number','Product Name', 'Ordered Quantity', 'total Price', 'Ordered Date') + '\n'

                for row_data in select_result:
                    strOut += strFormat % (row_data['order_id'], row_data['product_name'], row_data['order_qty'], row_data['total_price'], row_data['c_date'])
                
                print(strOut)
                exit = input("\n뒤로가려면 아무키나 눌러주세요.")
                cursor.close()

            elif mum == 2: 
                system('clear')
                print("나의 정보\n")
                cursor = conn.cursor()

                sql_select = "select * from member where id = '{}'".format(id)

                cursor.execute(sql_select)
                result = cursor.fetchone()

                # 개인정보 출력
                strFormat = '%-20s%-20s%-20s%-20s\n'
                strOut = strFormat % ('ID', "email", 'password', 'create_date')
                strOut += '\n' + strFormat % (result[0], result[1], result[2], result[3])
                print(strOut)

                change_info = input("1) 회원정보 변경\n2) 회원탈퇴\n3) 나가기\n\n원하시는 작업을 선택해주세요(1~3): ")
                
                # 나의 정보 수정하기
                if change_info == '1':
                    while True:
                        system('clear')
                        print("-나의 정보-")
                        print(strOut)

                        print("1) ID \n2) email \n3) password \n4) 나가기")
                        num = input("\n변경하고 싶은 나의정보를 선택하세요(1~3): ")

                        if num == '1':
                            new_id = input("새로운 아이디를 입력하세요: ")
                            sql_select = "select * from member where id = '{}'".format(new_id)
                            
                            # 새로운 ID 가능 여부 조회
                            cursor.execute(sql_select)
                            isExist = cursor.fetchall()

                            if isExist:
                                print("이미 존재하는 아이디 입니다.")
                                sleep(3)

                            else:
                                sql_update = "update member set id = '{}' where id = '{}'".format(new_id, id)
                                result_update = cursor.execute(sql_update)

                                # 구매내역 아이디 바꿔주기
                                sql_orderList_update = "update order_list set memberID = '{}' where memberID = '{}'".format(new_id, id)
                                result_orderList_update = cursor.execute(sql_orderList_update)

                                # if result_update and result_orderList_update:
                                if result_update:
                                    id = new_id
                                    print("아이디가 변경되었습니다!")
                                    conn.commit()

                                else:
                                    print("아이디 변경에 실패하였습니다. 다시 시도해 주세요.")
                                
                                sleep(3)
                                break;

                        elif num == '2':
                            new_email = input("새로운 이메일을 입력하세요: ")
                            sql_update = "update member set email = '{}' where id = '{}'".format(new_email, id)
                                        
                            cursor.execute(sql_update)
                            print("이메일이 변경되었습니다.")

                            conn.commit()
                            sleep(3)
                            break

                        elif num == '3':
                            new_password = input("새로운 비밀번호를 입력하세요: ")
                            confirm_password = input("비밀번호를 확인해주세요: ")

                            if new_password == confirm_password:
                                sql_update = "update member set pw = '{}' where id = '{}'".format(new_password, id)

                                cursor.execute(sql_update)
                                        
                                print("비밀번호가 변경되었습니다.")
                                conn.commit()
                                sleep(3)
                                break

                        elif num == 4:
                            break

                        else: 
                            break
                    
                # 회원 탈퇴
                elif change_info == '2':
                    confirm = input("회원탈퇴를 하시겠습니까?(y/n): ")

                    if confirm == 'y':
                        sql_delete = "delete from member where id = '{}'".format(id)
                        result = cursor.execute(sql_delete)
                        # print(result[0])

                        if result:
                            #system('clear')
                            print("\n그동안 이용해 주셔서 감사합니다..")
                            
                            conn.commit()
                            sleep(3)
                            return 0

                        else :
                            print("회원탈퇴 실패하였습니다. 다시 진행해 주세요.")
                            sleep(3)
                            return 0

                # 뒤로가기
                elif change_info == '3':
                    continue

                else:
                    pass

                cursor.close()
                
            else:
                # 로그아웃
                break

### main
global conn

# conn = pymysql.connect(
#     host = '127.0.0.1', 
#     user = 'root', 
#     password='', 
#     port = 13306, 
#     db = 'e_commerce', 
#     charset = 'utf8')

conn = pymysql.connect(
    host = '172.17.0.2', 
    user = 'root', 
    password='', 
    port = 3306, 
    db = 'e_commerce', 
    charset = 'utf8')

if __name__ == '__main__':
    Init_Display()
    Main_Page()

    conn.close()