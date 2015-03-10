#!/usr/bin/python
import webapp

class ShortApp(webapp.webApp):
	dicLongShort = {}
	dicShortLong = {}
	NextIndex = 0
	Form = '<form name="input" method="post">\nURL: <input type="text" name="URL">\n<input type="submit" value="Enviar">\n</form>'

	def parse (self, request):
		lines = request.splitlines()
		method = lines[0].split(' ')[0]
		resource = lines[0].split(' ')[1]
		if method == "GET":
			url = ""
		elif method == "POST":
			if lines[-1][0:4] == "URL=":
				url = lines[-1].split('=')[1]
			else:
				url = ""

		parsedRequest = [method, resource, url]
		return parsedRequest

	def process (self, parsedRequest):
		if parsedRequest[0] == "GET":
			if parsedRequest[1] == '/':
				httpCode = "200 OK"
				htmlBody = "<h1>Bienvenido!</h1>Introduce una URL para acortarla" + self.Form
				for key in self.dicShortLong.keys():
					htmlBody = htmlBody + '<p><a href="' + self.dicShortLong[key] + '">' + str(key) + '</a> -- <a href="' + self.dicShortLong[key] + '">' + self.dicShortLong[key] + "</a></p>"
			else:
				key = "localhost:1234" + parsedRequest[1]
				if self.dicShortLong.has_key(key):
					httpCode = "200 OK"
					htmlBody = '<a href="' + self.dicShortLong[key] + '">' + str(self.dicShortLong[key]) + "</a>"
				else:
					httpCode = "200 OK"
					htmlBody = "<h1>URL no existente</h1>"

		elif parsedRequest[0] == "POST":
			if parsedRequest[1] == '/':
				if parsedRequest[2] != None:
					parsedRequest[2] = parsedRequest[2].replace("%3A", ':')
					parsedRequest[2] = parsedRequest[2].replace("%2F", '/')
					if parsedRequest[2][0:7] == "http://":
						urlLong = "http://" + parsedRequest[2][7:]
					elif parsedRequest[2][0:8] == "https://":
						urlLong = "https://" + parsedRequest[2][8:]
					else:
						urlLong = "http://" + parsedRequest[2]
					if not self.dicLongShort.has_key(urlLong):
						urlShort = "localhost:1234/" + str(self.NextIndex)
						self.NextIndex = self.NextIndex + 1
						self.dicShortLong[urlShort] = urlLong
						self.dicLongShort[urlLong] = urlShort
						htmlBody = "<h1>Agregada una nueva URL</h1>Quieres agregar otra?" + self.Form
					else:
						htmlBody = "<h1>URL ya conocida</h1>Quiere agregar otra?" + self.Form
					httpCode = "200 OK"
					for key in self.dicShortLong.keys():
						htmlBody = htmlBody + '<p><a href="' + self.dicShortLong[key] + '">' + str(key) + '</a> -- <a href="' + self.dicShortLong[key] + '">' + self.dicShortLong[key] + "</a></p>"
				else:
					httpCode = "200 OK"
					htmlBody = "<h2>El POST recibido no es valido. Debes rellenar el formulatio</h2>"
		else:
