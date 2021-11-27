import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='4545456', db='student_management', charset='utf8mb4')

cursor=conn.cursor()

def menu():
    print('')
    print('')
    print('')

    choice = input('')

    return int(choice)

