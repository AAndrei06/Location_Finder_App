import geocoder as ip_finder
import folium
import webbrowser
import requests
import tkinter
from phonenumbers import timezone,carrier,geocoder,parse

error = False

def search_phone_number():

	try:
		number_from_entry = nr_box.get()
		phone = parse(number_from_entry)
		time = timezone.time_zones_for_number(phone)
		car = carrier.name_for_number(phone,"ro")
		region = geocoder.description_for_number(phone,"ro")
		phrase = str(phone)
		firstpart, secondpart = phrase[:len(phrase)//2], phrase[len(phrase)//2:]
		country_code = ""
		national_number = ""

		for letter in firstpart:
			if letter in "0123456789":
				country_code = country_code + str(letter)

		for letter in secondpart:
			if letter in "0123456789":
				national_number = national_number + str(letter)
	except:
		informations_tel.configure(text = "A aparut o eroare,\nincearca sa  pui \'+\' \nin fata numarului de telefon")

	informations_tel.configure(text = "Codul Tarii: +" + str(country_code) + "\n"+
															"Numar National: " + str(national_number) + "\n"+
															"Fus Orar: "+str(time[0])+"\n"+
															"Purtator: "+str(car)+"\n"+
															"Regiune: "+str(region)+"\n")

def open_map():
	webbrowser.open_new("map.html")

def get_ip_adrress_and_search():
	ip = ip_box.get()
	location = ip_finder.ip(ip)
	myAddress = location.latlng
	my_map1 = folium.Map(location = myAddress,zoom_start = 12)
	folium.CircleMarker(location = myAddress,radius = 50,popup = "Location").add_to(my_map1)
	my_map1.save("map.html")

	try:
		url = f'https://ip-api.co/{ip}/json/'
		response = requests.get(url)
		country = response.json()['country_name']
		city = response.json()['city']
		timezone = response.json()['timezone']
		latitude = response.json()['latitude']
		longitude = response.json()['longitude']
		currency = response.json()['currency_name']
		region = response.json()['region']
		country_population = response.json()['country_population']
		languages = response.json()['languages']
		ip_address_location = response.json()['ip']
		informations.configure(text = "Oraș: "+str(city)+"\n"+
										"Țara: "+str(country)+"\n"+
										"Fus Orar: "+str(timezone)+"\n"+
										"Latitudine: "+str(latitude)+"\n"+
										"Longitudine: "+str(longitude)+"\n"+
										"Valuta: "+str(currency)+"\n"+
										"Regiunea: "+str(region)+"\n"+
										"Populatia Tarii: "+str(country_population)+"\n"+
										"Limbi: "+str(languages)+"\n"+
										"IP: "+str(ip_address_location)+"\n")

	except:
		url = f'http://ip-api.com/json/{ip}'
		response = requests.get(url)
		country = response.json()['country']
		city = response.json()['city']
		timezone = response.json()['timezone']
		latitude = response.json()['lat']
		longitude = response.json()['lon']
		region = response.json()['region']
		informations.configure(text = "Oraș: "+str(city)+"\n"+
										"Țara: "+str(country)+"\n"+
										"Fus Orar: "+str(timezone)+"\n"+
										"Latitudine: "+str(latitude)+"\n"+
										"Longitudine: "+str(longitude)+"\n"+
										"Regiunea: "+str(region)+"\n")

	open_map()


window = tkinter.Tk()
color_bg_color = "#252525"
window.geometry('700x550')
window.title('Location Finder')
window.resizable(False,False)
window.configure(bg = "#252525")
try:
	img = tkinter.Image("photo",file = "location.png")
	window.iconphoto(True,img)
except:
	error = True

enter = tkinter.Label(master = window,text = "Introdu adresa IP:",font = ("Arial",16,"bold"),bg = color_bg_color,fg = "#C3C3C3")
enter.place(x=30,y=21)

ip_box = tkinter.Entry(master = window,fg = "black",width = 25,font = ("Arial",18,"bold"))
ip_box.place(x = 220,y = 20)

submit_ip = tkinter.Button(master = window,width = 8,text = "Caută  IP",font = ("Arial",12,"bold"),command = get_ip_adrress_and_search,bg = "#0C89E0")
submit_ip.place(x = 560,y = 20)

enter_tel = tkinter.Label(master = window,text = "Introdu numărul tel:",font = ("Arial",16,"bold"),bg = color_bg_color,fg = "#C3C3C3")
enter_tel.place(x = 8,y = 65)

nr_box = tkinter.Entry(master = window,fg = "black",width = 25,font = ("Arial",18,"bold"))
nr_box.place(x = 220,y = 63)

submit_nr = tkinter.Button(master = window,width = 8,text = "Caută tel",font = ("Arial",12,"bold"),command = search_phone_number,bg = "#0C89E0")
submit_nr.place(x = 560,y = 63)

location_word = tkinter.Label(master = window,width = 12,text = "Locația IP:",font = ("consolas",17,"bold"),bg = color_bg_color,fg = "#C3C3C3")
location_word.place(x = 40,y = 125)

tel_word = tkinter.Label(master = window,width = 12,text = "Locația tel:",font = ("consolas",17,"bold"),bg = color_bg_color,fg = "#C3C3C3")
tel_word.place(x = 480,y = 125)

info_frame = tkinter.Frame(master = window,width = 680,height = 340)

informations = tkinter.Label(master = info_frame,font = ("consolas",14,"bold"),text = "")
informations.place(x = 30,y = 10)

informations_tel =tkinter.Label(master = info_frame,font = ("consolas",14,"bold"),text = "")
informations_tel.place(x = 380,y = 10)

info_frame.place(x = 10,y = 160)
copyright = tkinter.Label(master = window,bg = color_bg_color,fg = "white",font = ("consolas",10,"bold"),text = "Copyright © 2022 Andrei's Software-All Rights Reserved \nCEO - Arseni Andrei ")
copyright.place(x = 160,y = 515)

window.mainloop()
