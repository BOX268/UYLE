import os


imagePath = ""
labelPath = ""

filePairs = {}


leftPanelWidth = 200


classColors = [[0, 200, 0], [0, 0, 200], [200, 0, 0]]


def GetPaths() :

	global imagePath, labelPath

	with open("paths.txt", "r") as file :

		lines = file.readlines()

		imagePath = lines[0].strip("\n")
		labelPath = lines[1].strip("\n")

		print(imagePath)
		print(labelPath)


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