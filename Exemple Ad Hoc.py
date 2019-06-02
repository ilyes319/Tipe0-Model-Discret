#!/usr/bin/env python3
#encoding: windows-1252

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
#On commence par créer un diagramme fondamental (Triangulaire Greenshield)

#Par exemple ici on crée un diagramme Triangulaire
#Avec la vitesse free 36 m/s (130 km/h)
#La vitesse de l'onde congestion -5 m/s (cf Treiber) donnée de test
#La densité maximale 0,2 vehicule / m en prenant l'approximation q'un vehicule
#fait 4 m plus 1 m de distance de sécuirté
#le coefiance c (homogène à une vitesse) de 17 m/s (cf Newell)

funddiag = Diagramme_Triangulaire(34,-5,0.2,17)

#Ensuite on crée un environement spatiale entre deux abscisses avec un diagramme fondamental funddiag
#Ici la route fait 1Km

MyEnv = Main(funddiag,0,1000)

#Puis on set up les densités initiales le long de la route discretisée
#Dans cette exemple la route est coupée en 3 portions tel que:
#pour 0<x<100m densité = 100 voitures par km 
#pour 100<x<300m densité = 10 voitures par km
#pour 300<x<1000m densité = 40 voitures par km

MyEnv.Dens_Ini([0,100,300,1000] ,[100*10**(-3),10*10**(-3),40*10**(-3)] )

#Puis on set up le flow entrant pour chaque temps à l'abscisse xmin
#Par exemple ici:
#pour 0<t<20 s il rentre 0.4 vehicules par seconde
#pour 20<t<40 s il rentre 0.01 vehicules par seconde
MyEnv.Up_Flow([0,20,40,50],[0.4,0.01,0.2])

#Puis on set up le flow sortant pour chaque temps à l'abscisse xmax

MyEnv.Down_Flow([0,30,35,50], [0.3,0, 0.1])

X = 1000;           #x maximal
nx = 500;           #Nombre d abscisse
T = 50;             #Durée de la simulation
nt = 500;           #Nombre de points temporels
dx=X/nx;            #Pas spatial
dt=T/nt;            #Temps spatial
xScale = np.arange(0,X,dx)    #Array pour domaine spatiale
tScale = np.arange(0,T,dt)    #Array pour le domaine temporelle

x = np.ones(np.shape(np.transpose(tScale)))*(xScale)
t = np.transpose(tScale)*(np.ones(np.shape(xscale)))

resultat = MyEnv.explicitSol(t,x)

N = resultat[1]
Index = resultat[2]

k = MyEnv.density(t,x,index)
v = v_f*(1-exp((c/v_f)*(1- (kmax*(np.power(k,-1)))))
cCO2 =  [9449, 938.4, 0.0, 467.1, 28.26, 0.0];
cCO = [593.2, 19.32, 0.0, 73.25, 2.086, 0.0] ;
cHC = [2.923, 0.1113, 0.0, 0.3476, 0.01032, 0.0] ;
cNOx = [4.336, 0.4428, 0.0, 0.3204, 0.01371, 0.0] ;
cPM = [0.2375, 0.0245, 0.0, 0.03251, 0.001325, 0.0] ;
ECO2 = cCO2(1) + cCO2(3) * v + cCO2(4) * np.power(v,2) + cCO2(5) * np.power(v,3);
ECO = cCO(1) + cCO(3) * v + cCO(4) * np.power(v,2) + cCO(5) * np.power(v,3);
EHC = cHC(1) + cHC(3) * v + cHC(4) * np.power(v,2) + cHC(5) * np.power(v,3);
ENOx = cNOx(1) + cNOx(3) * v + cNOx(4) * np.power(v,2) + cNOx(5) * np.power(v,3);
EPM = cPM(1) + cPM(3) * v + cPM(4) * np.power(v,2) + cPM(5) * np.power(v,3);


