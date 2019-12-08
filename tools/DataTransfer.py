from pymysql import *
import re


class DataTransfer(object):
    def __init__(self):
        self.sub_conn = connect(host='localhost', port=3306, database='database_3', user='root', password='mysql',
                                charset='utf8')

        self.main_conn = connect(host="localhost", port=3306, database="FifthDemo", user="root", password="mysql",
                                 charset="utf8")

        self.sub_cursor = self.sub_conn.cursor()

        self.main_cursor = self.main_conn.cursor()

    def transfer_between_databases_question(self):
        sql = "select * from testdata"
        self.sub_cursor.execute(sql)
        content = self.sub_cursor.fetchall()
        # database_3:testdata (id,question_content,path,subject,workbook,grade)
        # FifthDemo:question (id,create_time,update_time,is_delete,content,answer,picture_path,grade,subject,type,workbook_id,workbook_chapter_id)

        for temp in content:
            id = temp[0]
            question_content = temp[1]
            path = temp[2]
            path = re.match(r"./(TestInput/.*.jpg)", path)
            path = "resources/" + path.group(1)
            subject = temp[3]
            workbook_name = temp[4]
            grade = temp[5]
            sql = "select id from workbook where workbook_name=%s"
            self.main_cursor.execute(sql, [workbook_name])
            workbook_id = self.main_cursor.fetchall()[0][0]
            sql = "insert into question (id,create_time,update_time,is_delete,content,picture_path,grade,subject,workbook_id)" \
                  "values(%s,now(),now(),0,%s,%s,%s,%s,%s)"
            params = [id, question_content, path, grade, subject, workbook_id]
            self.main_cursor.execute(sql, params)

        self.main_conn.commit()

    def transfer_between_databases_sub_images(self):
        sql = "select * from sub_images"
        self.sub_cursor.execute(sql)
        content = self.sub_cursor.fetchall()
        for temp in content:
            sub_image_path = temp[2]
            sub_image_path = re.match(r"./GraduationProjectData/(sub_images/.*png)", sub_image_path)
            sub_image_path = "resources/" + sub_image_path.group(1)
            question_id = temp[1]
            sql = "insert into sub_image values(default,now(),now(),0,%s,%s)"
            params = [sub_image_path, question_id]
            self.main_cursor.execute(sql, params)

        self.main_conn.commit()

    def workbook_chapter_ren_sw_4_1(self):
        with open("../resources/source/ren_sw_4_1_BBB_utf8.html") as file:
            filelines = file.readlines()
        filelines_len = len(filelines)
        workbook_id = 1
        grade = "四年级上"
        subject = "数学"
        i = 0
        while i < filelines_len:
            chapter_re = re.match(r".*作业本\+人教版\+2018\+小学数学\+四年级上\+(.*)<br/><br/><br/>", filelines[i])
            if chapter_re:
                chapter_name = chapter_re.group(1)
                print(chapter_name)
                j = i + 1
                while j < filelines_len:
                    chapter_re = re.match(r".*作业本\+人教版\+2018\+小学数学\+四年级上\+(.*)<br/><br/><br/>", filelines[j])
                    if chapter_re:
                        break
                    else:
                        question_id_re = re.match(r"100.{6}", filelines[j])
                        question_content_re = re.match(r"100.*<br/>(.*)<br/>", filelines[j])
                        if question_id_re and question_content_re:
                            question_id = question_id_re.group()
                            question_path = "resources/TestInput/" + question_id + ".jpg"
                            question_content = question_content_re.group(1)
                            sql = "select id from workbook_chapter where workbook_chapter_name=%s"
                            self.main_cursor.execute(sql, [chapter_name])
                            workbook_chapter_id = self.main_cursor.fetchall()[0][0]
                            params = [question_id, question_content, question_path, grade, subject, workbook_id,
                                      workbook_chapter_id]
                            sql = "insert into question (id,create_time,update_time,is_delete,content,picture_path,grade,subject,workbook_id,workbook_chapter_id)" \
                                  "values(%s,now(),now(),0,%s,%s,%s,%s,%s,%s)"
                            self.main_cursor.execute(sql, params)
                        j += 1
                i = j
            else:
                i += 1
        self.main_conn.commit()

    def workbook_chapter_ren_sw_5_1(self):
        with open("../resources/source/ren_sw_5_1_BBB_utf8.html") as file:
            filelines = file.readlines()
        filelines_len = len(filelines)
        workbook_id = 2
        grade = "五年级上"
        subject = "数学"
        i = 0
        # for fileline in filelines:
        #     chapter_re = re.match(r".*小学数学作业本\+五年级上册\+(.*)<br/><br/><br/>", fileline)
        #     if chapter_re:
        #         chapter_name = chapter_re.group(1)
        #         sql = "insert into workbook_chapter values (default, now(), now(), 0, %s, %s)"
        #         self.main_cursor.execute(sql, [chapter_name, workbook_id])
        # self.main_conn.commit()

        while i < filelines_len:
            chapter_re = re.match(r".*小学数学作业本\+五年级上册\+(.*)<br/><br/><br/>", filelines[i])
            if chapter_re:
                chapter_name = chapter_re.group(1)
                print(chapter_name)
                j = i + 1
                while j < filelines_len:
                    chapter_re = re.match(r".*小学数学作业本\+五年级上册\+(.*)<br/><br/><br/>", filelines[j])
                    if chapter_re:
                        break
                    else:
                        question_id_re = re.match(r"100.{6}", filelines[j])
                        question_content_re = re.match(r"100.*<br/>(.*)<br/>", filelines[j])
                        if question_id_re and question_content_re:
                            question_id = question_id_re.group()
                            question_path = "resources/TestInput/" + question_id + ".jpg"
                            question_content = question_content_re.group(1)
                            sql = "select id from workbook_chapter where workbook_chapter_name=%s"
                            self.main_cursor.execute(sql, [chapter_name])
                            workbook_chapter_id = self.main_cursor.fetchall()[0][0]
                            params = [question_id, question_content, question_path, grade, subject, workbook_id,
                                      workbook_chapter_id]
                            sql = "insert into question (id,create_time,update_time,is_delete,content,picture_path,grade,subject,workbook_id,workbook_chapter_id)" \
                                  "values(%s,now(),now(),0,%s,%s,%s,%s,%s,%s)"
                            self.main_cursor.execute(sql, params)
                            print(params)
                        j += 1
                i = j
            else:
                i += 1
        self.main_conn.commit()

    def workbook_chapter_lianxiyuceshi(self):
        with open("../resources/source/练习与测试_五上_BBB_utf8.html") as file:
            filelines = file.readlines()
        filelines_len = len(filelines)
        workbook_id = 3
        grade = "五年级上"
        subject = "数学"
        i = 0
        # for fileline in filelines:
        #     chapter_re = re.match(r".*<br/><br/><br/>(.*)<br/><br/><br/>", fileline)
        #     if chapter_re:
        #         chapter_name = chapter_re.group(1)
        #         print(chapter_name)
        #         sql = "insert into workbook_chapter values (default, now(), now(), 0, %s, %s)"
        #         self.main_cursor.execute(sql, [chapter_name, workbook_id])
        # self.main_conn.commit()

        while i < filelines_len:
            chapter_re = re.match(r".*<br/><br/><br/>(.*)<br/><br/><br/>", filelines[i])
            if chapter_re:
                chapter_name = chapter_re.group(1)
                print(chapter_name)
                j = i + 1
                while j < filelines_len:
                    chapter_re = re.match(r".*<br/><br/><br/>(.*)<br/><br/><br/>", filelines[j])
                    if chapter_re:
                        break
                    else:
                        question_id_re = re.match(r"100.{6}", filelines[j])
                        question_content_re = re.match(r"100.*<br/>(.*)<br/>", filelines[j])
                        if question_id_re and question_content_re:
                            question_id = question_id_re.group()
                            question_path = "resources/TestInput/" + question_id + ".jpg"
                            question_content = question_content_re.group(1)
                            sql = "select id from workbook_chapter where workbook_chapter_name=%s"
                            self.main_cursor.execute(sql, [chapter_name])
                            workbook_chapter_id = self.main_cursor.fetchall()[0][0]
                            params = [question_id, question_content, question_path, grade, subject, workbook_id,
                                      workbook_chapter_id]
                            sql = "insert into question (id,create_time,update_time,is_delete,content,picture_path,grade,subject,workbook_id,workbook_chapter_id)" \
                                  "values(%s,now(),now(),0,%s,%s,%s,%s,%s,%s)"
                            self.main_cursor.execute(sql, params)
                            print(params)
                        j += 1
                i = j
            else:
                i += 1
        self.main_conn.commit()

    def workbook_chapter_yingyu_wunianji(self):
        with open("../resources/source/英语五年级上_BBB_utf8.html") as file:
            filelines = file.readlines()
        filelines_len = len(filelines)
        workbook_id = 4
        grade = "五年级上"
        subject = "英语"
        i = 0
        # for fileline in filelines:
        #     chapter_re = re.match(r".*小学英语作业本\+人教版\+2018\+五年级上册\+(.*)<br/><br/><br/>", fileline)
        #     if chapter_re:
        #         chapter_name = chapter_re.group(1)
        #         print(chapter_name)
        #         sql = "insert into workbook_chapter values (default, now(), now(), 0, %s, %s)"
        #         self.main_cursor.execute(sql, [chapter_name, workbook_id])
        # self.main_conn.commit()

        while i < filelines_len:
            chapter_re = re.match(r".*小学英语作业本\+人教版\+2018\+五年级上册\+(.*)<br/><br/><br/>", filelines[i])
            if chapter_re:
                chapter_name = chapter_re.group(1)
                print(chapter_name)
                j = i + 1
                while j < filelines_len:
                    chapter_re = re.match(r".*小学英语作业本\+人教版\+2018\+五年级上册\+(.*)<br/><br/><br/>", filelines[j])
                    if chapter_re:
                        break
                    else:
                        question_id_re = re.match(r"100.{6}", filelines[j])
                        question_content_re = re.match(r"100.*<br/>(.*)<br/>", filelines[j])
                        if question_id_re and question_content_re:
                            question_id = question_id_re.group()
                            question_path = "resources/TestInput/" + question_id + ".jpg"
                            question_content = question_content_re.group(1)
                            sql = "select id from workbook_chapter where workbook_chapter_name=%s"
                            self.main_cursor.execute(sql, [chapter_name])
                            workbook_chapter_id = self.main_cursor.fetchall()[0][0]
                            params = [question_id, question_content, question_path, grade, subject, workbook_id,
                                      workbook_chapter_id]
                            sql = "insert into question (id,create_time,update_time,is_delete,content,picture_path,grade,subject,workbook_id,workbook_chapter_id)" \
                                  "values(%s,now(),now(),0,%s,%s,%s,%s,%s,%s)"
                            self.main_cursor.execute(sql, params)
                            print(params)
                        j += 1
                i = j
            else:
                i += 1
        self.main_conn.commit()

    def workbook_chapter_yingyu_sinianji(self):
        with open("../resources/source/英语四年级上_BBB_utf8.html") as file:
            filelines = file.readlines()
        filelines_len = len(filelines)
        workbook_id = 5
        grade = "四年级上"
        subject = "英语"
        i = 0
        # for fileline in filelines:
        #     chapter_re = re.match(r".*小学英语作业本\+人教版\+2018\+四年级上册\+(.*)<br/><br/><br/>", fileline)
        #     if chapter_re:
        #         chapter_name = chapter_re.group(1)
        #         print(chapter_name)
        #         sql = "insert into workbook_chapter values (default, now(), now(), 0, %s, %s)"
        #         self.main_cursor.execute(sql, [chapter_name, workbook_id])
        # self.main_conn.commit()

        while i < filelines_len:
            chapter_re = re.match(r".*小学英语作业本\+人教版\+2018\+四年级上册\+(.*)<br/><br/><br/>", filelines[i])
            if chapter_re:
                chapter_name = chapter_re.group(1)
                print(chapter_name)
                j = i + 1
                while j < filelines_len:
                    chapter_re = re.match(r".*小学英语作业本\+人教版\+2018\+四年级上册\+(.*)<br/><br/><br/>", filelines[j])
                    if chapter_re:
                        break
                    else:
                        question_id_re = re.match(r"100.{6}", filelines[j])
                        question_content_re = re.match(r"100.*<br/>(.*)<br/>", filelines[j])
                        if question_id_re and question_content_re:
                            question_id = question_id_re.group()
                            question_path = "resources/TestInput/" + question_id + ".jpg"
                            question_content = question_content_re.group(1)
                            sql = "select id from workbook_chapter where workbook_chapter_name=%s"
                            self.main_cursor.execute(sql, [chapter_name])
                            workbook_chapter_id = self.main_cursor.fetchall()[0][0]
                            params = [question_id, question_content, question_path, grade, subject, workbook_id,
                                      workbook_chapter_id]
                            sql = "insert into question (id,create_time,update_time,is_delete,content,picture_path,grade,subject,workbook_id,workbook_chapter_id)" \
                                  "values(%s,now(),now(),0,%s,%s,%s,%s,%s,%s)"
                            self.main_cursor.execute(sql, params)
                            print(params)
                        j += 1
                i = j
            else:
                i += 1
        self.main_conn.commit()


def main():
    data_transfer = DataTransfer()
    # data_transfer.transfer_between_databases_question() 已执行
    # data_transfer.transfer_between_databases_sub_images() 已执行
    data_transfer.workbook_chapter_yingyu_sinianji()


if __name__ == '__main__':
    main()
