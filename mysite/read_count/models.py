from django.db import models
from django.db.models.fields import exceptions 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

class ReadNum_interface():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            ReadNum_obj = ReadNum.objects.get(content_type = ct, object_id = self.pk)
            return ReadNum_obj.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField() # 对应其它表中该对象的主键值(id)
    
    content_object = GenericForeignKey('content_type', 'object_id') # 类似一种更普适的外键


class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now) # 以天为单位
    read_num = models.IntegerField(default=0) # 当天有多少访问量

    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField() # 对应其它表中该对象的主键值(id)
    
    content_object = GenericForeignKey('content_type', 'object_id') # 类似一种更普适的外键