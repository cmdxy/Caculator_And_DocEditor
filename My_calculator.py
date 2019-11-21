#cumt 高级语言程序设计课程作业
#很大程度参考了别人的代码

import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *


accuracy = 10
def to_bin(num):
    if num < 0 :
        num = -num
        is_ne = True
    else:
        is_ne = False
    #判断是否为浮点数
    if num - int(num) < 1e-6:
        #若为整数
        integer = bin(int(num))
        if is_ne :   
            return '-' + integer
        else :
            return integer
    else:
        #若为浮点数
        #取整数部分
        integer = int(num)
        #取小数部分
        flo = num - integer
        #整数部分进制转换
        integercom = bin(integer)
        #小数部分进制转换
        tem = flo
        tmpflo = []
        for i in range(accuracy):
            tem *= 2
            tmpflo += str(int(tem))
            tem -= int(tem)
        flocom = tmpflo
        if is_ne:
            return '-' + integercom + '.' + ''.join(flocom)
        else:
            return integercom + '.' + ''.join(flocom)

def to_oct(num):
    #判断是否为浮点数
    if num < 0 :
        num = -num
        is_ne = True
    else:
        is_ne = False
    if num - int(num) < 1e-6:
        #若为整数
        integer = oct(int(num))
        if is_ne :   
            return '-' + integer
        else :
            return integer
    else:
        #若为浮点数
        #取整数部分
        integer = int(num)
        #取小数部分
        flo = num - integer
        #整数部分进制转换
        integercom = oct(integer)
        #小数部分进制转换
        tem = flo
        tmpflo = []
        for i in range(accuracy):
            tem *= 8
            tmpflo += str(int(tem))
            tem -= int(tem)
        flocom = tmpflo
        if is_ne:
            return '-' + integercom + '.' + ''.join(flocom)
        else:
            return integercom + '.' + ''.join(flocom)

#change to 16
def base(num):
    if 0<=num<=9 :
        return str(num)
    elif num == 10 :
        return 'a'
    elif num == 11 :
        return 'b'
    elif num == 12 :
        return 'c'
    elif num == 13:
        return 'd'
    elif num == 14:
        return 'e'
    elif num == 15:
        return 'f'
    
def to_hex(num):
    if num < 0 :
        num = -num
        is_ne = True
    else:
        is_ne = False
    if num - int(num) < 1e-6:
        #若为整数/avoid the bug when input 2.0
        integer = hex(int(num))
        if is_ne :   
            return '-' + integer
        else :
            return integer
    else:
        #若为浮点数
        #取整数部分
        integer = int(num)
        #取小数部分
        flo = num - integer
        #整数部分进制转换
        integercom = hex(integer)
        #小数部分进制转换
        tem = flo
        tmpflo = []
        for i in range(accuracy):
            tem *= 16
            tmpflo += base(int(tem))
            tem -= int(tem)
        flocom = tmpflo
        if is_ne:
            return '-' + integercom + '.' + ''.join(flocom)
        else:
            return integercom + '.' + ''.join(flocom)
        

# 计算二元
def get_result(num_a, num_b, operator):
    result = 0
    if operator == '+':
        result = num_a + num_b
    elif operator == '-':
        result = num_a - num_b
    elif operator == '×':
        result = num_a * num_b
    elif operator == '÷':
        result = num_a / num_b
    elif operator == 'X^Y':
        result = num_a ** num_b
    elif operator == 'mod':
        result = num_a % num_b
    return result



#主类    
class calculator(QWidget):

    def __init__(self):
        super().__init__()   
        # 按钮
        self.button_names = ['AC', 'Bin', 'Oct', 'Hex',
                             'X!', '+/-', 'X^Y', '÷',
                            
                             '7', '8', '9', '×',
                            
                             '4', '5', '6', '-',
                           
                             '1', '2', '3', '+',
                            
                             '0', '.', 'mod', '=']
        # 数字符号
        self.num_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
        # 二元运算符
        self.operator_names = ['X^Y', '÷', '×', '-', '+', 'mod']
     
        # 二元算符优先级字典，幂运算和模运算优先级最高，乘除次之，加减再次
        self.priority_dict = {'X^Y': 4, 'mod': 3, '×': 2, '÷': 2, '+': 1, '-': 1}
        # 数字队
        self.num_list = [0]

        '''
        #修bug，2019.11.20，用于修复 类似 A*B(-)^C 打的补丁
        self.num_back = [0]
        self.op_back = []
        '''

        # 二元符号队
        self.operator_list = []
        # 记录当前数字和当前符号
        self.num, self.operator = 0, 0
        self.num_inputting, self.operator_inputting = False, False
        # 这是label中要显示的内容/初始化为0，避免开始点'.'会卡住
        self.label_show = '0'
        #测试：record_label
        self.record_show = ''
        #点击了符号是self.last置False ,点击了符号数字self.last置True，self.per_last同理
        self.last = False
        self.per_last = self.last
        
        self.initUI()

    def initUI(self):
        '''关于下面，这些变量要不要加self限定，reference: https://www.cnblogs.com/ydf0509/p/9435677.html
        不加self就相当于是局部变量，不方便后面实现计算功能'''
        
        #设置样式,不必要的功能
        #self.setStyleSheet("background-color: rgb(205, 255, 255)")
        
        # 上下布局
        self.vbox = QVBoxLayout()
        
        # label用作输出/ #设置数字靠右显示
        self.num_line = QLabel()
        self.num_line.setAlignment(Qt.AlignRight)
        self.num_line.setText('0')

        # 测试：record_label输出记录/ #设置数字靠右显示
        self.record_line = QLabel()
        self.record_line.setAlignment(Qt.AlignRight)
        self.record_line.setText('')
        
        # self.num_line.setAutoFillBackground(True)
        self.vbox.addWidget(self.record_line)
        self.vbox.addWidget(self.num_line)
        self.grid = QGridLayout()
        
        # grid.setSpacing(5) 设置按键间隔
        self.vbox.addLayout(self.grid)
        self.setLayout(self.vbox)

        '''学习官方文档样例的写法:先造一个元组数组
            下面的循环将name和position对应起来，并在对应位置创造按纽
        '''
        positions = [(i, j) for i in range(6) for j in range(4)]
        for position, name in zip(positions, self.button_names):
            button = QPushButton(name) #creat  button
            button.clicked.connect(self.button_clicked) #link button to event , 传递事件的函数,button_click是自己实现的
            self.grid.addWidget(button, *position) #添加附件

        self.setWindowTitle('My_Calculator') #设置程序框名称
        self.show() 


    
    def button_clicked(self):
        
        sender = self.sender()
            
        #输入数字/注意条件改了
        if sender.text() in self.num_names and not(sender.text()=='.'and eval(self.label_show)%1 != 0 ) :
            #如果上一次也是输入数字，把上次存的数弹出
            if self.last == True and self.num_list:
                self.num_list.pop()
            
            self.last = True
            
            # 如果状态num_inputting已经设置为true,说明这不是输入的第一个数字
            if self.num_inputting:
                if self.label_show == '0':
                    self.label = ''
                self.label_show += sender.text()   #用字符串处理,lable_show 和 sender.text 都是字符串 
            else: #这是输入的第一个数字，更改相关状态，特殊情况‘0’      
                self.num_inputting = True   
                self.operator_inputting = False
                if sender.text() != '.':
                    self.label_show = sender.text()
                else :
                    self.label_show += '.'

                #测试
                if self.record_line.text() and self.record_line.text()[-1] == '=':
                    self.record_line.setText('')
                #测试/固定样式
                self.record_show = self.record_line.text()
            
            # 内部控制            
            # eval在这里起到将字符串转为数字的功能
            self.num_line.setText(self.label_show)
            #测试/临时样式
            self.record_line.setText(self.record_show + self.label_show)

            self.num = eval(self.label_show)
            self.num_list.append(self.num)

        elif sender.text() == '+/-'and self.num_list  :
            self.last = False
            # 内部控制
            self.num_list[-1] = -self.num_list[-1]
            # 表现
            self.label_show = str(self.num_list[-1])
            self.num_line.setText(self.label_show)
            self.num = -self.num



        #输入运算符
        elif sender.text() in self.operator_names and self.num_list :

            #测试/固定样式/如果上次点击的是数字
            if self.last :
                self.record_show = self.record_line.text() 

                #边界/如果上次点了等于号
                if self.record_line.text() and self.record_line.text()[-1] == '=':
                    self.record_line.setText(self.num_line.text())
                    self.record_show = self.num_line.text()

                if sender.text() == 'X^Y':
                    self.record_line.setText(self.record_show + '^')
                else:
                    self.record_line.setText(self.record_show + sender.text())

            self.per_last = self.last
            self.last = False
            

            #增加程序健壮性：如果多次点击，取最近点击的符号/这里引入了self.per_last 
            if self.per_last == False and self.operator_list :
                    self.operator_list.pop()
                    self.operator_inputting = False #一定要加这句

                    #测试/临时样式
                    if sender.text() == 'X^Y':
                        self.record_line.setText( self.record_show + '^'  )
                    else:
                        self.record_line.setText(self.record_show + sender.text())
                    
            #储存当前输入的运算符
            if not self.operator_inputting:
                self.num_inputting = False
                self.operator_inputting = True 

                '''
                #测试 by charles
                self.num_list = self.num_back
                self.operator_list = self.op_back
                '''



                '''
                若算符队列里有算符，则要将优先级大于等于x的算符全部计算并显示结果
                这样就保证了这是单调列表，下面的while用到了这个特性
                '''
                
                result_num = self.num
                while len(self.operator_list):
                    if self.priority_dict[self.operator_list[-1]] >= self.priority_dict[sender.text()]:
                        num_b = self.num_list.pop()
                        num_a = self.num_list.pop()
                        op = self.operator_list.pop()
                        result_num = get_result(num_a, num_b, op)
                        self.num = result_num
                        self.num_list.append(result_num)
                    else:
                        break

                self.label_show = str(self.num)
                self.num_line.setText(self.label_show)
                self.operator_list.append(sender.text())


        #结算/处理队列里的运算符
        elif sender.text() == '='and self.num_list  :

            #测试
            self.record_show = self.record_line.text()
            #如果上次输入的是数字或等于号 失效
            if self.record_line.text()[-1] != '=' and self.last :
                self.record_line.setText(self.record_show+'=')

            print('数字：', self.num_list)
            print('运算符：', self.operator_list)
            # 若按下等号，则全部计算直接得到结果
            result_num = self.num
            while len(self.operator_list):
                num_b = self.num_list.pop()
                num_a = self.num_list.pop()
                op = self.operator_list.pop()
                result_num = get_result(num_a, num_b, op)
                print("ans:",result_num)
                self.num = result_num
                self.num_list.append(result_num)
               
            self.label_show = str(self.num)
            self.num_line.setText(self.label_show)
            self.num_inputting = False 

            
        #一系列进制转换        
        elif sender.text() == 'Bin':
            if not ( self.num_line.text()[0:2] == '0b' or self.num_line.text()[0:3] == '-0b' )  :
                temp = to_bin(self.num)
                self.num_line.setText(temp)
            else:
                self.num_line.setText(str(self.num))
       
            
        elif sender.text() == 'Hex':
           if not ( self.num_line.text()[0:2] == '0x' or self.num_line.text()[0:3] == '-0x' )  :
               temp = to_hex(self.num)
               self.num_line.setText(temp)
           else:
               self.num_line.setText(str(self.num))
           


        elif sender.text() == 'Oct':
           if not ( self.num_line.text()[0:2] == '0o' or self.num_line.text()[0:3] == '-0o' ) :
               temp = to_oct(self.num)
               self.num_line.setText(temp)
           else:
               self.num_line.setText(str(self.num))
           


       # 算阶乘
        elif  sender.text() == 'X!'and self.num_list:

            #测试/如果是在等于号后面
            if self.record_line.text() and (self.record_line.text()[-1] == '=' or self.record_line.text()[-1] == '!'):
                self.record_line.setText('('+self.num_line.text()+')!')
                self.record_show = self.record_line.text()
            else:
                self.record_line.setText(self.record_show+'('+self.num_line.text()+')!')
                self.record_show = self.record_line.text()
          


            
            n = self.num_list[-1]
            #if is not a float
            if type(n) == int:	
            	self.num_list.pop()
            	#算阶乘循环
            	num_a = 1
            	for i in range(1,n+1): num_a = num_a * i
            	self.num = num_a
            	self.num_list.append(num_a)
            	self.num_line.setText(str(num_a))
            else:
            	self.num_line.setText("NaN")

        #清空还原初始化    
        elif sender.text() == 'AC':
            #测试
            self.record_line.setText('')
            self.record_show = ''

            self.operator_list.clear()
            #self.num_list.clear()
            self.num_list = [0]
            self.num = 0
            self.label_show = '0'
            self.num_line.setText('0')
            self.num_inputting = False
            self.operator_inputting = False
            self.last = False
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = calculator()
    sys.exit(app.exec_())
