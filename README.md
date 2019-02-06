# CENACE_Prices Analysis
​
## Authors: Jiménez-Martínez, Mariana; Reyes-Ortiz, Marco Antonio.
​
​
# Retrieval and overview of Locational Marginal Price in Mexico’s short-term energy market in 2018
​
## The Wholesale Electricity Market
​
On January 27, 2016 the Mexican Deparment of Energy (Secretaría de Energía) initialized the new Wholesale Electricity Market, which aimed to allow private companies to enter the country's electrical network to supply and compete against the government-owned *Comisión Federal de Electricidad* (CFE), which had been the dominant supplier before that time. By introducing an offer-and-demand model, companies would now have different options to purchase energy at more convenient prices.
​
The *Centro Nacional de Control de Energía* (CENACE) was designated as the government entity in charge of operating the Wholesale Electricity Market. This market has five major components, among which stands the **short-term market**. This work will be centered on the performance of this component during the year 2018.
​
## Mexico's national electricity system
​
Mexico is composed of three independent systems:
​
* **BCA** which is interconnected with California, and trades energy with CAISO’s market.
* **BCS** which is completely isolated and works like an energy island.
* **SIN** which is interconnected with the US, Belize and Guatemala.
​
![Mexico's Electricity System](/images/mexico_electricity_system.png)
​
Each of this systems is composed of charge zones and each zone itself contains electricity nodes, which are the base units to model the physical injection or retrieval of electricity as well as the points where a Local Marginal Price (LMP) is established.
​
* **BCA** is composed of 4 charge zones and 101 electricity nodes. 
* **BCS** is composed of 3 charge zones and 28 electricity nodes. 
* **SIN** is composed of 101 charge zones and 2118 electricity nodes. 
​
## Stakeholders in the Wholesale Electricity Market
​
A few examples of players who have a proven interest in the perforance of the WEM are: 
​
* Electricity generators
* Basic suppliers
* Qualified users [>1MW]
* Qualified suppliers
* Traders
​
## Key questions and findings 
​
Before retrieveing any data, the following key questions were placed in order to conduct a relevant research. The key findings are presented after each question.
​
### 1. How did LMPs perform during 2018 in the three independent systems?
​
* BCS load zones have the most expensive LMPs on average; energy prices are mostly responsible of this outcome as they are significantly higher than BCA and SIN [Q1].
​
* BCA have the cheapest marginal LMPs, except in July and August when energy, congestion and loss components rise significantly.
​
### 2. How did zonal LMPs fluctuate during the day? Were there any seasonal trends?
​
* LMPs tend to rise from 08:00 – 22:00 hours; this is mostly driven by energy costs behavior and is more evident in BCS load zones.
​
* Hotter months of the year present higher LMPs in all systems; an expected outcome as higher temperatures are linked to higher demand and lower hydropower availability.  
​
### 3. Which locational components had stronger influence on zonal LMPs?
​
* Congestion costs have a wider cost range than losses (≈x5);  but finding average costs equal to zero is much more common in congestion than losses components.
​
* Congestion costs are more significant for SIN’s load zones than peninsular systems where they are most of the time zero.
​
* Locational components vary more in SIN’s load zones that in BCA and BCS; which is expected given this system’s geographical extension. 
​
### 4. How did prices bid in the day-ahead market vary from those in real time?
​
* Most of the time, MDA LMPs are lower than in MTR; but when the opposite case happens the differences are more significant.
​
### 5. How many hours per year were MDA prices higher than MTR per load zone?
​
* BCS was the system where it happened more often (>6500 hours), whereas BCA was the one with the least occurrences (<5200 hours).
​
* Given the number of load zones in SIN, there is a higher degree of variation across these regions. However, it was observed that northern regions tend to have the higher frequencies (>5000 hours) while load zones in the Yucatan Peninsula have the lowest (>4300 hours). 
​
# Data Analysis Methodology
​
1. First, the **NodosP** catalogue (v2019 01 16) was retrieved from the [official CENACE website](https://www.cenace.gob.mx/paginas/publicas/mercadooperacion/nodosp.aspx) as a *.xlsx* file. A Python script was written to retrieve the following columns from the spreadsheet (using Pandas) and generate a *.csv* file named **"zones_table.csv"**:
​
    * **CLAVE**
    * **NOMBRE**
    * **(CARGA) DIRECTAMENTE MODELADA:"TIPO DE CARGA DIRECTAMENTE MODELADA.**
    * **(CARGA) INDIRECTAMENTE MODELADA":"TIPO DE CARGA INDIRECTAMENTE MODELADA.**
    * **(GENERACION) DIRECTAMENTE MODELADA.1":"TIPO DE GENERACION DIRECTAMENTE MODELADA.**
    * **(GENERACION) INDIRECTAMENTE MODELADA.1":"TIPO DE GENERACION INDIRECTAMENTE MODELADA.**
 <br><br>
2. A second Python script named "create_master_tables.py" was written in order to retrieve data from [CENACE's API](https://www.cenace.gob.mx/DocsMEM/Manual%20para%20Uso%20SW-PEND%202018%2003%2001%20v1.pdf) using the *Pandas* and *requests* libraries. Two tables were built from the data retrieved:
​
    * **Master_Table_MDA** for the day-ahead component of the short-term market.
    * **Master_Table_MTR** for the real-time component of the short-term market.
<br><br>
  Both tables contain the following columns:
<br><br>
    * **SISTEMA**
    * **ZONA**
    * **FECHA**
    * **HORA**
    * **PRECIO MDA / MTR**
    * **PRECIO ENERGIA MDA / MTR**
    * **PRECIO PERDIDA MDA / MTR**
    * **PRECIO CONGESTION MDA / MTR**
<br><br>
  Each table contains nearly 1M rows due to the fact that for each zone in every system, data for every hour of the year 2018 is retrieved.
<br><br>
3. Two separate analysis were conducted to analyze the retrieved data to answer the key questions. Both of them use the *Pandas*, *Matplotlib* and *Numpy* libraries to manipulate, analyze and visualize data.
​
    * **Analysis_MJM.ipynb** analyzes the congestion, energy and loss components of the grand energy price and plots the data along the year in order to find geographic or temporal trends.
    * **MReyes_A1.ipynb** analyzes the frequencies of the MTR-MDA price different being positive or negative along the year. A positive price difference implies a profit for the company selling energy whereas a negative price difference implies a loss. The maximum and minimum daily prices for each zone are also computed in order to look for observable patterns along the year.
