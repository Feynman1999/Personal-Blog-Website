from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from .models import Comment

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(min_length=5, widget=forms.Textarea(attrs={'class':'form-control', 'id':'forclear',
                             'placeholder':"至少写入5个字符哦   支持markdown(刷新可渲染tex)~   \n\n点击下面回复可以对评论进行回复 \n\n刷新本页面时默认对文章进行评论",
                                 "rows":"6"}), 
                             error_messages={'required': '评论内容不能为空哦'})

    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)


    def clean(self):  # 前端页面不可信原则
        # 判断用户是否登录
        if not self.user.is_authenticated:
            raise forms.ValidationError('用户尚未登录！')
        
        # 评论对象存在验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在！')

        return self.cleaned_data
    
    
    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError("回复出错：id<0")
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = Comment.objects.filter(pk=reply_comment_id)[0] # 加0很关键
        else:
            raise forms.ValidationError("回复出错：回复对象不存在")
        return reply_comment_id