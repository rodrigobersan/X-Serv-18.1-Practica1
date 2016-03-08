#!/usr/bin/python
import webapp

class AcortadorApp(webapp.webApp):
	Dic = {}
	Index = 0
	Form = '<form name="input" method="post">\nURL: <input type="text" name="URL">\n<input type="submit" value="Enviar">\n</form>'

	def parse(self, request):
		lines = request.splitlines()
		method = lines[0].split(' ')[0]
		resource = lines[0].split(' ')[1]
		if method == 'GET':
			url = ""
		elif method == "POST":
			if lines[-1][0:4] == "URL=":
				url = lines[-1].split('=')[1]
			else:
				url = ""
		
		parsedRequest = [method,resource,url]
		print parsedRequest
		return parsedRequest

	def process(self,parsedRequest):
		htmlBody = ''
		repetido = 0
		if parsedRequest[0] == "GET":
			htmlBody = "<h1>Bienvenido!! Introduce una URL para acortar</h1>" + self.Form
		elif parsedRequest[0] == "POST":
			if parsedRequest[2][0:13] == "http%3A%2F%2F":
				parsedRequest[2] = "http://" + parsedRequest[2][13:]
			elif parsedRequest[2][0:14] == "https%3A%2F%2F":
				parsedRequest[2] = "https://" + parsedRequest[2][14:]
			else:
				parsedRequest[2] = "http://" + parsedRequest[2]
			for key in self.Dic.keys():
				if key == parsedRequest[2]:
					repetido = 1
				htmlBody = htmlBody + '<p><a href="' + key + '">' + key + '</a> -- <a href="' + key + '">' + self.Dic[key] + '</a></p>'
			if repetido == 0:
				self.Dic[parsedRequest[2]] = "localhost:1234/" + str(self.Index)
				self.Index = self.Index + 1
				htmlBody = htmlBody + '<p><a href="' + parsedRequest[2] + '">' + parsedRequest[2] + '</a> -- <a href="' + parsedRequest[2] + '">' + self.Dic[parsedRequest[2]] + '</a></p>'
				htmlBody = "<h1>Nueva URL acortada y agregada. Introduce otra si quieres</h1>" + self.Form + htmlBody
			else:
				htmlBody = "<h1>URL almacenada previamente. Introduce otra si quieres</h1>" + self.Form + htmlBody
		return("200 OK", "<html><body>" + htmlBody + "</html></body>")

if __name__ == "__main__":
	testAvortadorApp = AcortadorApp("localhost", 1234)
