import pygame
import SharedData 
import WindowManager as WM


pushButtons = []
font = None

def Init() :
	global font
	font = pygame.font.Font(SharedData.fontPath)

class PushButton :

	def __init__(self, x : int, y : int, w : int, h : int, updateCallback = None, text = ""):
		
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.text = text

		self.hovered = False
		self.click = False

		self.selected = False

		# called when button need to change its appearance
		self.updateCallback = updateCallback
		
		global pushButtons
		pushButtons.append(self)

		self.SetText(text)
	
	def Delete(self) :
		try :
			pushButtons.remove(self)
		except :
			pass
	
	def SetText(self, text = "") :
		self.textSurface = font.render(text, True, [0, 0, 0])

	def Hovered(self, x : int, y : int) :
		inZone = x > self.x and x < self.x + self.w and y > self.y and y < self.y + self.h

		if self.hovered != inZone :
			self.hovered = inZone
			if self.updateCallback != None : self.updateCallback()

		self.hovered = inZone
		return inZone
	
	def MouseClicked(self) :
		print("honk")
	
	def MouseReleased(self) :
		pass
	
	def MousePressed(self) :
		pass

	def Draw(self, surface) :
		color = [80, 80, 80]
		if self.hovered : color = [70, 70, 70]

		pygame.draw.rect(surface, color, pygame.rect.Rect(self.x, self.y, self.w, self.h))

		surface.blit(self.textSurface, pygame.rect.Rect(self.x, self.y, self.w, self.h))




