import os
content = './input/content/chicago.jpg'
style = './input/style/harvard_0.jpg'
os.system("python test.py  --content  %s  --style %s" % (content, style))
