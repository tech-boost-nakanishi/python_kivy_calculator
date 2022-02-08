import japanize_kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import BooleanProperty

Builder.load_file('main.kv')

class RoundedButton(ButtonBehavior, Label):

	def collide_point(self, x, y):
		return Vector(x, y).distance(self.center) <= self.width / 2

class CalcWidgets(Widget):
	result = StringProperty()
	currentOp = StringProperty()
	isPressed = BooleanProperty()
	moveCount = NumericProperty(0)

	def __init__(self, **kwargs):
		super(CalcWidgets, self).__init__(**kwargs)
		self.result = '0'
		self.currentOp = ''
		self.stackedValue = 0
		self.isPressed = False
		self.afterCalc = False
		self.isStacked = False

	def ClearPressed(self):
		self.isPressed = False
		self.afterCalc = False
		self.isStacked = False
		self.result = '0'
		self.currentOp = ''

	def PlusMinusPressed(self):
		self.isPressed = False
		if '-' in self.result:
			self.result = str(self.result).replace('-', '')
		else:
			self.result = '-' + self.result

	def PercentPressed(self):
		self.afterCalc = True
		self.isPressed = False
		self.result = str(float(self.result) / 100)
		if self.result == '0.0':
			self.result = '0'

	def NumPressed(self, num):
		if num == 0:
			# 0の場合
			if self.afterCalc or self.result == '0':
				self.result = '0'
			else:
				self.result = self.result + '0'
		elif num >= 1 and num <= 9:
			# 1〜9の場合
			if self.afterCalc or self.result == '0':
				self.result = str(num)
			else:
				self.result = str(self.result) + str(num)
		self.isPressed = True
		self.afterCalc = False

	def CalcPressed(self, calc):
		self.afterCalc = True
		self.isStacked = True
		if self.result == '数値ではありません':
			return
		self.stackedValue = float(self.result)
		if calc == '+':
			self.currentOp = '+'
		elif calc == '-':
			self.currentOp = '-'
		elif calc == '*':
			self.currentOp = '*'
		elif calc == '/':
			self.currentOp = '/'

	def PeriodPressed(self):
		self.isPressed = True
		self.afterCalc = False
		if '.' not in self.result:
			self.result = self.result + '.'
		if self.afterCalc:
			self.result = '0.'

	def EqualPressed(self):
		self.afterCalc = True
		self.isStacked = False
		self.isPressed = False
		if self.result == '数値ではありません':
			return
		value = float(self.result)
		if self.currentOp == '+':
			self.stackedValue += value
		elif self.currentOp == '-':
			self.stackedValue -= value
		elif self.currentOp == '*':
			self.stackedValue *= value
		elif self.currentOp == '/':
			if value == 0.0:
				self.result = '数値ではありません'
				return
			else:
				self.stackedValue /= value
		if self.stackedValue % 1 == 0:
			self.result = str(int(self.stackedValue))
		elif self.stackedValue == '0.0':
			self.result = '0'
		else:
			self.result = str(self.stackedValue)

		self.currentOp = ''

	def LastStringDelete(self):
		if self.isPressed:
			st = str(self.result)[:-1]
			if st == '' or st == '-':
				self.result = '0'
			else:
				self.result = st

	def on_touch_move(self, touch):
		if self.ids.label1.collide_point(*touch.pos):
			self.moveCount += 1
			if self.moveCount == 5:
				self.LastStringDelete()

	def on_touch_up(self, touch):
		if self.ids.label1.collide_point(*touch.pos):
			self.moveCount = 0

class CalcApp(App):
	splits = NumericProperty(4)
	padding = NumericProperty(8)
	width = NumericProperty()
	height = NumericProperty()
	
	def __init__(self, **kwargs):
		super(CalcApp, self).__init__(**kwargs)
		self.title = '電卓'
		self.width, self.height = Window.size

	def build(self):
		return CalcWidgets()

if __name__=='__main__':
	CalcApp().run()