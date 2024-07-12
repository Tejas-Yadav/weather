import tkinter as tk
import requests

from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as ttk

# Get weather (API)
def get_weather(city):
    API_key = "f079825b2495a71c96e74217bb488a39"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None

    # Parse the response JSON to get weather info
    weather = res.json()
    icon_id = weather['weather'][0]['icon']
    temp = weather['main']['temp'] - 273.15
    feels = weather['main']['feels_like'] - 273.15
    description = weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Icon URL and return weather info
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temp, feels, description, city, country)

# Search
def search():
    city = city_entry.get()
    result = get_weather(city)
    if result is None:
        return
    icon_url, temp, feels, description, city, country = result
    location_label.configure(text=f"{city}, {country}")

    # Getting weather icon image from URL
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temp and other labels
    temp_label.configure(text=f"Temperature: {temp:.2f}°C")
    feels_label.configure(text=f"Feels Like: {feels:.2f}°C")
    des_label.configure(text=f"Description: {description}")

root = ttk.Window(themename="morph")
root.title("Weather")
root.geometry("400x400")

# Entry
city_entry = tk.Entry(root, font="Helvetica")
city_entry.pack(pady=10)

# Button
search_button = ttk.Button(root, text="Search", command=search, bootstyle="warning")
search_button.pack(pady=10)

# Label
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Icon
icon_label = tk.Label(root)
icon_label.pack()

# Temperature
temp_label = tk.Label(root, font="Helvetica, 15")
temp_label.pack()

# Feels Like
feels_label = tk.Label(root, font="Helvetica, 15")
feels_label.pack()

# Description
des_label = tk.Label(root, font="Helvetica, 13")
des_label.pack()

root.mainloop()