import SharedData
import WindowManager as WM
import UI

import pygame
import os

surface = None
surfaceOffsetX = SharedData.leftPanelWidth


""" store the currently displayed image at its native resolution """
originalImage = None
""" the resized version that is blitted on the screen """
resizedImage = None


""" the image offset without the current panning"""
imgOffsetX = 0
imgOffsetY = 0

""" the image offset, taking into account the current panning being done """
imgOffsetPannedX = 0
imgOffsetPannedY = 0

resizeRatio = 1

panningEnabled = False


""" constants for the UI's appearance"""

handleSize = 10
minHandleDistance = 10
hoverColorMod = [100, 100, 100]

""" the label that is being hovered over by the mouse. There can only be one, to avoid confusion. The order of priority is random, any label that detect the mouse
is hovering over them will set this variable to their reference. Updated every time the mouse moves """
focusedLabel = None


""" the last known mouse pos """
mouseX = 0
mouseY = 0
mouseInWindow = False

""" the mouse's position when panning was started """
panStartX = 0
panStartY = 0





updateUI = False

labelFile = None



rects = []

temp = 0


class RectHandle(UI.PushButton) :

	def __init__(self, x, y, w, h, updateCallback=None, text="", upperCorner = None, lowerCorner = None):

		self.fracX = x
		self.fracY = y

		x, y = self.ConvertFracToPx(x, y)

		super().__init__(x, y, w, h, updateCallback, text)
	
		self.followMouse = False

		# other RectHandle objets that it cannot go higher or lower in term of coordinates
		self.upperCorner = upperCorner
		self.lowerCorner = lowerCorner
	
	def ConvertFracToPx(self, x, y) :
		#return int(x * resizedImage.get_width()) + SharedData.leftPanelWidth, int(y * resizedImage.get_height())
		return int(x * resizedImage.get_width()) + imgOffsetPannedX, int(y * resizedImage.get_height() + imgOffsetPannedY)
	
	def ConvertPxToFrac(self, x, y) :
		return (x - imgOffsetPannedX) / resizedImage.get_width(), (y - imgOffsetPannedY) / resizedImage.get_height()
	
	def Hovered(self, x, y):
		return super().Hovered(x - SharedData.leftPanelWidth, y)

	def MouseClicked(self):
		super().MouseClicked()
		self.followMouse = True
	
	def MouseReleased(self):
		super().MouseReleased()
		self.followMouse = False
	
	def MouseMoved(self, x, y) :
		if not self.followMouse : return

		self.x = x - SharedData.leftPanelWidth
		self.y = y

		if self.upperCorner != None :
			self.x = min(self.x, self.upperCorner.x - minHandleDistance)
			self.y = min(self.y, self.upperCorner.y - minHandleDistance)
		
		if self.lowerCorner != None :
			self.x = max(self.x, self.lowerCorner.x + minHandleDistance)
			self.y = max(self.y, self.lowerCorner.y + minHandleDistance)
		
		x = max(x, 0)

		self.fracX, self.fracY = self.ConvertPxToFrac(self.x, self.y)


		global updateUI
		updateUI = True
	
	def Draw(self, surface):

		self.x, self.y = self.ConvertFracToPx(self.fracX, self.fracY)

		return super().Draw(surface)
	



class AdjustableRect :

	""" x and y are the center of the box """
	def __init__(self, objectID : int, x : int, y : int, w : int, h : int):

		self.objectID = objectID

		x1 = x - w / 2
		y1 = y - h / 2
		x2 = x + w / 2
		y2 = y + h / 2
		
		self.leftHandle = RectHandle(x1, y1, handleSize, handleSize, RequestUpdateUI, "")
		self.rightHandle = RectHandle(x2, y2, handleSize, handleSize, RequestUpdateUI, "")
		self.leftHandle.upperCorner = self.rightHandle
		self.rightHandle.lowerCorner = self.leftHandle

		self.color = [0, 0, 0]
	
	def MouseMoved(self, x, y) :
		global focusedLabel

		self.leftHandle.MouseMoved(x, y)
		self.rightHandle.MouseMoved(x, y)

		if self.rightHandle.hovered or self.leftHandle.hovered :
			focusedLabel = self
	
	def Draw(self, surface) :
		global focusedLabel

		""" take the fractional values because else the pixel values might not be updated yet """
		x1, y1 = self.leftHandle.ConvertFracToPx(self.leftHandle.fracX, self.leftHandle.fracY)
		x2, y2 = self.rightHandle.ConvertFracToPx(self.rightHandle.fracX, self.rightHandle.fracY)

		self.color[0] = SharedData.classColors[self.objectID][0]
		self.color[1] = SharedData.classColors[self.objectID][1]
		self.color[2] = SharedData.classColors[self.objectID][2]

		# if one of the handles is being hovered, make the color brighter
		if focusedLabel == self :
			self.color[0] = min(self.color[0] + hoverColorMod[0], 255)
			self.color[1] = min(self.color[1] + hoverColorMod[1], 255)
			self.color[2] = min(self.color[2] + hoverColorMod[2], 255)
		
			

		pygame.draw.rect(surface, self.color, pygame.rect.Rect(x1, y1, x2 - x1, y2 - y1), 1, 1)

		self.leftHandle.Draw(surface)
		self.rightHandle.Draw(surface)
	
	def __del__(self) :
		
		self.leftHandle.Delete()
		self.rightHandle.Delete()
	
	def Serialize(self) :

		centerX = (self.leftHandle.fracX + self.rightHandle.fracX) / 2
		centerY = (self.leftHandle.fracY + self.rightHandle.fracY) / 2

		width = abs(self.rightHandle.fracX - self.leftHandle.fracX)
		height = abs(self.rightHandle.fracY - self.leftHandle.fracY)

		return f"{self.objectID} {centerX} {centerY} {width} {height}"

def CalculateAvailableSpace() :

	global surface, surfaceOffsetX
	width = WM.display.get_width() - SharedData.leftPanelWidth
	height = WM.display.get_height()

	surface = pygame.surface.Surface((width, height))
	surfaceOffsetX = SharedData.leftPanelWidth


""" open the image with the given name, and resize it to """
def OpenImage(fileName : str) :

	global originalImage
	global rects

	CloseImage()

	rects = []

	originalImage = pygame.image.load(os.path.join(SharedData.imagePath, fileName))


	AdjustImage()	

	global labelFile
	labelFile = SharedData.filePairs[fileName]

	if labelFile != None :

		results = SharedData.ReadRectFile(labelFile)
		print(results)

		for result in results :
			
			rects.append(AdjustableRect(result[0], result[1], result[2], result[3], result[4]))

""" save rectangle modifications """
def CloseImage() :

	if len(rects) == 0 : return
	if labelFile == None : return
	
	lines = []
	for rect in rects :
		lines.append(rect.Serialize())
	
	SharedData.WriteRectFile(labelFile, lines)


def AdjustImage() :

	if originalImage == None : return

	global resizedImage, resizeRatio

	widthRatio = surface.get_width() / originalImage.get_width()
	heightRatio = surface.get_height() / originalImage.get_height()

	resizeRatio = min(widthRatio, heightRatio)

	ResizeImage()

def ResizeImage() :

	global resizedImage, resizeRatio

	resizedImage = pygame.transform.scale(originalImage, (int(originalImage.get_width() * resizeRatio), int(originalImage.get_height() * resizeRatio)))


def MouseMovement(x, y) :
	global mouseX, mouseY, mouseInWindow
	global updateUI
	global focusedLabel

	mouseX = x
	mouseY = y

	focusedLabel = None

	for rect in rects :

		rect.MouseMoved(x, y)
	
	if panningEnabled : updateUI = True

	if x > SharedData.leftPanelWidth :
		mouseInWindow = True
	else :
		mouseInWindow = False
	

def Draw() :
	global updateUI

	global temp
	temp += 1
	print(f"draw {temp}")

	surface.fill([255, 255, 255])

	PanImage()

	if resizedImage != None :
		surface.blit(resizedImage, (imgOffsetPannedX, imgOffsetPannedY))
	
	for rect in rects :
		rect.Draw(surface)

	WM.display.blit(surface, (SharedData.leftPanelWidth, 0))

	updateUI = False

""" activate or deactivate panning with the mouse's movement """
def EnablePanning(enable : bool) :
	global panningEnabled
	global panStartX, panStartY

	global imgOffsetY, imgOffsetX, imgOffsetPannedY, imgOffsetPannedX

	panningEnabled = enable

	
	if enable :
		""" store where the mouse was when we started panning """
		panStartX = mouseX
		panStartY = mouseY
		print("startpan")
	else :
		""" apply panning changes we made """
		imgOffsetX = imgOffsetPannedX
		imgOffsetY = imgOffsetPannedY

		print("stoppan")


""" responsible for calculating the panning of the image of we are currently whanging it """
def PanImage() :
	if not panningEnabled : return

	print("panning")

	global imgOffsetPannedX, imgOffsetPannedY, imgOffsetX, imgOffsetY
	global updateUI

	imgOffsetPannedX = imgOffsetX + mouseX - panStartX
	imgOffsetPannedY = imgOffsetY + mouseY - panStartY

	BoundPanning()

	updateUI = True


def BoundPanning() :
	global imgOffsetPannedY, imgOffsetPannedX

	imgOffsetPannedX = max(imgOffsetPannedX, surface.get_width()- resizedImage.get_width())
	imgOffsetPannedX = min(imgOffsetPannedX, 0)

	imgOffsetPannedY = max(imgOffsetPannedY, surface.get_height() - resizedImage.get_height())
	imgOffsetPannedY = min(imgOffsetPannedY, 0)


def Zoom(value) :

	if panningEnabled : return # cannot pan and zoom at the same time

	print("scroll")

	global resizeRatio, updateUI
	global imgOffsetY, imgOffsetX
	global imgOffsetPannedY, imgOffsetPannedX

	if not mouseInWindow : return


	oldWidth = originalImage.get_width() * resizeRatio
	oldHeight = originalImage.get_height() * resizeRatio

	print("scale change")

	# multiplying by resize ratio prevent the zoom from being slower at high zoom values
	resizeRatio += value * resizeRatio / 10

	resizeRatio = max(resizeRatio, 0.1)

	ResizeImage() # important to put before BoundPanning because it uses the dimensions of the resized image

	""" move the image so that the currently viewed part of the image stays at the center"""
	imgOffsetPannedX += (oldWidth - originalImage.get_width() * resizeRatio) // 2
	imgOffsetPannedY += (oldHeight - originalImage.get_height() * resizeRatio) // 2

	BoundPanning()

	imgOffsetX = imgOffsetPannedX
	imgOffsetY = imgOffsetPannedY
	

	updateUI = True

# used by rectangle handles
def RequestUpdateUI() :
	global updateUI

	updateUI = True


# add a new label at the center of the screen
def AddLabel() :

	rects.append(AdjustableRect(0, 0.5, 0.5, 0.5, 0.5))

	RequestUpdateUI()

def DeleteFocusedLabel() :
	if focusedLabel == None : return

	rects.remove(focusedLabel)

	RequestUpdateUI()


def SetFocusedLabelObject(num) :
	if focusedLabel == None : return

	focusedLabel.objectID = num

	RequestUpdateUI()