#-*- coding:utf-8 -*-

# """
# 本文件定义接收用户上传文件的方法和处理方法(与MySql,redis数据库交互)
# 学生上传的源码(压缩包)文件保存在[根目录(和Django项目同级)\upload_data\老师姓名\项目名称\模块名称\学生名称(姓名-账号名)\extends\]路径下
# 学生上传的doc|docx文件保存在[根目录(和Django项目同级)\upload_data\老师姓名\项目名称\模块名称\学生名称\docs]路径下
# 老师上传的文件保存在[根目录(和Django项目同级)\upload_data\老师姓名\students_info\]路径下(老师上传的是学生名单文件(Excel格式))
# @:param  file_object  是request.FILES.get(<input>的name标签)得到的对象,用于获取文件名字和文件数据流
# @:param  project  是文件所属项目的名称,用于创建项目文件夹
# @:param  module  是文件所属的项目的某一个模块的名称,用于创建模块文件夹
# @:param  teacher  是文件所属老师的models模型对象,方便对数据库进行操作,同时用于创建老师的文件夹
# @:param  student  是文件所属学生的(姓名-账号名),用于创建学生文件夹
# @:param  is_doc  (Boolean type)判断是否是doc类型的文件
# """

# TODO 实现get_data_from_antiword(部署时)使用的默认读入方式

import pandas as pd
import os
import subprocess
import redis
from .models import UserRelation, Student, ProjectUser

# TODO 收到一个doc就分词并存储进redis数据库中
def recieve_stu_file(file_object, teacher, project, module, student, is_doc=False):
    file_type = os.path.splitext(file_object.name)[-1]
    file_directory = os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(os.path.abspath('..'), 'upload_data'),teacher),project),module),student)
    if is_doc is True:     # 如果文件是doc|docx文件
        if file_type != '.doc' and file_type != '.docx':
            raise TypeError
        file_directory = os.path.join(file_directory, 'docs')
    else:
        file_directory = os.path.join(file_directory, 'extends')
    os.makedirs(file_directory, exist_ok=True)
    file_path = os.path.join(file_directory, file_object.name)
    with open(file_path, 'wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)

def recieve_tea_file(file_object, teacher, project):
    file_type = os.path.splitext(file_object.name)[-1]
    if file_type != '.xlsx' and file_type != '.xls':
        raise TypeError
    teacher_info = '{}-{}'.format(teacher.name,teacher.account)
    file_directory = os.path.join(os.path.join(os.path.join(os.path.abspath('..'), 'upload_data'), teacher_info), 'students_info')
    os.makedirs(file_directory, exist_ok=True)
    file_path = os.path.join(file_directory, file_object.name)
    with open(file_path, 'wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)
    try:
        update_student_info(file_path=file_path, teacher=teacher, project=project)
    except:
        raise ValueError

# 读取上传的Excel文件,将文件中的信息同步到数据库中(student表,user_relation表,project_user表)[经过测试,可以正常运行]
def update_student_info(file_path, teacher, project):
    student_info = pd.read_excel(file_path)      # student_info type->DataFrame
    student_name, student_account, student_unit = list(student_info['姓名']), list(student_info['学号']), list(student_info['班级'])
    for name, account, unit in zip(student_name, student_account, student_unit):
        try:
            student = Student.objects.get(account=account)    # 报出DonotExist错误才创建用户
        except:
            student = Student()
            student.name = name
            student.account = str(account)
            student.password = student.account[-6:]    # init password is account[-6:]
            student.unit = unit
            student.save()
        try:
            relation = UserRelation.objects.get(student=student, teacher=teacher)
        except:
            relation = UserRelation()
            relation.student = student
            relation.teacher = teacher
            relation.save()
        try:
            project_user = ProjectUser.objects.get(project=project, student=student)
        except:
            project_user = ProjectUser()
            project_user.project = project
            project_user.student = student
            project_user.save()


def get_content_from_antiword(antiword_path, doc_file_path):
    content = subprocess.check_output([antiword_path, doc_file_path])
    #TODO antiword返回的content的格式有待确认