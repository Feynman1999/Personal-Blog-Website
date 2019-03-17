from django.db import models
from django.contrib.auth.models import User


class AC_detail(models.Model):
    student_id = models.IntegerField(default = 0) # 座位号
    problem_id = models.IntegerField(default = 0) # 题号
    aoj_id = models.IntegerField(default = 0) # aoj 上的status id
    # 状态 
    # 0 表示刚加入数据库还未显示
    # 1 表示已显示但还未处理
    # 2 表示正在处理
    # 3 表示处理完毕
    status = models.IntegerField(default = 0)
    name = models.CharField(max_length = 120) # 对应的提交者的姓名
    created_time = models.DateTimeField(auto_now_add=True)    # create_time = models.DateTimeField(default=timezone.now)
    last_updated_time = models.DateTimeField(auto_now=True)
    deal_people = models.ForeignKey(User, on_delete = models.CASCADE, default = 1) # 1是pk

    def __str__(self):  
        return "AC_detail status:{}".format(self.status) 

    def get_problem(self):
        return chr(ord('A') + self.problem_id - 1)

    class Meta:
        ordering = ['-created_time']  # 按照时间倒叙排列