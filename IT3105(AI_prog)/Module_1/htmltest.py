htmlString='<link rel="stylesheet" type="text/css" href="theme.css"><table>'

Matrix = [["O" for x in range(5)] for x in range(5)] 
Matrix[0][0] = "B"
Matrix[0][1] = "B"
Matrix[1][0] = "B"
Matrix[1][1] = "B"
Matrix[4][4] = "G"
Matrix[2][2] = "B"
Matrix[2][3] = "B"
Matrix[3][2] = "B"

cols=5
rows=5



for i in range(cols):
	htmlString = htmlString + "<tr>"
	for j in range(rows):
		if Matrix[i][j]=="O":
			htmlString = htmlString + '<td class="O">' + Matrix[i][j] + "</td>"
		elif Matrix[i][j]=="G":
			htmlString = htmlString + '<td class="G">' + Matrix[i][j] + "</td>"
		elif Matrix[i][j]=="B":
			htmlString = htmlString + '<td class="B">' + Matrix[i][j] + "</td>"
		elif Matrix[i][j]=="S":
			htmlString = htmlString + '<td class="S">' + Matrix[i][j] + "</td>"

		


	htmlString = htmlString + "</tr>"


def addClass(symbol):
	pass

f = open('myfile.html','w')
f.write(htmlString)
f.close()