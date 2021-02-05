import os
from test import using

content = './input/content/flowers.jpg'
style = './input/style/harvard_0.jpg'
alpha = 1.0


# os.system("python test.py  --content  %s  --style %s --alpha %f"  % (content, style,alpha))
# def Style(content_path,style_path,alpha=1.0):
def Style_():
    return using(content, style, alpha)

if __name__ == '__main__':
    print(Style_())