import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='4545456', db='student_management', charset='utf8mb4')
cursor = conn.cursor()

# # 회원가입
# def join(id, password, sname, sno):
#     stud_sql = "insert into student values('" \
#                + id + "', '" + password + "', " + sname + ", '" + sno + "')"
               
#     try:
#         cursor.execute(stud_sql)
#         conn.commit()
#     except:
#         conn.rollback()

# 학생정보입력
def input_student(sno, sname, grade, dept):
    stud_sql = "insert into student values('" \
               + sno + \
               " " + sname + \
               " " + grade + \
               " " + dept + "')"
    try:
        cursor.execute(stud_sql)
        conn.commit()
    except:
        conn.rollback()


# 수강정보입력
def input_course(cno, cname, credit, profname, dept):
    course_sql = "insert into course values('' \
                 + cno + '', '' + cname + '', '' + credit + "', '" + profname + "', '" + dept + '')"
    try:
        cursor.execute(course_sql)
        conn.commit()
    except:
        conn.rollback()


# 등록하기
def join(id, password, sname, sno):
    joins_sql = "insert into joins values('" \
                 + id + "', '" + password + "', '" + sname + "', '" + sno + "')"
    student_sql = "insert into student values('" + sno + "',NULL,NULL,NULL)"
    # course_sql = "insert into course values('" + cno + "',NULL,NULL,NULL,NULL)"
    cursor.execute(student_sql)
    # cursor.execute(course_sql)
    cursor.execute(joins_sql)
    conn.commit()


# 학생선택
def select_student(cursor):
    sql = "select * from student"
    cursor.execute(sql)
    print("{0:>20}{1:>20}{2:>20}{3:>20}".format("sno", "sname", "grade", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        sno = cur_row[0]
        sname = cur_row[1]
        grade = cur_row[2]
        dept = cur_row[3]
        print("%20s %20s %20s %20s" % (sno, sname, grade, dept))


# 수강선택
def select_course(cursor):
    sql = "select * from course"
    cursor.execute(sql)
    print("{0:>20}{1:>20}{2:>20}{3:>20}{4:>20}".format("cno", "cname", "credit", "profname", "dept"))
    rows = cursor.fetchall()
    for cur_row in rows:
        cno = cur_row[0]
        cname = cur_row[1]
        credit = cur_row[2]
        profname = cur_row[3]
        dept = cur_row[4]
        print("%20s %20s %20s %20s %20s" % (cno, cname, credit, profname, dept))


# 로그인
def login(cursor):
    sql = "select * from joins"
    cursor.execute(sql)

    id_insert = input("id를 입력하시오 : ")
    password_insert = input("비밀번호를 입력하시오 : ")

    print("{0:>20}{1:>20}".format("id", "password"))

    rows = cursor.fetchall()
    for cur_row in rows:
        id = cur_row[0]
        password = cur_row[1]
        print("%20s %20s" % (id, password))

    if((id_insert==id) & (password_insert==password)):
        print("로그인 성공 \nid : %20s\npassword : %20s" % (id_insert,password_insert))
    else:
        print("로그인 실패")



# 기존 테이블 삭제
cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS student cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS course cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

cursor.execute("set foreign_key_checks = 0")
sql = "drop table IF EXISTS joins cascade"
cursor.execute(sql)
cursor.execute("set foreign_key_checks = 1")

# 테이블 생성
sql = "create table student(sno int, sname varchar(45), grade int, dept varchar(45), primary key (sno))"
cursor.execute(sql)
sql = "create table course(cno varchar(45), cname varchar(45), credit int, profname varchar(45), dept varchar(45), primary key (cno))"
cursor.execute(sql)
sql = "create table joins(id varchar(45), password varchar(45), sname varchar(45), sno int, FOREIGN KEY (sno) REFERENCES student (sno), PRIMARY KEY (id))"
cursor.execute(sql)


##출력
print("0. 종료"
    "\n1. student 레코드 검색"
    "\n2. course 레코드 검색"
    "\n3. 로그인"
    "\n4. 회원가입"
    )

while True:
    cmd = input("원하는 항목을 선택하시오 : ")
    if cmd == '0':
        break
    elif cmd == '1':
        ##학생검색
        select_student(cursor)
    elif cmd == '2':
        ##수강검색
        select_course(cursor)
    elif cmd == '3':
        ##로그인
        login(cursor)
    elif cmd == '4':
        ##회원가입
        print(">> 4. 회원가입")
        id = input("아이디를 기입하시오: ")
        password = input("비밀번호를 기입하시오: ")
        sname = input("이름을 기입하시오: ")
        sno = input("관리자 또는 학번을 기입하시오: ")
        join(id, password, sname, sno)
        

conn.close()
