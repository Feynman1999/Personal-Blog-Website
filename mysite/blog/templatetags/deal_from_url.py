from django import template
register = template.Library()

@register.filter

# 要完全解决 需要从后面开始找（只保留最后一个from）
def deal_from_url_fun1(url):  # 找到from 关键字 后的等于 取其后面的内容 直到结束或者 & 
    Id = url.rfind('from')
    if Id>=0:
        url= url[Id+len("from"):]
        Id = url.find('=')
        if Id>=0:
            url = url[Id+len('='):]
            Id = url.find('&')
            if Id>=0: # 后面还有&
                url = url[:Id] # 舍弃&
            else:
                pass
        else:
            pass
    else:
        pass
    return url