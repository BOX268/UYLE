import pygame
import sys

import WindowManager
import UI
import SharedData
import FileBar
import Canvas

pygame.init()

mainWindow = WindowManager.MainWindow()

SharedData.GetPaths()

UI.Init()

SharedData.ListFiles()

FileBar.Regenerate()

Canvas.CalculateAvailableSpace()

Canvas.Draw()


while True :


	for event in pygame.event.get() :

		if event.type == pygame.QUIT :
			Canvas.CloseImage()
			pygame.quit()
			sys.exit()
		
		if event.type == pygame.MOUSEBUTTONDOWN :

			if event.button == 1 : # left mouse button
				print("leftmousedown")
				canActivate = True
				for button in UI.pushButtons :
					
					 # can click only one button at once
					if button.Hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and canActivate :
						if canActivate :
							print("activation")
							button.MouseClicked() # mouseclicked ?? 

							canActivate = False

				for rectangle in Canvas.rects:
					if rectangle.IsInside_rectangle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
						print("inside the rectangle")
						rectangle.Dragging_Pressed(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])



			elif event.button == 3 : # right mouse button
				print("righmouseown")
				Canvas.EnablePanning(True)
						
		
		elif event.type == pygame.MOUSEBUTTONUP :

			if event.button == 1 :

				for button in UI.pushButtons :
					button.MouseReleased()

				for rectangle in Canvas.rects:
					rectangle.MouseReleased()
			
			elif event.button == 3 :
				Canvas.EnablePanning(False)

		
		elif event.type == pygame.MOUSEMOTION :
			pos = pygame.mouse.get_pos()
			for button in UI.pushButtons : button.Hovered(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
			FileBar.IsMouseInMenu(pos[0], pos[1])

			Canvas.MouseMovement(pos[0], pos[1])

		elif event.type == pygame.MOUSEWHEEL :

			FileBar.MouseScroll(event.y)
			Canvas.Zoom(event.y)

		elif event.type == pygame.VIDEORESIZE :

			Canvas.CalculateAvailableSpace()
			#Canvas.ScaleImage()
			Canvas.Draw()
			FileBar.Draw()
		
		elif event.type == pygame.KEYDOWN :

			if event.key == pygame.K_a :
				Canvas.AddLabel()
			
			elif event.key == pygame.K_c :
				Canvas.copy_rectangle()

			elif event.key == pygame.K_v :
				Canvas.paste_rectangle()

			elif event.key == (pygame.K_d) or event.key ==(pygame.K_BACKSPACE) :
				Canvas.DeleteFocusedLabel()
			
			elif event.key == pygame.K_0 :
				Canvas.lastObjectID = 0
				Canvas.SetFocusedLabelObject(0)
			elif event.key == pygame.K_1 :
				Canvas.lastObjectID = 1
				Canvas.SetFocusedLabelObject(1)
			elif event.key == pygame.K_2 :
				Canvas.lastObjectID = 2
				Canvas.SetFocusedLabelObject(2)
	
	if Canvas.updateUI : Canvas.Draw()

	

	pygame.display.flip()

