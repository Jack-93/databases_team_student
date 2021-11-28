import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='4545456', db='student_management', charset='utf8mb4')
cursor = conn.cursor()


##################################################################################################################

# 수강신청정보
def input_course(score, apply_no):
    course_sql = "insert into course values('" \
                 + score + "', '" + apply_no + "')"

    cursor.execute(course_sql)
    conn.commit()


##################################################################################################################

# 회원가입 , id : 교원번호(각자 부여받은 고유번호를 아이디로 사용)
def join(id, password, sname, stype):
    print(">> 4. 회원가입")
    
    if(stype=="재학생" or stype=="휴학생"):
        joins_sql = "insert into joins values('" \
                 + id + "', '" + password + "', '" + sname + "', '" + stype + "')"
        student_sql = "insert into student values('" + stype + "','" + sname + "',NULL,NULL)"
        
        cursor.execute(joins_sql)
        cursor.execute(student_sql)
        
    else:
        joins_sql = "insert into joins values('" \
                 + id + "', '" + password + "', '" + sname + "', '" + stype + "')"
        cursor.execute(joins_sql)


    conn.commit()

    print("회원가입 완료")

##################################################################################################################

# 학생정보확인
def student(stype, sname, score, dept):
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

# 학생선택
def select_student(cursor):
    sql = "select * from student"
    cursor.execute(sql)
    print("{0:>20}{1:>20}{2:>20}{3:>20}".format("stype", "sname", "score", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        stype = cur_row[0]
        sname = cur_row[1]
        score = cur_row[2]
        dept = cur_row[3]

        print("%20s %20s %20s %20s" % (stype, sname, score, dept))

##################################################################################################################
# 수강선택
def select_course(cursor):
    sql = "select * from course"
    cursor.execute(sql)
    print("{0:>20}{1:>20}".format("score", "apply_no"))
    rows = cursor.fetchall()
    for cur_row in rows:
        score = cur_row[0]
        apply_no = cur_row[1]

        print("%20s %20s" % (score, apply_no))

##################################################################################################################

# 과목 목록
def select_subject(cursor):
    sql = "select * from subject"
    cursor.execute(sql)

    print("{0:>20}{1:>20}{2:>20}{3:>20}".format("sub_no", "sub_name", "sub_num", "sub_max"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sub_no = cur_row[0]
        sub_name = cur_row[1]
        sub_num = cur_row[2]
        sub_max = cur_row[3]

        print("%20s %20s %20s %20s" % (sub_no, sub_name, sub_num, sub_max))
    
    if(sub_max == sub_num):
        print("수강인원이 가득 찼습니다")

        select_subject(cursor)
        

    
##################################################################################################################

# 로그인
def login(cursor):
    sql = "select * from joins"
    cursor.execute(sql)

    id_insert = input("id를 입력하시오 : ")
    password_insert = input("비밀번호를 입력하시오 : ")

    print("{0:>20}{1:>20}".format("id", "password"))

    rows = cursor.fetchall()
    # print("현재 joins 테이블 정보")
    # for cur_row in rows:
    #     id = cur_row[0]
    #     password = cur_row[1]
        
    #     print("%20s %20s" % (id, password))

    if((id_insert==id) & (password_insert==password)):
        print("로그인 성공 \nid : %20s\npassword : %20s" % (id_insert,password_insert))
    
        if(stype=="교수"):
            print("\n0. 종료"
            "\n1. 교수 페이지"
            )
            while True:
                cmd = input("원하는 항목을 선택하시오( 현재 교수로 로그인 상태 ) : ")
                
                if cmd == '0':
                    break
                elif cmd == '1':
                    print("현재 페이지 없음")
                    break

            conn.rollback()

        elif(stype=="교직원"):
            print("\n0. 종료"
            "\n1. 교직원 페이지"
            )
            while True:
                cmd = input("원하는 항목을 선택하시오( 현재 교직원으로 로그인 상태 ) : ")
                
                if cmd == '0':
                    login(cursor)
                elif cmd == '1':
                    print("현재 페이지 없음")
                    break

            conn.rollback()

        elif(stype=="재학생"):
            print("\n0. 종료"
            "\n1. 재학생 페이지"
            "\n2. 장학수혜내역 페이지"
            "\n2. 성적 확인 페이지"
            )
            while True:
                cmd = input("원하는 항목을 선택하시오( 현재 재학생으로 로그인 상태 ) : ")

                if cmd == '0':
                    break
                elif cmd == '1':
                    print("현재 페이지 없음")
                    break
                elif cmd == '2':
                    print("현재 페이지 없음")
                    break
                elif cmd == '3':
                    print("현재 페이지 없음")
                    break

            conn.rollback()

        elif(stype=="휴학생"):
            print("\n0. 종료"
            "\n1. 휴학생 페이지"
            )

            while True:
                cmd = input("원하는 항목을 선택하시오( 현재 휴학생으로 로그인 상태 ) : ")

                if cmd == '0':
                    break
                elif cmd == '1':
                    print("현재 페이지 없음")
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

##################################################################################################################
# 테이블 생성

# 회원가입시 - 학교 전체인원의 정보 테이블
sql = """create table joins(
    id varchar(45),
    password varchar(45),
    sname varchar(45),
    stype varchar(45) UNIQUE, 
    PRIMARY KEY (id))"""
# 참조당하는 키는 꼭 유니크하거나 프라이머리해야한다 개빡치네 
cursor.execute(sql)

# 재학생 정보
sql = """create table student(
    stype varchar(45), 
    sname varchar(45), 
    score int, 
    dept varchar(45),
    FOREIGN KEY (stype) REFERENCES joins(stype),
    PRIMARY KEY (stype))"""

cursor.execute(sql)

# 수강 정보 테이블
sql = """create table course(
    score int, 
    apply_no int)"""

cursor.execute(sql)

# 과목 목록 테이블(max인원 설정 후 sub_max == sub_num -> 수강 불가)
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
    sch_account int,
    sch_condition varchar(45),
    PRIMARY KEY (sch_name))"""

cursor.execute(sql)

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
        ##회원가입
        print(">> 4. 회원가입")
        id = input("본인의 고유번호를 기입하시오( 아이디로 사용 ): ")
        password = input("비밀번호를 기입하시오: ")
        sname = input("이름을 기입하시오: ")
        stype = input("본인의 TYPE를 기입하시오(교수, 교직원, 재학생, 휴학생): ")
        join(id, password, sname, stype)

    elif cmd == '2':
        ##로그인
        login(cursor)

    elif cmd == '3':
        ##학교인원검색
        select_join(cursor)

    elif cmd == '4':
        ##수강검색
        select_student(cursor)        

    elif cmd == '5':
        ##수강검색
        select_course(cursor)

# 메인페이지에서의 종료는 프로그램종료
conn.close()

##################################################################################################################
