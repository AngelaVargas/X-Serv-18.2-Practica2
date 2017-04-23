from django.shortcuts import render
from django.http import HttpResponse
from .models import urls
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Process(Request,resource):
	
		sequency = 0

		form = '<form action="" method="POST">'
		form += 'Introduce url para acortar: <input type="text" name="url">'
		form += '<input type="submit" value="Enviar">'
		form += '</form>'

		if Request.method == "GET":
			if resource == "":				#Estoy en el principio				
				#Ahora busco qué tengo en la base de datos para mandarlo junto con el formulario por pantalla

				list = urls.objects.all()
				Response = 'Urls acortadas en la base de datos:' + '<br>'
				for entry in list:
					Response += '<li>' + entry.longer + '   -> url_acortada = ' + str(entry.short)
					sequency= str(entry.short)

				htmlAnswer = "<html><body>" + form + "<br>" + Response + "</body></html>"

			else:									#Acabo de pinchar en el enlace de la url y he hecho un GET a esa url para que me redirija
				try:
					url_saved = urls.objects.get(longer=resource)
					htmlAnswer = "<html><body><meta http-equiv='refresh'"	+	"content='1 url="	+	url_saved + "'>"\
										+ "</p></body></html>"

				except urls.DoesNotExist: 
					url_saved = urls.objects.get(short=resource)
					htmlAnswer = "<html><body><meta http-equiv='refresh'"	+	"content='1 url="	+	url_saved.longer + "'>"\
										+ "</p></body></html>"

				except ValueError:
						htmlAnswer = "<html><body>Error: Recurso no disponible</body></html>"

		elif Request.method == "POST":
			url = Request.POST['url']
			
			if url == "":								#En el cuerpo del POST no hay url y debo devolver código de error
				returnCode = "404 Not Found"
				htmlAnswer = "<html><body>Error: Introduzca una url\n</body></html>"
				return HttpResponse(htmlAnswer)
	
			elif url.find("http") == -1:			#Si en el cuerpo hay una url SIN http, devuelve -1 como error porque no lo encuentra
				url = "http://" + url				#A la url le debo añadir la cabecera http://


			htmlAnswer = "<html><body>" + url + "</body></html>"

			try:
				#Esta url está en la base de datos
				url_saved = urls.objects.get(longer=url)					
				sequency = url_saved.short			#La url acortada, será el número de secuencia

			except:
				#Esta url no está en la base de datos
				list = urls.objects.all()
				for i in list:
					sequency= str(i.short)

				sequency = int(sequency) + 1		#Al último valor de sequency que tenía le sumo
				u = urls(longer=url, short=sequency)	#La guardo en la base de datos
				u.save()		

			
			htmlAnswer ="<html><body><a href=" + url + ">" + url + "</href><p><a href="\
							+	str(sequency)	+	">"	+	str(sequency)	+	"</href></body></html>"

		else:

			htmlAnswer = "<html><body>Error en el método</body></html>"

		return HttpResponse(htmlAnswer)

