import pandas as pd
import numpy as np
import requests
import json
import os

master_table_path = "zones_table/zones_table"                               # Set origin file path

P_NodesDF = pd.read_csv(master_table_path)                                  # Create Data Frame
P_NodesDF = P_NodesDF.drop(labels="Unnamed: 0", axis=1)                     # Drop duplicate number column
P_NodesDF = P_NodesDF.loc[P_NodesDF["ZONA DE CARGA"] != "No Aplica", :]     # Drop rows with unassigned ZONA DE CARGA

# Count unique ZONA DE CARGA for each SISTEMA
Zonas_CargaDF = P_NodesDF.loc[:, ["SISTEMA", "ZONA DE CARGA"]]
Zonas_CargaDF = Zonas_CargaDF.drop_duplicates()
Zonas_CargaDF_Count = Zonas_CargaDF.groupby("SISTEMA").count()

# Count Unique NODO P for each SISTEMA
NodosDF = P_NodesDF.loc[:, ["SISTEMA", "NOMBRE NODO P"]]
NodosDF = NodosDF.drop_duplicates()
NodosDF_Count = NodosDF.groupby("SISTEMA").count()

# Retrieve names for ZONA and save to lists
BCA_ZonasLS = P_NodesDF.loc[P_NodesDF["SISTEMA"] == "BCA", "ZONA DE CARGA"]
BCA_ZonasLS = BCA_ZonasLS.drop_duplicates()
BCA_ZonasLS = BCA_ZonasLS.tolist()

BCS_ZonasLS = P_NodesDF.loc[P_NodesDF["SISTEMA"] == "BCS", "ZONA DE CARGA"]
BCS_ZonasLS = BCS_ZonasLS.drop_duplicates()
BCS_ZonasLS = BCS_ZonasLS.tolist()

SIN_ZonasLS = P_NodesDF.loc[P_NodesDF["SISTEMA"] == "SIN", "ZONA DE CARGA"]
SIN_ZonasLS = SIN_ZonasLS.drop_duplicates()
SIN_ZonasLS = SIN_ZonasLS.tolist()

# Create lists to build API Requests
year = "2018"
Calendar_LS = []

for month in range(1,13):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        for day in range(1,32):
            if day < 10 and month < 10:
                date = f"{year}/0{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day < 10 and month >= 10:
                date = f"{year}/{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month < 10:
                date = f"{year}/0{str(month)}/{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month >= 10:
                date = f"{year}/{str(month)}/{str(day)}"
                Calendar_LS.append(date)
    elif month in [4, 6, 9, 11]:
        for day in range(1,31):
            if day < 10 and month < 10:
                date = f"{year}/0{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day < 10 and month >= 10:
                date = f"{year}/{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month < 10:
                date = f"{year}/0{str(month)}/{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month >= 10:
                date = f"{year}/{str(month)}/{str(day)}"
                Calendar_LS.append(date)       
    else:
        for day in range(1,29):
            if day < 10 and month < 10:
                date = f"{year}/0{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day < 10 and month >= 10:
                date = f"{year}/{str(month)}/0{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month < 10:
                date = f"{year}/0{str(month)}/{str(day)}"
                Calendar_LS.append(date)
            elif day >= 10 and month >= 10:
                date = f"{year}/{str(month)}/{str(day)}"
                Calendar_LS.append(date)

# Create dictionary for SISTEMA-ZONAS
Sistemas_dict = {"BCA":BCA_ZonasLS, "BCS":BCS_ZonasLS, "SIN":SIN_ZonasLS}
LS_SIN_ZonasLS = []
Zonas_aux = []
flag_sist = 0
while flag_sist < len(Sistemas_dict["SIN"]):
    if flag_sist in [9, 19, 29, 39, 49, 59, 69, 79, 89, 99]:
        zn = Sistemas_dict["SIN"][flag_sist]
        Zonas_aux.append(zn)
        LS_SIN_ZonasLS.append(Zonas_aux)
        Zonas_aux = []
        flag_sist += 1
    else:
        zn = Sistemas_dict["SIN"][flag_sist]
        Zonas_aux.append(zn)
        flag_sist += 1
    if flag_sist == 100:
        Zonas_aux = []   
        zn = Sistemas_dict["SIN"][flag_sist]
        Zonas_aux.append(zn)
        LS_SIN_ZonasLS.append(Zonas_aux)
        break
Sistemas_dict["SIN"] = LS_SIN_ZonasLS

#Create Lists for API Requests - MDA               
Sistemas_MDA = []
Zonas_MDA = []
Fechas_MDA = []
Horas_MDA = []
pz_MDA = []
pz_ene_MDA = []
pz_per_MDA = []
pz_cng_MDA = []

# Make API requests - MDA
# Sistemas BC y BCS 
TEST = 0

for SISTEMA in Sistemas_dict:
    
    if SISTEMA != "SIN":      
        
        ZONAS= Sistemas_dict[SISTEMA]
        ZTEXT = ','.join(ZONAS)
           
        n = 0
        
        while n < 365:
            if n == 364:
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n]
                THoras = 24
            else:
                
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n+6]
                THoras = 168
            
            url_new = f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{SISTEMA}/MDA/{ZTEXT}/{DUNO}/{DDOS}/JSON"
            url_new= url_new.replace(" ","-")
            response = requests.get(url_new)
            response_JSON = response.json()
            
            if response_JSON["status"] == "OK":
                
                for Z in range(len(ZONAS)):
                    
                    for HORA in range(THoras):
                        
                        Sistemas_MDA.append(response_JSON["sistema"])
                        Zonas_MDA.append(response_JSON["Resultados"][Z]["zona_carga"])
                        try:
                            Fechas_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["fecha"])
                        except: 
                            Fechas_MDA.append("NULL")
                        try: 
                            Horas_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["hora"])
                        except: 
                            Horas_MDA.append("NULL")
                        try:
                            pz_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz"])
                        except:
                            pz_MDA.append("NULL")
                        try:
                            pz_ene_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_ene"])
                        except:
                            pz_ene_MDA.append("NULL")
                        try:
                            pz_per_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_per"])
                        except:
                            pz_per_MDA.append("NULL")
                        try:
                            pz_cng_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_cng"])
                        except:
                            pz_cng_MDA.append("NULL")
            n= n + 7
            TEST= TEST+1
            print(f"Processing: MDA | {SISTEMA} |{ZONAS} | TEST:{TEST}  ")

print("----------------------------------------------------------------------------")
print(                  "Finished Retrieving data for MDA-BC, MDA-BS")
print("----------------------------------------------------------------------------")

#Make API Requests - MDA
#Sistema Interconectado Nacional (SIN) 

TEST = 0

SISTEMA = "SIN"
    
for GRUPO in range(len(Sistemas_dict[SISTEMA])):      
        
    ZONAS= Sistemas_dict["SIN"][GRUPO]
    ZTEXT = ','.join(ZONAS)
           
    n = 0
        
    while n < 365:
        if n == 364:
            DUNO = Calendar_LS[n]
            DDOS = Calendar_LS[n]
            THoras = 24
        else:
                
            DUNO = Calendar_LS[n]
            DDOS = Calendar_LS[n+6]
            THoras = 168
            
        url_new = f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{SISTEMA}/MDA/{ZTEXT}/{DUNO}/{DDOS}/JSON"
        url_new= url_new.replace(" ","-")
        response = requests.get(url_new)
        response_JSON = response.json()
            
        if response_JSON["status"] == "OK":
                
            for Z in range(len(ZONAS)):
                    
                for HORA in range(THoras):
                        
                    Sistemas_MDA.append(response_JSON["sistema"])
                    Zonas_MDA.append(response_JSON["Resultados"][Z]["zona_carga"])
                    try:
                        Fechas_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["fecha"])
                    except: 
                        Fechas_MDA.append("NULL")
                    try: 
                        Horas_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["hora"])
                    except: 
                        Horas_MDA.append("NULL")
                    try:
                        pz_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz"])
                    except:
                        pz_MDA.append("NULL")
                    try:
                        pz_ene_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_ene"])
                    except:
                        pz_ene_MDA.append("NULL")
                    try:
                        pz_per_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_per"])
                    except:
                        pz_per_MDA.append("NULL")
                    try:
                        pz_cng_MDA.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_cng"])
                    except:
                        pz_cng_MDA.append("NULL")
        n= n + 7
        TEST= TEST+1
        print(f"Processing: MDA | {SISTEMA} |{ZONAS} | TEST:{TEST} ")

print("----------------------------------------------------------------------------")
print(                  "Finished Retrieving data for MDA-SIN")
print("----------------------------------------------------------------------------")

#Dataframe for MDA prices
MT_DF_MDA = pd.DataFrame({
    "SISTEMA":Sistemas_MDA,
    "ZONA":Zonas_MDA,
    "FECHA":Fechas_MDA,
    "HORA":Horas_MDA,
    "PRECIO MDA":pz_MDA,
    "PRECIO ENERGIA MDA":pz_ene_MDA,
    "PRECIO PERDIDA MDA":pz_per_MDA,
    "PRECIO CONGESTION MDA":pz_cng_MDA,
})
MT_DF_MDA= MT_DF_MDA.sort_values(["SISTEMA","ZONA","FECHA"], ascending=[True, True,True])
MT_DF_MDA = MT_DF_MDA.set_index("ZONA")
path_Master_Table_MDA = os.path.join("MDA_table" + os.sep, "Master_Table_MDA.csv")
MT_DF_MDA.to_csv(path_Master_Table_MDA)     # Save CSV file

print("----------------------------------------------------------------------------")
print(               "Saved data for MDA as Master_Table_MDA.csv")
print("----------------------------------------------------------------------------")

#Create Lists for API Requests - MTR               
Sistemas_MTR = []
Zonas_MTR = []
Fechas_MTR = []
Horas_MTR = []
pz_MTR = []
pz_ene_MTR = []
pz_per_MTR = []
pz_cng_MTR = []

# Make API requests - MTR
#Sistemas BC y BCS 
TEST = 0

for SISTEMA in Sistemas_dict:
    
    if SISTEMA != "SIN":      
        
        ZONAS= Sistemas_dict[SISTEMA]
        ZTEXT = ','.join(ZONAS)
           
        n = 0
        
        while n < 365:
            if n == 364:
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n]
                THoras = 24
            else:
                
                DUNO = Calendar_LS[n]
                DDOS = Calendar_LS[n+6]
                THoras = 168
            
            url_new = f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{SISTEMA}/MTR/{ZTEXT}/{DUNO}/{DDOS}/JSON"
            url_new= url_new.replace(" ","-")
            response = requests.get(url_new)
            response_JSON = response.json()
            
            if response_JSON["status"] == "OK":
                
                for Z in range(len(ZONAS)):
                    
                    for HORA in range(THoras):
                        
                        Sistemas_MTR.append(response_JSON["sistema"])
                        Zonas_MTR.append(response_JSON["Resultados"][Z]["zona_carga"])
                        try:
                            Fechas_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["fecha"])
                        except: 
                            Fechas_MTR.append("NULL")
                        try: 
                            Horas_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["hora"])
                        except: 
                            Horas_MTR.append("NULL")
                        try:
                            pz_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz"])
                        except:
                            pz_MTR.append("NULL")
                        try:
                            pz_ene_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_ene"])
                        except:
                            pz_ene_MTR.append("NULL")
                        try:
                            pz_per_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_per"])
                        except:
                            pz_per_MTR.append("NULL")
                        try:
                            pz_cng_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_cng"])
                        except:
                            pz_cng_MTR.append("NULL")
            n= n + 7
            TEST= TEST+1
            print(f"Processing: MTR | {SISTEMA} |{ZONAS} | TEST:{TEST} ")

print("----------------------------------------------------------------------------")
print(               "Finished Retrieving data for MTR-BC, MTR-BCS")
print("----------------------------------------------------------------------------")

#Make API Requests - MTR
#Sistema Interconectado Nacional (SIN) 
TEST = 0

SISTEMA = "SIN"
    
for GRUPO in range(len(Sistemas_dict[SISTEMA])):      
        
    ZONAS= Sistemas_dict["SIN"][GRUPO]
    ZTEXT = ','.join(ZONAS)
           
    n = 0
        
    while n < 365:
        if n == 364:
            DUNO = Calendar_LS[n]
            DDOS = Calendar_LS[n]
            THoras = 24
        else:
                
            DUNO = Calendar_LS[n]
            DDOS = Calendar_LS[n+6]
            THoras = 168
            
        url_new = f"https://ws01.cenace.gob.mx:8082/SWPEND/SIM/{SISTEMA}/MTR/{ZTEXT}/{DUNO}/{DDOS}/JSON"
        url_new= url_new.replace(" ","-")
        response = requests.get(url_new)
        response_JSON = response.json()
            
        if response_JSON["status"] == "OK":
                
            for Z in range(len(ZONAS)):
                    
                for HORA in range(THoras):
                        
                    Sistemas_MTR.append(response_JSON["sistema"])
                    Zonas_MTR.append(response_JSON["Resultados"][Z]["zona_carga"])
                    try:
                        Fechas_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["fecha"])
                    except: 
                        Fechas_MTR.append("NULL")
                    try: 
                        Horas_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["hora"])
                    except: 
                        Horas_MTR.append("NULL")
                    try:
                        pz_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz"])
                    except:
                        pz_MTR.append("NULL")
                    try:
                        pz_ene_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_ene"])
                    except:
                        pz_ene_MTR.append("NULL")
                    try:
                        pz_per_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_per"])
                    except:
                        pz_per_MTR.append("NULL")
                    try:
                        pz_cng_MTR.append(response_JSON["Resultados"][Z]["Valores"][HORA]["pz_cng"])
                    except:
                        pz_cng_MTR.append("NULL")
        n= n + 7
        TEST= TEST+1
        print(f"Processing: {SISTEMA} |{ZONAS} | TEST:{TEST} ")

print("----------------------------------------------------------------------------")
print(                   "Finished Retrieving data for MTR-SIN")
print("----------------------------------------------------------------------------")
#Dataframe for MTR prices
MT_DF_MTR = pd.DataFrame({
    "SISTEMA":Sistemas_MTR,
    "ZONA":Zonas_MTR,
    "FECHA":Fechas_MTR,
    "HORA":Horas_MTR,
    "PRECIO MTR":pz_MTR,
    "PRECIO ENERGIA MTR":pz_ene_MTR,
    "PRECIO PERDIDA MTR":pz_per_MTR,
    "PRECIO CONGESTION MTR":pz_cng_MTR,
})
MT_DF_MTR= MT_DF_MTR.sort_values(["SISTEMA","ZONA","FECHA"], ascending=[True, True,True])
MT_DF_MTR = MT_DF_MTR.set_index("ZONA")
path_Master_Table_MTR = os.path.join("MTR_table" + os.sep, "Master_Table_MTR.csv")
MT_DF_MTR.to_csv(path_Master_Table_MTR)    # Save CSV File

print("----------------------------------------------------------------------------")
print(               "Saved data for MTR as Master_Table_MTR.csv")
print("----------------------------------------------------------------------------")