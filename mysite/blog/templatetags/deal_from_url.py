from django import template
register = template.Library()

@register.filter
def deal_from_url_fun1(url):  # 找到from 关键字 后的等于 取其后面的内容 直到结束或者 & 
    Id = url.find('from')
    if Id>=0:
        url= url[Id+len("from"):]
        Id = url.find('=')
        if Id>=0:
            url = url[Id+len('='):]
            Id = url.find('&')
            if Id>=0: # 后面还有&
                url = url[:Id]
            else:
                pass
        else:
            pass
    else:
        pass
    return url