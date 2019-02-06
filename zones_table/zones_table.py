import pandas as pd

P_NodesXLSX = "Catalogo_NodosP_Sistema_Electrico_Nacional_v2018_12_19.xlsx"
P_NodesDF = pd.read_excel(P_NodesXLSX, header=1)
P_NodesDF = P_NodesDF.rename(columns={
                                      "CLAVE":"CLAVE NODO P",
                                      "NOMBRE":"NOMBRE NODO P",
                                      "DIRECTAMENTE MODELADA":"TIPO DE CARGA DIRECTAMENTE MODELADA",
                                      "INDIRECTAMENTE MODELADA":"TIPO DE CARGA INDIRECTAMENTE MODELADA",
                                      "DIRECTAMENTE MODELADA.1":"TIPO DE GENERACION DIRECTAMENTE MODELADA",
                                      "INDIRECTAMENTE MODELADA.1":"TIPO DE GENERACION INDIRECTAMENTE MODELADA",
                                     })
P_NodesDF.to_csv('zones_table')