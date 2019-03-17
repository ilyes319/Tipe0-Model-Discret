

class Diagramme_triangualaire(Diagramme_fondammental):
    """Creation du diagramme triangualaire liant le flux � la densit�"""
    def __init__(self,Veff = 10,T = 2,leff = 10, pj = 1):
        self.Vf = Vf #Soit vf la vitesse maximal desir� par l'utilsateur sur cette route
        self.w= w  #vitesse de congestion
        self.pmax = pmax #Soit kmax la densit� maximale
        self.k_c = -swspeed*kmax/(ffspeed-swspeed) ##Soit kmax la densit� maximale avant saturation
   
    def density(self,v):
        k = np.ones(v.shape)
        if v >= self.w and v <= self.Vf:
            k(self,v)= self.k_c
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
          if k < self.k_c :
              v = self.Vf
              
          else
              v = self.w
              

              
             
               