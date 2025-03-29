import UI
import SharedData
import Canvas
import WindowManager as WM

import pygame

generatedButtons = []
scroll = 0

buttonHeight = 20
menuWidth = 200

mouseInMenu = False


class FileButton(UI.PushButton) :

	def __init__(self, x, y, w, h, updateCallback=None, text=""):
		super().__init__(x, y, w, h, updateCallback, text)
	
	def MouseClicked(self) :
		super().MouseClicked()

		global generatedButtons
		for button in generatedButtons : button.selected = False
		self.selected = True

		print(f"opening {self.text}")
		Canvas.OpenImage(self.text) # the button text is the image file name
		Canvas.Draw()




def Regenerate() :

	global generatedButtons

	for button in generatedButtons :
		button.Delete()
	
	generatedButtons = []

	SharedData.ListFiles()

	i = 0
	files = [key for key in SharedData.filePairs.keys()]
	files.sort()
	for file in files :

		generatedButtons.append(FileButton(0, i*buttonHeight, menuWidth, buttonHeight, Draw, file))
		i += 1
	
	Draw()


def IsMouseInMenu(x : int, y : int) :
	global mouseInMenu
	mouseInMenu = x > 0 and x < menuWidth
	return mouseInMenu

def MouseScroll(value : int) :
	global scroll
	if mouseInMenu :
		scroll += value * buttonHeight
		scroll = min(0, scroll)
	
		for i in range(len(generatedButtons)) :
			generatedButtons[i].y = i * buttonHeight + scroll
		
		Draw()


def Draw() :


	tempSurface = pygame.surface.Surface((menuWidth, WM.display.get_height()))

	pygame.draw.rect(tempSurface, [50, 50, 50], pygame.rect.Rect(0, 0, menuWidth, WM.display.get_height()))

	for button in generatedButtons :
		button.Draw(tempSurface)
	
	WM.display.blit(tempSurface, (0, 0), tempSurface.get_rect())