from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

pharmacies = []
clients = []
workers = []

class Pharmacy:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        try:
            latitude = float(soup.select_one(".latitude").text.replace(",", "."))
            longitude = float(soup.select_one(".longitude").text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [0.0, 0.0]

class Client:
    def __init__(self, name, service, location1, location2):
        self.name = name
        self.service = service
        self.location1 = location1
        self.location2 = location2
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.location2}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        try:
            latitude = float(soup.select_one(".latitude").text.replace(",", "."))
            longitude = float(soup.select_one(".longitude").text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [0.0, 0.0]

class Worker:
    def __init__(self, name, service, location):
        self.name = name
        self.service = service
        self.location = location
        self.coordinates = self.get_coordinates()

    def get_coordinates(self):
        url = f"https://pl.wikipedia.org/wiki/{self.location}"
        response = requests.get(url).text
        soup = BeautifulSoup(response, "html.parser")
        try:
            latitude = float(soup.select_one(".latitude").text.replace(",", "."))
            longitude = float(soup.select_one(".longitude").text.replace(",", "."))
            return [latitude, longitude]
        except:
            return [0.0, 0.0]

def dodaj_pharmacy():
    name = entry_name.get()
    location = entry_location.get()
    pharmacy = Pharmacy(name, location)
    pharmacies.append(pharmacy)
    listbox_lista_obiektow.insert(END, f"{pharmacy.name} ({pharmacy.location})")
    map_widget.set_marker(*pharmacy.coordinates, text=pharmacy.name)

def usun_pharmacy():
    index = listbox_lista_obiektow.curselection()
    if index:
        del pharmacies[index[0]]
        listbox_lista_obiektow.delete(index)

def dodaj_worker():
    name = entry_name.get()
    service = entry_posts.get()
    location = entry_location.get()
    worker = Worker(name, service, location)
    workers.append(worker)
    listbox_lista_obiektow_klient.insert(END, f"{worker.name} ({worker.location})")
    map_widget.set_marker(*worker.coordinates, text=worker.name)

def usun_worker():
    index = listbox_lista_obiektow_klient.curselection()
    if index:
        del workers[index[0]]
        listbox_lista_obiektow_klient.delete(index)

def dodaj_client():
    name = entry_name.get()
    service = entry_posts.get()
    location1 = entry_location.get()
    location2 = entry_location.get()  # zakładamy, że podano tę samą lokalizację
    client = Client(name, service, location1, location2)
    clients.append(client)
    listbox_lista_obiektow_klient_2.insert(END, f"{client.name} ({client.location2})")
    map_widget.set_marker(*client.coordinates, text=client.name)

def usun_client():
    index = listbox_lista_obiektow_klient_2.curselection()
    if index:
        del clients[index[0]]
        listbox_lista_obiektow_klient_2.delete(index)

root = Tk()
root.geometry("1200x720")
root.title("Projekt pop pf")

ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, rowspan=2, sticky=N)
ramka_formularz.grid(row=0, column=1, sticky=N)
ramka_szczegoly_obiektow.grid(row=1, column=1, sticky=N)
ramka_mapa.grid(row=2, column=0, columnspan=2)

# lista placówek
Label(ramka_lista_obiektow, text="Placówki").grid(row=0, column=0, columnspan=2)
listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=2)
Button(ramka_lista_obiektow, text='Dodaj', command=dodaj_pharmacy).grid(row=2, column=0)
Button(ramka_lista_obiektow, text='Usuń', command=usun_pharmacy).grid(row=2, column=1)

# lista pracowników
Label(ramka_lista_obiektow, text="Pracownicy").grid(row=3, column=0, columnspan=2)
listbox_lista_obiektow_klient = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow_klient.grid(row=4, column=0, columnspan=2)
Button(ramka_lista_obiektow, text='Dodaj', command=dodaj_worker).grid(row=5, column=0)
Button(ramka_lista_obiektow, text='Usuń', command=usun_worker).grid(row=5, column=1)

# lista klientów
Label(ramka_lista_obiektow, text="Klienci").grid(row=6, column=0, columnspan=2)
listbox_lista_obiektow_klient_2 = Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow_klient_2.grid(row=7, column=0, columnspan=2)
Button(ramka_lista_obiektow, text='Dodaj', command=dodaj_client).grid(row=8, column=0)
Button(ramka_lista_obiektow, text='Usuń', command=usun_client).grid(row=8, column=1)

# formularz
Label(ramka_formularz, text="Formularz").grid(row=0, column=0, columnspan=2)
Label(ramka_formularz, text="Imię:").grid(row=1, column=0, sticky=W)
Label(ramka_formularz, text="Nazwisko:").grid(row=2, column=0, sticky=W)
Label(ramka_formularz, text="Miejscowość:").grid(row=3, column=0, sticky=W)
Label(ramka_formularz, text="Usługa:").grid(row=4, column=0, sticky=W)

entry_name = Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=3, column=1)
entry_posts = Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)

# szczegóły obiektów
Label(ramka_szczegoly_obiektow, text="Szczegóły obiektu: ...").grid(row=0, column=0)

# mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

root.mainloop()