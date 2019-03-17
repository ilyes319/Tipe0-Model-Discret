class Diagramme_triangualaire:
    """Creation du diagramme triangualaire liant le flux � la densit�"""
    def __init__(self,Vf,w, kmax):
        self.Vf = Vf #Soit vf la vitesse maximal desir� par l'utilsateur sur cette route
        self.w= w  #vitesse de l'onde de congestion (Negative!!!)
        self.kmax = kmax #Soit kmax la densit� maximale
        self.k_c = -w*kmax/(Vf-w) ##Soit kmax la densit� maximale avant saturation
   
    def density(self,v):
        k = np.ones(v.shape)
        PossibleArea = np.bitwise_and(v>= self.w , v<= self.vf)
        k[PossibleArea] = self.k_c
        return k
    

    def flow(self,k):
        """La fonction renvoie le flux en fonction de la densit� k"""
        if k < self.Vf:
            q = k*self.Vf
        else:
            q= self.w*(k-self.kmax)
        return q

    def R(self,v):
        r= self.k_c * (self.Vf-v)
        return r
        
            
    def densities(self,v,g):
        k1 = g / (self.Vf-v)
        k2 = (self.w*self.kmax+g)/(self.w-v)
        resultat =  np.array([k1,k2])
        return resultat
        
    def speed(self,k):
        if k < self.k_c:
            v = self.Vf
                
        else:
            v = self.w
        return v
              

def Moskowitz(Diagramme_fondamental,ti,xi,weak_cond):
    
    """Calcule la fonction de Moskowitz en t,x avec les conditions faibles donnees et le diagramme fondamental"""
    t = np.array(ti)
    x = np.array(xi)
    if t.shape != x.shape:
        return "t et x sont de dimensions differentes"
    
    N = np.array(np.inf*np.ones(t.shape))   #Matrice representant les densit�s � chaque abscisse discretisee
    
    t0 = weak_cond[0]
    t1 = weak_cond[1]
    x0 = weak_cond[2]
    x1 = weak_cond[3]
    m = weak_cond[4]
    n0 = weak_cond[5]
    
    if t1 == t0:
        k1 = 0
        k2 = -m/(x1-x0)
    else:
        dens = Diagramme_fondamental.densities((x1-x0)/(t1-t0),m/(t1-t0))
        k1 = dens[1]
        k2 = dens[2]
    
    AfterBeging = t>=t0
    AfterEnd = t >= t1
    
    velObserver= (x1-x0) / (t1-t0)
    virtualV0 = N
    virtualV1 = N
    
    virtualV0[AfterBeging] = np.array( ( np.divide((x[AfterBeging]-x0),(t[AfterBeging]-t0) ) ) )
    
    virtualV1[AfterEnd] = np.array( ( np.divide( (x[AfterEnd]-x1),(t[AfterEnd]-t1) ) ) )
    
    ActionArea = np.array(np.bitwise_and( (np.minimum(virtualV0,virtualV1)) <= Diagramme_fondamental.speed(0) 
    
    , (np.maximum(virtualV0,virtualV1) >= np.array( Diagramme_fondamental.speed(Diagramme_fondamental.kmax) ) ) ) )
     
    EndArea = np.array( (np.bitwise_and( virtualV1 <= np.array(Diagramme_fondamental.speed(k1)) 
    
    , virtualV1 >= np.array( Diagramme_fondamental.speed(k2) ) ) ) )
    
    N[EndArea] = n0 + m + np.multiply( np.array( (t[EndArea]-t1) ), np.array(Diagramme_fondamental.R(virtualV1[EndArea]) ))
    
    CharacterArea = np.array( np.bitwise_and.reduce(
    
    virtualV0 >= Diagramme_fondamental.speed(k1) , 
    
    np.bitwise_or( ( virtualV0 <= Diagramme_fondamental.speed(k1) , 
    
    np.bitwise_and( virtualV0 <= velObserver , virtualV0 < Diagramme_fondamental.speed(0) ) ) ), 
    
    ( np.bitwise_not(EndArea) ) ) )
    
    UpCharacArea = np.array( np.bitwise_and(virtualV0 > velObserver , CharacterArea) )
    
    N[UpCharacArea] = n0 + (x0 - x(UpCharacArea))*k1 + (t(UpCharacArea)-t0)*Diagramme_fondamental.flow(k1)
    
    DownCharacArea = np.array( np.bitwise_and( virtualV0 <= velObserver , CharacDomain ) )
    
    N[DownCharacArea] = n0 + (x0 - x[DownCharacArea])*k2 + (t[DownCharacArea]-t0)*Diagramme_fondamental.flow(k1)
    
    BetweenArea = np.array( np.bitwise_and.reduce( ActionArea ,( np.bitwise_not(EndArea) ) , ( np.bitwise_not(CharacterArea) ) ) )
    
    N[BetweenArea] = n0 + np.multiply( (t[BetweenArea]  -t0) , np.array(Diagramme_fondamental.R(virtualV0(BetweenArea)) ) )
    
    StartPoint = np.array( np.bitwise_and(t==t0 , x==x0) )    
    
    N[StartPoint] = n0
    
    EndPoint = np.array( np.bitwise_and(t==t1 , x==x1) )
    
    N[EndPoint] = n0 + m
    
    return N
    
import matplotlib as mat
from math import *
import pylab as pyl
import numpy as np

class Main:
    #Les caract�ristiques de notre mod�le, le diagramme fondamental peut etre Triangulaire, mod�le de Greenshield ect... Se r�ferer � la Superclass...
    def __init__(self,fundamental_diag,xmin,xmax):
        self.xmin = xmin
        self.xmax = xmax
        self.funddiag = fundamental_diag
        self.Conditions = np.array([])
    

  
    def general(self,FundD,xup,xdown):
    
        self.funddiag = FundD
        self.xmin = xup
        self.xmax = xdown
        return self.general
        
    #Setup les conditions initiales
    # def First_Cond(self,t0,t1,x0,x1,g):
    #     self.Condtions = np.array( [t0 , t1 , x0 , x1, g*(t1 - t0) , 0] )
    # 
    # def Interior_Cond(self,t0,t1,x0,x1,g):
    #     intr = np.array( [t0 , t1 , x0 , x1, g*(t1 - t0) , self.doSol(t0,x0)] )
    #     self.Conditions = np.array( [[self.Condtions] , [intr]] ) 
    #     
    # def dd_Ini_Cond(self,x0,x1,k):
    #     ini = np.array([0,0,x0,x1,-k*(x1-x0),0])
    #     self.Conditions = np.array( ini )
    # 
    # def dd_Ini_Cond(self,x0,x1,k):
    #     int = np.array([0,0,x0,x1,-k*(x1-x0), self.doSol(0,x0)])
    #     self.Conditions = np.array([[self.Conditions],[int]])
    
    #Solution approch�e de N
    def doSol(self,t,x):
        N = np.inf*np.ones(np.shape(t))
        print(self.Conditions)
        for Cond in self.Conditions:
            print(Cond)
            N = min(N,Moskowitz(self.funddiag,t,x,Cond))
        
        return N
    #Verification de la continuit� de N
    def Start_Count(self,t,x):
        N = self.doSol(t,x)
        if np.any(np.isinf(N)):
            N = 0
            if not(self.Conditions.size==0):
                print("L'offset est indertimin�")
        return N
    #Solution explicite de N en fonction des conditions initiales au point x et � la date t
    def explicitSol(self,t,x):
        if np.shape(t) != np.shape(x):
            return "Verifies les dimensions mon ami..."
        N = np.array( np.inf*np.ones(np.shape(t)) )
        i=0
        indexing = np.array( np.inf*np.ones(np.shape(t)) )
        for Cond in self.Conditions : 
            i+=1
            res = Moskowitz(self.funddiag,t,x,Cond)
            LowerArea = res <= N
            indexing[LowerArea] = i
            N[LowerArea] = res[LowerArea]
        return [N,indexing]
    #Solution explicite de N en fonction des conditions initiales au point x et � la date t
    def density(self,t,x,indexing):
        k = np.array(np.inf*np.ones(t.shape[0]))
        if np.shape(indexing) != np.shape(t):    
            return "Les dimensions et toi �a fait deux... x et t!!!!!!"
        if np.shape(indexing) != np.shape(t):
            return "mauvaise indexation"
        i = 0
        for Cond in self.Conditions:
            i+=1
            ActionArea = index==1
            k[ActionArea] = Density(self.funddiag,t[ActionArea],x[ActionArea],Cond)
        return k
    
    def Dens_Ini(self,x,kx):
        # On set up les conditions initiliales en fonction des densit�s initiales de la route � chaque abscisse 
        # ainsi d(0,x) = kx(i) pour tout x dans [x[i] , x[i+1]] dim(x)=n et dim(k)=n-1
        if len(x) - 1 != len(kx):
            return "Probl�me de dimension de x et de la densit�"
        N = self.Start_Count(np.zeros(np.shape(x)),x) 
        xspacing = np.diff(x)
        xstart = x[0: len(x)-1]
        xend = x[1 : len(x)]
        Numbcars = - np.multiply(kx , xspacing) # l integrale de kx sur toute la longeur de la route pour chaque abscisse
        sumc = np.array(np.cumsum(Numbcars[0:len(Numbcars)-1]))
        Carstotal = N + np.array([0] + [sumc[0],sumc[1]])
        z = np.zeros(np.shape(kx))
        self.Conditions = np.transpose(np.stack((np.transpose(z),np.transpose(z) ,np.transpose(xstart) , np.transpose(xend) , np.transpose(Numbcars) , np.transpose(Carstotal))))

     # On set up les upstream Flow en  fonction
    def UpFlow(self,t,qt):
        if  len(t) - 1 != len(qt):
            return "Probl�me de dimension de t et du flux"
        N = self.Start_Count(t[0],self.xmin) #
        timeint = np.diff(t)
        timestart = t[1: len(t)-1]
        timeend = t[2 : len(t)]
        Numbcars = np.multiply(qt , timeint) # l integrale de qt sur toute la longeur de la route pour chaque abscisse
        Carstotal = N + [0 , np.cumsum(Numbcars[1:len(Numbcars)-1])]
        b = np.one(np.shape(np.transpose(qt))*(self.xmin))
        self.Conditions = [[self.Conditions] , [np.transpose(timestart),np.transpose(timeend),b , b,                     np.transpose(Numbcars),np.transpose(Carstotal)]]
     
    def DownFlow(self,t,qt):
        if t.shape[0] != 1 or (qt).shape[0] != 1 or t.shape[1] - 1 != (qt).shape[1]:
            return "Probl�me de dimension de t et du flux"
        N = self.Start-Count(self,t[0],self.xmax) #
        timeint = np.diff(t)
        timestart = t[1: t.shape[1]-1]
        timeend = t[2 : t.shape[1]]
        Numbcars = np.multiply(qt , timeint) # l integrale de qt sur toute la longeur de la route pour chaque abscisse
        Carstotal = N + [0 , np.cumsum(Numbcars[1:len(Numbcars)-1])]
        b = np.one(np.shape(np.transpose(qt))*(self.xmax))
        self.Conditions = [[self.Conditions] , [np.transpose(timestart),np.transpose(timeend),b , b, np.transpose(Numbcars),np.transpose(Carstotal)]]
                
#Par exemple ici on crée un diagramme Triangulaire
#Avec la vitesse free 36 m/s (130 km/h)
#La vitesse de l'onde congestion -5 m/s (cf Treiber) donnée de test
#La densité maximale 0,2 vehicule / m en prenant l'approximation q'un vehicule
#fait 4 m plus 1 m de distance de sécuirté

funddiag = Diagramme_triangualaire(34,-5,0.2)

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
MyEnv.UpFlow([0,20,40,50],[0.4,0.01,0.2])

#Puis on set up le flow sortant pour chaque temps à l'abscisse xmax

MyEnv.DownFlow([0,30,35,50], [0.3,0, 0.1])

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


