# School_Recommendation_System

This is for 95888 Project

Project By: Yushi Feng, Xin Zhou, Bobby Yang

Abstract

With cutting-edge technologies, such as AI and ChatGPT, that can reshape the future job
market, global students seek to transfer their majors to the discipline of Computer Science (CS).
Tuition, budget, and rankings are essential for an international student to choose a school. Thus,
the North American computer science school recommendation system is designed to help
students recommend CS schools within their budget. The application is written in the Python
language. It has a graphical user interface (GUI) using the Tkinter library to enable user inputs
and visualize resulting school lists. The back end is responsible for data queries and scraping
through the BeautifulSoup and Requests libraries and data analysis through the Numpy and
Pandas libraries. When the user inputs the budget, country, and ranking type, the application
can automatically transfer the budget into dollars through currency. API and web scrape the
ranking website. Using the budget as a limiting factor, the application can first match the
schools whose tuitions are within the budget limit. Then, further filters can be made to the
matched schools by the web-scraped school ranking list. Students can then make connections
between their budgets and target schools promptly by using this tool.

Data Sources: 
Currency Exchange Rate API: https://www.amdoren.com/api/currency.php?api_key={api_key}&from={cur}&to=USD&amount={budget}
University Rankings Data Table: https://drafty.cs.brown.edu/csopenrankings/
