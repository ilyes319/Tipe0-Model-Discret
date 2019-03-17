
import matplotlib as mat
from math import *
import pylab as pyl
import numpy as np

class Main:
    #Les caractéristiques de notre modèle, le diagramme fondamental peut etre Triangulaire, modèle de Greenshield ect... Se réferer à la Superclass...
    def _init_(self,fundamental_diag,xmin,xmax):
        
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
    def First_Cond(self,t0,t1,x0,x1,g):
        self.Condtions = np.array( [t0 , t1 , x0 , g*(t1 - t0) , 0] )
    
    def Interior_Cond(self,t0,t1,x0,x1,g):
        intr = np.array( [t0 , t1 , x0 , g*(t1 - t0) , self.doSol(t0,x0)] )
        self.Conditions = np.array( [[self.Condtions] , [intr]] ) 
        
    def dd_Ini_Cond(self,x0,x1,k):
        ini = np.array([0,0,x1,-k*(x1-x0),0])
        self.Conditions = np.array( ini )
    
    def dd_Ini_Cond(self,x0,x1,k):
        int = np.array([0,0,x0,x1,-k*(x1-x0), self.doSol(0,x0)])
        self.Conditions = np.array([[self.Conditions],[int]])
    
    #Solution approchée de N
    def doSol(self,t,x):
        N = np.inf*np.ones(np.shape(t))
       
        for Cond in self.valConditions:
            N = min(N,Moskowitz(self.funddiag,t,x,Cond))
       
    return N
    #Verification de la continuité de N
    def Start_Count(self,t,x):
        N = doSol(t,x)
        if np.isinf(N):
            N=0
            if not(isempty(self.cond)):
                print("L'offset est indertiminé")
        
        return N
    #Solution explicite de N en fonction des conditions initiales au point x et à la date t
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
    #Solution explicite de N en fonction des conditions initiales au point x et à la date t
    def density(self,t,x,indexing):
        k = np.array(np.inf*np.ones(t.shape[0]))
        if np.shape(indexing) != np.shape(t):    
            return "Les dimensions et toi ça fait deux... x et t!!!!!!"
        if np.shape(indexing) != np.shape(t):
            return "mauvaise indexation"
        i = 0
        for Cond in self.Conditions:
            i+=1
            ActionArea = index==1
            k[ActionArea] = Density(self.funddiag,t[ActionArea],x[ActionArea],Cond)
        return k
    
    def Dens_Ini(self,x,kx):
     # On set up les conditions initiliales en fonction des densités initiales de la route à chaque abscisse 
     # ainsi d(0,x) = kx(i) pour tout x dans [x[i] , x[i+1]] dim(x)=n et dim(k)=n-1
     if x.shape[0] != 1 or (kx).shape[0] != 1 or x.shape[1] - 1 != (kx).shape[1]:
         return "Problème de dimension de x et de la densité"
     N = self.Start-Count(self,0,x[0]) #
     xspacing = np.diff(x)
     xstart = x[1: x.shape[1]-1]
     xend = x[2 : x.shape[1]]
     Numbcars = - np.multiply(kx , xspacing) # l integrale de kx sur toute la longeur de la route pour chaque abscisse
     Carstotal = N + [0 , np.cumsum(Numbcars[1:len(Numbcars)-1])]
     z = np.zeros(np.shape(kx))
     self.Conditions = [[self.Conditions] , [z,z,np.transpose(xstart),np.transpose(xend),np.transpose(Numbcars),np.transpose(Carstotal)]]
     
     # On set up les upstream Flow en  fonction
    def UpFlow(self,t,qt):
        if t.shape[0] != 1 or (qt).shape[0] != 1 or t.shape[1] - 1 != (qt).shape[1]:
         return "Problème de dimension de t et du flux"
     N = self.Start-Count(self,t[0],self.xmin) #
     timeint = np.diff(t)
     timestart = t[1: t.shape[1]-1]
     timeend = t[2 : t.shape[1]]
     Numbcars = np.multiply(qt , timeint) # l integrale de qt sur toute la longeur de la route pour chaque abscisse
     Carstotal = N + [0 , np.cumsum(Numbcars[1:len(Numbcars)-1])]
     b = np.one(np.shape(qt))*(self.xmin)
     self.Conditions = [[self.Conditions] , [np.transpose(timestart),np.transpose(timeend),b , b, np.transpose(Numbcars),np.transpose(Carstotal)]]
     
     def DownFlow(self,t,qt):
        if t.shape[0] != 1 or (qt).shape[0] != 1 or t.shape[1] - 1 != (qt).shape[1]:
         return "Problème de dimension de t et du flux"
     N = self.Start-Count(self,t[0],self.xmax) #
     timeint = np.diff(t)
     timestart = t[1: t.shape[1]-1]
     timeend = t[2 : t.shape[1]]
     Numbcars = np.multiply(qt , timeint) # l integrale de qt sur toute la longeur de la route pour chaque abscisse
     Carstotal = N + [0 , np.cumsum(Numbcars[1:len(Numbcars)-1])]
     b = np.one(np.shape(qt))*(self.xmax)
     self.Conditions = [[self.Conditions] , [np.transpose(timestart),np.transpose(timeend),b , b, np.transpose(Numbcars),np.transpose(Carstotal)]]
