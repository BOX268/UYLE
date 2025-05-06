import os
import sys
import json

PATH_FILE_NAME = "paths.txt"

imagePath = ""
labelPath = ""
fontPath = ""


filePairs = {}


leftPanelWidth = 200


classColors = [[0, 200, 0], [0, 0, 200], [200, 0, 0]]


# check if shared config file exists, else creates it
if not os.path.exists(PATH_FILE_NAME) :
	
	with open(PATH_FILE_NAME, "w") as f :

		basePaths = {
			"images_folder" : "",
			"labels_folder" : "",
			"font_path" : "font/ConsolaMono-Book.ttf",
			"autolabel_model_path" : ""
			}
		
		string = json.dumps(basePaths, sort_keys=True, indent=4)
		f.write(string)
		
	raise RuntimeError("config file was not present, it has been created. Please fill it")
	


def GetPaths() :

	global imagePath, labelPath, fontPath, modelPath

	with open(PATH_FILE_NAME, "r") as file :

		content = file.read()

		paths = json.load(content)

		imagePath = paths["images_folder"]
		labelPath = paths["labels_folder"]
		fontPath = paths["font_path"]

		print(imagePath)
		print(labelPath)
		print(fontPath)


def ListFiles() :

	filePairs.clear()

	imageFiles = os.listdir(imagePath)
	labelFiles = os.listdir(labelPath)

	imageFilesName = [os.path.splitext(os.path.basename(path))[0] for path in imageFiles]
	labelFilesName = [os.path.splitext(os.path.basename(path))[0] for path in labelFiles]

	for i in range(len(imageFiles)) :
		
		if imageFiles[i].endswith((".png", ".jpeg", ".jpg")) :
			
			if imageFilesName[i] in labelFilesName :
				filePairs[imageFiles[i]] = labelFiles[labelFilesName.index(imageFilesName[i])]
			else :
				filePairs[imageFiles[i]] = None
				
	
	print(filePairs)


def CompareFileNames(name1, name2) :

	name1 = os.path.basename(name1)
	name2 = os.path.basename(name2)

	return name1 == name2


def ReadRectFile(fileName) :


	result = []

	with open(os.path.join(labelPath, fileName), "r") as file :

		lines = file.readlines()

		for line in lines :

			line = line.strip()
			if line == "" or line == "\n" : continue

			contents = line.split(" ")
			
			if len(contents) != 5 : raise RuntimeError(f"invalid number of arguments in file {fileName}, only {len(contents)}, should be 5")

			contents[0] = int(contents[0].strip())
			for i in range(1, len(contents)) :
				contents[i] = float(contents[i].strip())
		
			result.append(contents)
	
	return result

def WriteRectFile(fileName, lines) :

	with open(os.path.join(labelPath, fileName), "w") as file :

		for line in lines :

			file.write(line + "\n")