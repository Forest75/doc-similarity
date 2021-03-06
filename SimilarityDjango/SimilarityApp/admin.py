from django.contrib import admin

# Register your models here.
# 自定义管理页面(管理数据库等)

from .models import Student, UserRelation, Project, Module, Teacher, ProjectUser



# 在新建课程项目的界面同时可以添加所属的单元
class ModuleInfo(admin.TabularInline):
    model = Module        # 需要同时添加的数据条目
    extra = 1             # 添加的数量

class ProjectInfo(admin.TabularInline):
    model = Project
    extra = 1

class UserRelationInfo(admin.TabularInline):
    model = UserRelation
    extra = 1

# 使用装饰器将自定义管理类绑定注册
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ModuleInfo]
    # 列表页属性
    list_display = ['name', 'teacher', 'end_date', 'createtime']  # 数据显示的条目
    list_filter = ['name']         # 数据过滤字段
    search_fields = ['name']       # 搜索字段
    list_per_page = 10             # 分页(每几条分页)

    # 添加，修改数据页属性
    fieldsets = [
        ("基本信息", {"fields":['name','teacher']}),
        ("截止日期(选填)", {"fields":['end_date']})
    ]  # 给属性分组,然后按顺序显示
    # 注意:fields和fieldsets不能同时使用

# 使用装饰器将自定义管理类绑定注册
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['name', 'project', 'end_date', 'createtime', 'description']  # 数据显示的条目
    list_filter = ['name']         # 数据过滤字段
    search_fields = ['name']       # 搜索字段
    list_per_page = 10             # 分页(每几条分页)

    # 添加，修改数据页属性
    # fields = ['name','tea_id','end_date','path']    # 规定属性出现的先后顺序
    fieldsets = [
        ("基本信息", {"fields":['name','project','description']}),
        ("截止日期(选填)", {"fields":['end_date']})
    ]  # 给属性分组,然后按顺序显示
    # 注意:fields和fieldsets不能同时使用

# 使用装饰器将自定义管理类绑定注册
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['id', 'name', 'account', 'unit','createtime']  # 数据显示的条目
    list_filter = ['name']         # 数据过滤字段
    search_fields = ['name']       # 搜索字段
    list_per_page = 15             # 分页(每几条分页)

    # 添加，修改数据页属性
    # fields = ['name','account','password',role_,'unit']    # 规定属性出现的先后顺序
    fieldsets = [
        ("基本信息", {"fields":['name', 'unit']}),
        ("账号信息", {"fields":['account', 'password']})
    ]  # 给属性分组,然后按顺序显示
    # 注意:fields和fieldsets不能同时使用

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    inlines = [ProjectInfo, UserRelationInfo]
    # 列表页属性
    list_display = ['name', 'account', 'unit','createtime']  # 数据显示的条目
    list_filter = ['name']         # 数据过滤字段
    search_fields = ['name']       # 搜索字段
    list_per_page = 15             # 分页(每几条分页)

    # 添加，修改数据页属性
    # fields = ['name','account','password',role_,'unit']    # 规定属性出现的先后顺序
    fieldsets = [
        ("基本信息", {"fields":['name', 'unit']}),
        ("账号信息", {"fields":['account', 'password']})
    ]  # 给属性分组,然后按顺序显示
    # 注意:fields和fieldsets不能同时使用

@admin.register(UserRelation)
class UserRelationAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['teacher','student']   # 数据显示的条目
    list_filter = ['teacher']              # 数据过滤字段
    search_fields = ['teacher']            # 搜索字段
    list_per_page = 20                     # 分页(每几条分页)

    # 添加，修改数据页属性
    fieldsets = [
        ("老师", {"fields":['teacher']}),
        ("学生", {"fields":['student']})
    ]  # 给属性分组,然后按顺序显示
    # 注意:fields和fieldsets不能同时使用


@admin.register(ProjectUser)
class ProjectAdmin(admin.ModelAdmin):
    # 列表页属性
    list_display = ['project','student']   # 数据显示的条目
    list_filter = ['project']              # 数据过滤字段
    search_fields = ['project']            # 搜索字段
    list_per_page = 30                     # 分页(每几条分页)

    # 添加，修改数据页属性
    fieldsets = [
        ("项目", {"fields":['project']}),
        ("学生", {"fields":['student']})
    ]  # 给属性分组,然后按顺序显示
    # 注意:fields和fieldsets不能同时使用
