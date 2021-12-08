# mysql 켜고 student_management 미리 만들어놓고 코드 실행

import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='4545456a', db='student_management', charset='utf8mb4')
cursor = conn.cursor()


##################################################################################################################

# 회원가입 , id : 교원번호(각자 부여받은 고유번호를 아이디로 사용)
def join(id, password, sname, stype):
    print(">> 4. 회원가입")

    if(stype == "재학생" or stype == "휴학생"):
        joins_sql = "insert into joins values('" \
            + id + "', '" + password + "', '" + sname + "', '" + stype + "')"
        student_sql = "insert into student values('" + \
            stype + "','" + sname + "',NULL,NULL)"

        cursor.execute(joins_sql)
        cursor.execute(student_sql)

    else:
        joins_sql = "insert into joins values('" \
            + id + "', '" + password + "', '" + sname + "', '" + stype + "')"
        cursor.execute(joins_sql)

    conn.commit()

    print("회원가입 완료")

##################################################################################################################

# 학생 등록


def input_student(stype, sname, score, dept):
    print(">> 학생정보 확인")
    student_sql = "insert into student values('" \
        + stype + \
        " " + sname + \
        " " + score + \
        " " + dept + "')"

    cursor.execute(student_sql)
    conn.commit()


##################################################################################################################

# 학교 전체인원 정보
def select_join(cursor):
    sql = "select * from joins"
    cursor.execute(sql)
    print("{0:>20}{1:>20}{2:>20}".format("id", "sname", "stype"))
    rows = cursor.fetchall()
    for cur_row in rows:
        id = cur_row[0]
        sname = cur_row[2]
        stype = cur_row[3]

        print("%20s %20s %20s" % (id, sname, stype))

##################################################################################################################

# 재학생 보기


def view_student(cursor):
    sql = "select * from student"
    cursor.execute(sql)
    print("{0:>20}{1:>20}{2:>20}{3:>20}".format(
        "stype", "sname", "score", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        stype = cur_row[0]
        sname = cur_row[1]
        score = cur_row[2]
        dept = cur_row[3]

        print("%20s %20s %20s %20s" % (stype, sname, score, dept))

##################################################################################################################

# 수강신청


def input_course(cursor, id_insert, sub_no):

    score = '0'
    sub_sql = "SELECT sub_num, sub_max FROM subject where sub_no=%s AND sub_num = sub_max" % sub_no
    result = cursor.execute(sub_sql)
    conn.commit()

    if result == True:
        print("\n정원 초과입니다.")
        return

    sub_num_sql = "update subject set sub_num = sub_num + 1 where sub_no=%s" % sub_no
    cursor.execute(sub_num_sql)
    conn.commit()

    student_sql = "insert into course values('" \
        + id_insert + "', '" + sub_no + "', '" + score + "')"
    cursor.execute(student_sql)
    conn.commit()

    print("\n수강 신청되었습니다.")

##################################################################################################################

# 강의 목록


def view_subject(cursor):
    sql = "select * from subject"
    cursor.execute(sql)

    print("{0:>20}{1:>20}{2:>20}{3:>20}".format(
        "sub_no", "sub_name", "sub_num", "sub_max"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sub_no = cur_row[0]
        sub_name = cur_row[1]
        sub_num = cur_row[2]
        sub_max = cur_row[3]

        print("%20s %20s %20s %20s" % (sub_no, sub_name, sub_num, sub_max))


##################################################################################################################

# 수강신청내역
def view_course(cursor, id_insert):
    sql = "SELECT sub_no, sub_name FROM subject where sub_no=(SELECT sub_no_FK FROM course where id_FK=%s)" % id_insert
    cursor.execute(sql)
    print("{0:>20}{1:>20}".format("sub_no", "sub_name"))
    rows = cursor.fetchall()
    index = 0
    for cur_row in rows:
        sub_no = cur_row[0]
        sub_name = cur_row[1]
        print("%20s %20s" % (sub_no, sub_name))
    sub_no = input(print("\n취소하고 싶은 강의의 번호를 입력해주세요(없으면 0)"))
    if sub_no == '0':
        return
    else:
        sub_num_sql = "update subject set sub_num = sub_num - 1 where sub_no=%s" % sub_no
        cursor.execute(sub_num_sql)
        conn.commit()
        view_subject(cursor)

##################################################################################################################

# 성적 관리


def input_score(cursor, id, sub_no, score):
    sch_sql = "update course set score = '{}' where id_FK = '{}' AND sub_no_FK = '{}'".format(
        score, id, sub_no)
    cursor.execute(sch_sql)
    conn.commit()

    print("\n점수 변경이 완료되었습니다.")


##################################################################################################################

# 장학금신청
def input_scholar(cursor, id_insert, sch_name):

    scholar_sql = "insert into scholar_management values('" \
        + id_insert + "', '" + sch_name + "', '" + '신청' + "')"
    cursor.execute(scholar_sql)
    conn.commit()

    print("\n장학금이 신청되었습니다")

##################################################################################################################

# 장학금 목록


def view_scholar(cursor):
    sch_sql = "select * from scholar"
    cursor.execute(sch_sql)

    print("%-20s %-20s %-20s" %
          ("sch_name", "sch_cumulative_amount", "sch_condition"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sch_name = cur_row[0]
        sch_cumulative_amount = cur_row[1]
        sch_condition = cur_row[2]

        print("%-20s %-20s %-20s" %
              (sch_name, sch_cumulative_amount, sch_condition))

##################################################################################################################

# 장학금 관리


def input_scholar_management(cursor, id, sch_name, sch_amount):
    sch_sql = "insert into scholarship_history values('" \
        + id + "', '" + sch_name + "', '" + sch_amount + "')"
    cursor.execute(sch_sql)
    conn.commit()

    sch_apply = '허가'
    sch_sql = "update scholar_management set sch_apply = '{}' where id_FK = '{}' AND sch_name_FK = '{}'".format(
        sch_apply, id, sch_name)
    cursor.execute(sch_sql)
    conn.commit()

    print("\n장학금 신청이 허용되었습니다.")


##################################################################################################################

# 장학금 관리 목록
def view_scholar_management(cursor):
    sch_sql = "select * from scholar_management"
    cursor.execute(sch_sql)

    print("%-20s %-20s %-20s" % ("id_FK", "sch_name_FK", "sch_apply"))
    rows = cursor.fetchall()
    for cur_row in rows:
        id_FK = cur_row[0]
        sch_name_FK = cur_row[1]
        sch_apply = cur_row[2]

        print("%-20s %-20s %-20s" % (id_FK, sch_name_FK, sch_apply))

##################################################################################################################

# 성적 불러오는 함수 (cursor 와 ID를 입력받고 과목번호와 점수를 출력)


def get_grade_list(cursor, id_insert):

    get_grade_sql = "select sub_no_FK, score from course where ID_FK=%s" % id_insert
    cursor.execute(get_grade_sql)

    print("%-20s %-20s" % ("과목번호", "점수"))
    rows = cursor.fetchall()

    for cur_row in rows:
        sub_no_FK = cur_row[0]
        score = cur_row[1]

        print("%-20s %-20s" % (sub_no_FK, score))


##################################################################################################################

# 이중튜플을 푸는 함수
def fetchall_to_list(fetchall):
    temp_list = list()

    for i in range(len(fetchall)):
        temp_list.append(fetchall[i][0])
    result_list = list(temp_list)
    return result_list

##################################################################################################################

# 장학금 기록 불러오는 함수 (cursor와 ID 를 입력받고 ID와 장학금 이름 수렴내역을 출력)


def get_scholarship_list(cursor, id_insert):

    get_scholarship_list_sql = "SELECT id_FK, sch_name_FK, sch_amount FROM scholarship_history WHERE ID_FK=%s" % id_insert
    cursor.execute(get_scholarship_list_sql)

    print("%20s %20s %20s" % ("id_FK", "sch_name_FK", "sch_amount"))
    rows = cursor.fetchall()

    for cur_row in rows:
        id_FK = cur_row[0]
        sch_name_FK = cur_row[1]
        sch_amount = cur_row[2]

        print("%20s %20s %20s" % (id_FK, sch_name_FK, sch_amount))


##################################################################################################################

# 관리자 페이지
def mypage_manager(cursor, id_insert):

    print("\n0. 종료"
          "\n1. 학생관리"
          "\n2. 학생등록"
          )

    while True:
        cmd = input("원하는 항목을 선택하시오( 관리자 페이지 ) : ")

        if cmd == '0':
            break
        elif cmd == '1':
            id = input(print("관리하려는 학생의 학번을 입력해주세요."))
            print("\n학생관리페이지")
            student_management(cursor, id)
            break
        elif cmd == '2':
            print("\n학생등록")

            break

        conn.rollback()


##################################################################################################################

# 학생관리 페이지
def student_management(cursor, id):

    print("\n0. 종료"
          "\n1. 장학금 신청 내역 "
          "\n2. 학생 성적 관리"
          )

    while True:
        cmd = input("원하는 항목을 선택하시오( 학생관리 페이지 ) : ")

        if cmd == '0':
            break
        elif cmd == '1':
            view_scholar_management(cursor)
            sch_name = input(print("\n장학금을 허가하려면 장학금의 이름을 입력해주세요"))
            sch_amount = input(print("\n장학금 지급액을 정해주세요"))
            input_scholar_management(cursor, id, sch_name, sch_amount)
            break
        elif cmd == '2':
            print(get_grade_list(cursor, id))
            sub_no = input(print("\n점수변경을 원하는 과목번호를 입력해주세요"))
            score = input(print("\n변경한 점수를 입력해주세요"))
            input_score(cursor, id, sub_no, score)
            break

        conn.rollback()


##################################################################################################################

# 재학생 페이지
def mypage_Student(cursor, id_insert):

    print("\n0. 종료"
          "\n1. 수강신청내역"
          "\n2. 성적열람페이지"
          "\n3. 장학금 수해 내역"
          )

    while True:
        cmd = input("원하는 항목을 선택하시오( 재학생_현재페이지 ) : ")

        if cmd == '0':
            break
        elif cmd == '1':
            print("수강신청내역")
            view_course(cursor, id_insert)
            break
        elif cmd == '2':
            get_grade_list(cursor, id_insert)
            break
        elif cmd == '3':
            get_scholarship_list(cursor, id_insert)
            break

        conn.rollback()


##################################################################################################################

# 휴학생 페이지
def mypage_absenceStudent(cursor, id_insert):

    print("\n0. 종료"
          "\n1. 성적열람페이지"
          "\n2. 장학금 수혜 내역"
          )

    while True:
        cmd = input("원하는 항목을 선택하시오( 휴학생_마이페이지 ) : ")

        if cmd == '0':
            break
        elif cmd == '1':
            get_grade_list(cursor, id_insert)
            break
        elif cmd == '2':
            get_scholarship_list(cursor, id_insert)
            break

        conn.rollback()

##################################################################################################################

# 로그인


def login(cursor):
    sql = "select * from joins"
    cursor.execute(sql)

    id_insert = str(input("id를 입력하시오 : "))
    password_insert = str(input("비밀번호를 입력하시오 : "))

    print("{0:>20}{1:>20}".format("id", "password"))

    rows = cursor.fetchall()
    # print("현재 joins 테이블 정보")
    # for cur_row in rows:
    #     id = cur_row[0]
    #     password = cur_row[1]
    #     print("%20s %20s" % (id, password))
    get_id_list_sql = "select id from joins"
    cursor.execute(get_id_list_sql)
    id_list = cursor.fetchall()
    id_list = list(fetchall_to_list(id_list))

    print(id_list)
    # print((\'id_insert'\))
    if(id_insert in id_list):
        get_pw_sql = "select password from joins where ID=%s" % id_insert
        cursor.execute(get_pw_sql)
        password = cursor.fetchall()
        password = list(fetchall_to_list(password))
        print(password)
        if(password_insert == password[0]):
            print("로그인 성공 \nid : %20s\npassword : %20s" %
                  (id_insert, password_insert))
            search_stype_sql = "select stype from joins where ID=%s" % id_insert
            cursor.execute(search_stype_sql)
            stype = cursor.fetchall()
            stype = list(fetchall_to_list(stype))
            if(stype[0] == "교수"):
                print("\n0. 종료"
                      "\n1. 교수 페이지"
                      )
                while True:
                    cmd = input("원하는 항목을 선택하시오( 현재 교수로 로그인 상태 ) : ")

                    if cmd == '0':
                        break
                    elif cmd == '1':
                        mypage_manager(cursor, id_insert)
                        break

                conn.rollback()

            elif(stype[0] == "교직원"):
                print("\n0. 종료"
                      "\n1. 교직원 페이지"
                      )
                while True:
                    cmd = input("원하는 항목을 선택하시오( 현재 교직원으로 로그인 상태 ) : ")

                    if cmd == '0':
                        login(cursor)
                    elif cmd == '1':
                        mypage_manager(cursor, id_insert)
                        break

                conn.rollback()

            elif(stype[0] == "재학생"):
                print("\n0. 종료"
                      "\n1. 마이 페이지"
                      "\n2. 수강신청"
                      "\n3. 장학금신청"
                      )
                while True:
                    cmd = input("원하는 항목의 번호를 입력해주세요( 현재 재학생으로 로그인 상태 ) : ")

                    if cmd == '0':
                        break
                    elif cmd == '1':
                        print("마이 페이지")
                        mypage_Student(cursor, id_insert)
                        break
                    elif cmd == '2':
                        while True:
                            print("수강신청")
                            view_subject(cursor)
                            sub_no = input(
                                "신청하는 강의의 번호를 입력해주세요(종료를 원하시면 0) : ")
                            if sub_no == '0':
                                break
                            input_course(cursor, id_insert, sub_no)
                        break
                    elif cmd == '3':
                        while True:
                            print("장학금 신청")
                            view_scholar(cursor)
                            sch_name = input(
                                "신청하는 장학금의 이름을 입력해주세요(종료를 원하시면 0) : ")
                            if sch_name == '0':
                                break
                            input_scholar(cursor, id_insert, sch_name)
                        break

                conn.rollback()

            elif(stype[0] == "휴학생"):
                print("\n0. 종료"
                      "\n1. 마이 페이지"
                      )

                while True:
                    cmd = input("원하는 항목을 선택하시오( 현재 휴학생으로 로그인 상태 ) : ")

                    if cmd == '0':
                        break
                    elif cmd == '1':
                        print("마이 페이지")
                        mypage_absenceStudent(cursor, id_insert)
                        break

                conn.rollback()

            # while True:
            #     cmd = input("원하는 항목을 선택하시오( 현재 로그인 페이지 ) : ")

            #     # elif cmd =='1':

            #     # elif cmd =='2':

            #     # elif cmd =='3':

        else:
            print("로그인 실패 - 다시 입력해주세요")
            login(cursor)
    else:
        print("존재하지 않는 아이디입니다.")


##################################################################################################################

# 기존 테이블 삭제
cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS joins cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS student cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS course cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS subject cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS scholar cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS scholar_management cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS scholarship_history cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

##################################################################################################################
# 테이블 생성

# 회원가입시 - 학교 전체인원의 정보 테이블
sql = """create table joins(
    id varchar(45),
    password varchar(45),
    sname varchar(45),
    stype varchar(45), 
    PRIMARY KEY (id))"""
# 참조당하는 키는 꼭 유니크하거나 프라이머리해야한다 개빡치네
cursor.execute(sql)

# 재학생 정보
sql = """create table student(
    joinid varchar(45),
    stype_FK varchar(45),
    sname_FK varchar(45),
    grade int,
    dept varchar(45),
    FOREIGN KEY (joinid) REFERENCES joins(id))"""

cursor.execute(sql)


# 과목 테이블(max인원 설정 후 sub_max == sub_num -> 수강 불가)
sql = """create table subject(
    sub_no int, 
    sub_name varchar(45), 
    sub_num int, 
    sub_max int, 
    PRIMARY KEY (sub_no))"""

cursor.execute(sql)

# 장학금 테이블
sql = """create table scholar(
    sch_name varchar(45),
    sch_cumulative_amount int,
    sch_condition varchar(45),
    PRIMARY KEY (sch_name))"""

cursor.execute(sql)

# 장학금 관리 테이블
sql = """create table scholar_management(
    id_FK varchar(45),
    sch_name_FK varchar(45),
    FOREIGN KEY (id_FK) REFERENCES joins(id),
    FOREIGN KEY (sch_name_FK) REFERENCES scholar(sch_name),
    sch_apply varchar(45))"""

cursor.execute(sql)

# 장학 수령 내역
sql = """create table scholarship_history(
    id_FK varchar(45),
    sch_name_FK varchar(45),
    sch_amount int,
    FOREIGN KEY (id_FK) REFERENCES joins(id),
    FOREIGN KEY (sch_name_FK) REFERENCES scholar(sch_name))"""

cursor.execute(sql)

# 수강 테이블
sql = """create table course(
    id_FK varchar(45),
    sub_no_FK int,
    FOREIGN KEY (id_FK) REFERENCES joins(id),
    FOREIGN KEY (sub_no_FK) REFERENCES subject(sub_no),
    score int)"""

cursor.execute(sql)

# 임시 데이터
sql = "INSERT INTO joins(ID,password,sname,stype) VALUES(2000000000,1234,'홍길동1','교수')"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO joins(ID,password,sname,stype) VALUES(2000000001,1234,'홍길동2','교직원')"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO joins(ID,password,sname,stype) VALUES(2000000002,1234,'홍길동3','재학생')"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO joins(ID,password,sname,stype) VALUES(2000000003,1234,'홍길동4','휴학생')"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO subject(sub_no,sub_name,sub_num,sub_max) VALUES(01,'국어',0,50)"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO subject(sub_no,sub_name,sub_num,sub_max) VALUES(02,'영어',0,50)"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO subject(sub_no,sub_name,sub_num,sub_max) VALUES(03,'수학',0,50)"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO course(id_FK, sub_no_FK, score) VALUES('2000000002',1,0)"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO course(id_FK, sub_no_FK, score) VALUES('2000000003',1,0)"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO scholar(sch_name, sch_cumulative_amount, sch_condition) VALUES('고려장학금',1000000000,'성적이 우수하고 인품이 훌룡한 학생')"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO scholar_management(id_FK, sch_name_FK, sch_apply) VALUES('2000000002','고려장학금','신청')"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO scholarship_history(id_FK, sch_name_FK, sch_amount) VALUES('2000000002','고려장학금',1000000)"
cursor.execute(sql)
conn.commit()

sql = "INSERT INTO scholarship_history(id_FK, sch_name_FK, sch_amount) VALUES('2000000003','고려장학금',1000000)"
cursor.execute(sql)
conn.commit()

##################################################################################################################


# 첫페이지 화면 출력 함수

print("0. 종료"
      "\n1. 회원가입"
      "\n2. 로그인"
      "\n3. 학교 인원 검색"
      "\n4. 학생 검색"
      "\n5. 강의 레코드 검색"
      )

while True:
    cmd = input("원하는 항목을 선택하시오 ( 현재 메인 페이지 ) : ")
    if cmd == '0':
        break

    elif cmd == '1':
        # 회원가입
        print(">> 4. 회원가입")
        id = input("본인의 고유번호를 기입하시오( 아이디로 사용 ): ")
        password = input("비밀번호를 기입하시오: ")
        sname = input("이름을 기입하시오: ")
        stype = input("본인의 TYPE를 기입하시오(교수, 교직원, 재학생, 휴학생): ")
        join(id, password, sname, stype)

    elif cmd == '2':
        # 로그인
        login(cursor)

    elif cmd == '3':
        # 학교인원검색
        select_join(cursor)

    elif cmd == '4':
        # 학생보기
        view_student(cursor)

    elif cmd == '5':
        # 수강검색
        view_subject(cursor)

# 메인페이지에서의 종료는 프로그램종료
conn.close()

##################################################################################################################
