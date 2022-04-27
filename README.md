# 🃏 TCG_Project 🃏
Upload an image and generate a random trading card including a name, title, special attack, and stats.

## Technologies

Written in Python, Utilizing Flask & Jinja II

Flask / Jinja II
- Used for routing and communication between frontend and backend

Selenium
- Used to webscrape randomly generated names, titles, and moves from [fantasynamegenerator.com](https://www.fantasynamegenerators.com/)

Pillow
- Used to resize image appropriately in order to display it correctly in the trading card frame

Safesearch API
- Implemented to determine if user uploaded content was inapropriate

MySQL
- Utilized in storing user and card data


## To-Do
- Implement Async jobs to prevent loading screen lockdown
- Utilze Pillow to generate image files instead of showing cards via CSS
- Design Trading card market for trading and selling cards
