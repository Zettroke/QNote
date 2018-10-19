from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='short_file_label')
def short_file_label(value, char_num):
    dot = value.rfind('.')
    if len(value) > char_num:
        if dot == -1:
            return value[:char_num] + "..."
        else:
            ext = value[dot:]
            if len(ext) > char_num:
                return '... ' + ext
            else:
                return mark_safe(value[0:char_num - len(ext)] + '... <span style="word-break: normal">' + ext + '</span>')
    else:
        if dot == -1:
            return value
        else:
            ext = value[dot:]
            return mark_safe(value[0:len(value) - len(ext)] + '<span style="word-break: normal">' + ext + '</span>')
