from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

pharmacies = []
clients = []
workers = []
markers = []

def clear_map():
    global markers
    for marker in markers:
        marker.delete()
    markers = []

def get_coordinates(place):
    url = f"https://pl.wikipedia.org/wiki/{place}"
    response = requests.get(url).text
    response_html = BeautifulSoup(response, "html.parser")
    try:
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        return [latitude, longitude]
    except IndexError:
        return [52.23, 21.0]  # fallback to Warsaw

class Pharmacy:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.coordinates = get_coordinates(location)

class Client:
    def __init__(self, name, service, location1, location2, pharmacy):
        self.name = name
        self.service = service
        self.location1 = location1
        self.location2 = location2
        self.pharmacy = pharmacy  # reference to Pharmacy object
        self.coordinates = get_coordinates(location2)

class Worker:
    def __init__(self, name, service, location, pharmacy):
        self.name = name
        self.service = service
        self.location = location
        self.pharmacy = pharmacy
        self.coordinates = get_coordinates(location)

root = Tk()
root.geometry("1200x720")
root.title("System zarzadzania siecią weterynaryjną")

frame_list = Frame(root)
frame_form = Frame(root)
frame_buttons = Frame(root)
frame_map = Frame(root)

frame_list.pack(side=LEFT, fill=Y)
frame_form.pack(side=TOP, fill=X)
frame_buttons.pack(side=TOP, fill=X)
frame_map.pack(side=BOTTOM, fill=BOTH, expand=True)

listbox_pharmacies = Listbox(frame_list, width=40)
listbox_workers = Listbox(frame_list, width=40)
listbox_clients = Listbox(frame_list, width=40)

Label(frame_list, text="Placówki").pack()
listbox_pharmacies.pack()
Label(frame_list, text="Pracownicy").pack()
listbox_workers.pack()
Label(frame_list, text="Klienci").pack()
listbox_clients.pack()


Label(frame_form, text="Nazwa placówki:").grid(row=0, column=0)
entry_pharmacy_name = Entry(frame_form)
entry_pharmacy_name.grid(row=0, column=1)

Label(frame_form, text="Lokalizacja placówki:").grid(row=1, column=0)
entry_pharmacy_location = Entry(frame_form)
entry_pharmacy_location.grid(row=1, column=1)

Label(frame_form, text="Imię pracownika:").grid(row=0, column=2)
entry_worker_name = Entry(frame_form)
entry_worker_name.grid(row=0, column=3)

Label(frame_form, text="Usługa:").grid(row=1, column=2)
entry_worker_service = Entry(frame_form)
entry_worker_service.grid(row=1, column=3)

Label(frame_form, text="Miasto pracownika:").grid(row=2, column=2)
entry_worker_location = Entry(frame_form)
entry_worker_location.grid(row=2, column=3)

Label(frame_form, text="Imię klienta:").grid(row=0, column=4)
entry_client_name = Entry(frame_form)
entry_client_name.grid(row=0, column=5)

Label(frame_form, text="Usługa klienta:").grid(row=1, column=4)
entry_client_service = Entry(frame_form)
entry_client_service.grid(row=1, column=5)

Label(frame_form, text="Lokalizacja 1:").grid(row=2, column=4)
entry_client_loc1 = Entry(frame_form)
entry_client_loc1.grid(row=2, column=5)

Label(frame_form, text="Lokalizacja 2:").grid(row=3, column=4)
entry_client_loc2 = Entry(frame_form)
entry_client_loc2.grid(row=3, column=5)

map_widget = tkintermapview.TkinterMapView(frame_map, width=1200, height=400, corner_radius=5)
map_widget.pack(fill=BOTH, expand=True)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)

def add_pharmacy():
    name = entry_pharmacy_name.get()
    location = entry_pharmacy_location.get()
    p = Pharmacy(name, location)
    pharmacies.append(p)
    listbox_pharmacies.insert(END, name)
    marker = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"Placówka: {name}")
    markers.append(marker)

def add_worker():
    name = entry_worker_name.get()
    service = entry_worker_service.get()
    location = entry_worker_location.get()
    if pharmacies:
        worker = Worker(name, service, location, pharmacies[-1])
        workers.append(worker)
        listbox_workers.insert(END, name)
        marker = map_widget.set_marker(worker.coordinates[0], worker.coordinates[1], text=f"Pracownik: {name}")
        markers.append(marker)

def add_client():
    name = entry_client_name.get()
    service = entry_client_service.get()
    loc1 = entry_client_loc1.get()
    loc2 = entry_client_loc2.get()
    if pharmacies:
        client = Client(name, service, loc1, loc2, pharmacies[-1])
        clients.append(client)
        listbox_clients.insert(END, name)
        marker = map_widget.set_marker(client.coordinates[0], client.coordinates[1], text=f"Klient: {name}")
        markers.append(marker)

def show_all_pharmacies():
    clear_map()
    for p in pharmacies:
        m = map_widget.set_marker(p.coordinates[0], p.coordinates[1], text=f"Placówka: {p.name}")
        markers.append(m)

def show_all_workers():
    clear_map()
    for w in workers:
        m = map_widget.set_marker(w.coordinates[0], w.coordinates[1], text=f"Pracownik: {w.name}")
        markers.append(m)

def show_clients_for_selected_pharmacy():
    clear_map()
    index = listbox_pharmacies.curselection()
    if index:
        selected_pharmacy = pharmacies[index[0]]
        for c in clients:
            if c.pharmacy == selected_pharmacy:
                m = map_widget.set_marker(c.coordinates[0], c.coordinates[1], text=f"Klient: {c.name}")
                markers.append(m)

def show_workers_for_selected_pharmacy():
    clear_map()
    index = listbox_pharmacies.curselection()
    if index:
        selected_pharmacy = pharmacies[index[0]]
        for w in workers:
            if w.pharmacy == selected_pharmacy:
                m = map_widget.set_marker(w.coordinates[0], w.coordinates[1], text=f"Pracownik: {w.name}")
                markers.append(m)

Button(frame_buttons, text="Dodaj Placówkę", command=add_pharmacy).pack(side=LEFT)
Button(frame_buttons, text="Dodaj Pracownika", command=add_worker).pack(side=LEFT)
Button(frame_buttons, text="Dodaj Klienta", command=add_client).pack(side=LEFT)
Button(frame_buttons, text="Mapa Placówek", command=show_all_pharmacies).pack(side=LEFT)
Button(frame_buttons, text="Mapa Pracowników", command=show_all_workers).pack(side=LEFT)
Button(frame_buttons, text="Klienci Placówki", command=show_clients_for_selected_pharmacy).pack(side=LEFT)
Button(frame_buttons, text="Pracownicy Placówki", command=show_workers_for_selected_pharmacy).pack(side=LEFT)

root.mainloop()
