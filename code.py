#-*-coding:utf-8-*-
#测试matplotlib中文字符集
import ch
ch.set_ch()
from matplotlib import pyplot as plt
plt.title(u'显示中文')
plt.show()