import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import *
import random

class Game(GridLayout):
	def __init__(self, **kwargs):
		super(Game, self).__init__(**kwargs)
		self.game_over = False
		
		#colours
		self.red = (1, 0, 0, 1)
		self.green = (0, 1, 0, 1)
		self.blue = (0, 0, 1, 1)
		self.yellow = (1, 1, 0, 1)
		self.cyan = (0, 1, 1, 1)
		self.black = (0, 0, 0, 1)
		self.white = (1, 1, 1, 1)
		self.grey = (0.5, 0.5, 0.5, 1)
		self.orange = (1, 0.5, 0, 1)
		self.pink = (1, 0.5, 1, 1)
		self.lime = (0.5, 1, 0, 1)
		
		#background
		self.width, self.height = 720, 1440
		with self.canvas:
			Color(rgba=(0.5, 0.5, 1, 1))
			Rectangle(size=(self.width, self.height))
			
		#heading
		head = Label(text="Hangman!!!", pos=((self.width/2)-40, (self.height/2)+250), font_size=70, color=(0.5, 1, 0, 1))
		self.add_widget(head)
		
		#word
		file = open("words.txt", "r")
		self.words = []
		for line in file:
			self.words.append(line)
		file.close()
		
		self.word = (self.words[random.randint(0, 99)]).strip()
		
		self.length = len(self.word)
		
		self.wordLabel = Label(text="", font_size=45, pos=(self.width/2-40, self.height/2+100), color=self.cyan)
		for i in range(self.length):
			self.wordLabel.text += "~"
			
		self.add_widget(self.wordLabel)
		
		#incorrect attempts
		self.incorrect = 0
		self.incLabel = Label(text=f"Attempts left(max 6): {6-self.incorrect}", pos=((self.width/2)-30, (self.height/2)+180), font_size=40, color=(0.5, 1, 0, 1))
		self.add_widget(self.incLabel)
		
		#buttons
		self.buttons = []
		self.letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
		
		for j in range(self.length*2):
			self.buttons.append("")
			
		self.blacklisted = []
		for j in range(self.length):
			self.num = random.randint(0, self.length*2-1)
			while self.buttons[self.num] != "" or self.num in self.blacklisted:
				self.num = random.randint(0, self.length*2-1)
				
			self.blacklisted.append(self.num)
			self.buttons[self.num] = self.word[j]
			
		for j in range(self.length):
			self.num = random.randint(0, self.length*2-1)
			while self.buttons[self.num] != "" or self.num in self.blacklisted:
				self.num = random.randint(0, self.length*2-1)
				
			i = random.randint(0, 25)
			while self.letters[i] in self.word: 
				i = random.randint(0, 25)
				
			self.blacklisted.append(self.num)
			self.buttons[self.num] = self.letters[i]
			
		x = 10
		y = self.height/2 - 40
		
		self.btn = []
		for i in range(self.length*2):
			self.btn.append(Button(text=self.buttons[i], pos=(x, y), size=(70, 70), background_color=self.cyan, color=self.yellow))
			self.btn[i].bind(on_press=self.check)
			self.add_widget(self.btn[i])
			
			x += 100
			if x >= self.width-50:
				y -= 100
				x = 10
				
		#win label
		self.win1 = Label(text="", font_size=100, color=self.yellow, pos=((self.width/2)-40, (self.height/2)+400))
		self.add_widget(self.win1)
		
		self.win2 = Label(text="", font_size=40, color=self.yellow, pos=((self.width/2)-40, (self.height/2)+320))
		self.add_widget(self.win2)
		
		#reset button		
		self.resetButton = Button(text="Reset", size=(140, 70), pos=(self.width/2-70, self.height/2-500), background_color=self.pink, color=self.lime)
		self.resetButton.bind(on_press=self.reset)
		self.add_widget(self.resetButton)
				
	def check(self, instance):
		#check
		if self.game_over == False:
			if instance.text in self.word:
				self.incLabel.color = self.lime
				for i in range(self.length):
					if self.wordLabel.text[i] == "~" and self.word[i] == instance.text:
						self.wordLabel.text = self.wordLabel.text[:i] + instance.text + self.wordLabel.text[i+1:]
						break
			else:
				self.incLabel.color = self.red
				self.incorrect += 1
				self.incLabel.text = f"Attempts left(max 6): {6-self.incorrect}"

			#remove button
			instance.pos = (800, 720)
		
		#check win and fail
		if self.incorrect == 6:
			self.game_over = True
			self.win1.color = self.red
			self.win2.color = self.red
			self.win1.text = "Sorry, you lost!"
			self.win2.text = f"The word was {self.word}."
			
		elif "~" not in self.wordLabel.text:
			self.game_over = True
			self.win1.color = self.green
			self.win2.color = self.green
			self.win1.text = "Correct!"
			self.win2.text = f"The word was {self.word}."
			
	def reset(self, instance):
		self.incLabel.color = self.lime
		for i in self.btn:
			if i.pos != (800, 720):
				i.pos = (800, 720)
				i.text = ""
				
		self.win1.text = ""
		self.win2.text = ""
		self.game_over = False
		self.incorrect = 0
		self.incLabel.text = f"Attempts left(max 6): {6-self.incorrect}"
		self.word = (self.words[random.randint(0, 99)]).strip()
		self.length = len(self.word)
		
		self.wordLabel.text = ""
		for i in range(self.length):
			self.wordLabel.text += "~"
		
		#reseting the buttons	
		x = 10
		y = self.height/2 - 40
		self.blacklisted = []
		
		if self.length*2 <= len(self.btn):
			for i in range(self.length*2):
				self.btn[i].pos = (x, y)
				x += 100
				if x >= self.width-50:
					y -= 100
					x = 10
					
			for j in range(self.length):
				self.num = random.randint(0, self.length*2-1)
				while self.btn[self.num].text != "" or self.num in self.blacklisted:
					self.num = random.randint(0, self.length*2-1)
				
				self.blacklisted.append(self.num)
				self.btn[self.num].text = self.word[j]
			
			for j in range(self.length):
				self.num = random.randint(0, self.length*2-1)
				while self.btn[self.num].text != "" or self.num in self.blacklisted:
					self.num = random.randint(0, self.length*2-1)
				
				i = random.randint(0, 25)
				while self.letters[i] in self.word: 
					i = random.randint(0, 25)
				
				self.blacklisted.append(self.num)
				self.btn[self.num].text = self.letters[i]
		
		else:		
			for i in range((self.length*2)-len(self.btn)):
				self.btn.append(Button(text="", pos=(800, 720), size=(70, 70), background_color=self.cyan, color=self.yellow))
				self.btn[-1].bind(on_press=self.check)
				self.add_widget(self.btn[-1])
				
			for i in range(self.length*2):
				self.btn[i].pos = (x, y)
				x += 100
				if x >= self.width-50:
					y -= 100
					x = 10
				
			for j in range(self.length):
				self.num = random.randint(0, self.length*2-1)
				while self.btn[self.num].text != "" or self.num in self.blacklisted:
					self.num = random.randint(0, self.length*2-1)
				
				self.blacklisted.append(self.num)
				self.btn[self.num].text = self.word[j]
			
			for j in range(self.length):
				self.num = random.randint(0, self.length*2-1)
				while self.btn[self.num].text != "" or self.num in self.blacklisted:
					self.num = random.randint(0, self.length*2-1)
				
				i = random.randint(0, 25)
				while self.letters[i] in self.word: 
					i = random.randint(0, 25)
				
				self.blacklisted.append(self.num)
				self.btn[self.num].text = self.letters[i]
					
class MyApp(App):
	def build(self):
		return Game()
		
if __name__ == "__main__":
	MyApp().run()
