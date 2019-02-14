from django import template
import markdown
register = template.Library()

@register.filter
def md2html_1(content):  # 自定义过滤器 渲染成html即可 
    return markdown.markdown(content.replace("\r\n","  \n"), # https://blog.csdn.net/duke10/article/details/81033686
                            extensions=[
                            'markdown.extensions.extra',
                            'markdown.extensions.codehilite',
                            'markdown.extensions.toc', 
                        ])