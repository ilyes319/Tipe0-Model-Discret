class Main:
    #Les caract?ristiques de notre mod?le, le diagramme fondamental peut etre Triangulaire, mod?le de Greenshield ect... Se r?ferer ? la Superclass...
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
    
    #Solution approch?e de N
    def doSol(self,t,x):
        N = np.inf*np.ones(np.shape(t))
        print(self.Conditions)
        for Cond in self.Conditions:
            print(Cond)
            N = min(N,Moskowitz(self.funddiag,t,x,Cond))
        
        return N
    #Verification de la continuit? de N
    def Start_Count(self,t,x):
        N = self.doSol(t,x)
        if np.any(np.isinf(N)):
            N = 0
            if not(self.Conditions.size==0):
                print("L'offset est indertimin?")
        return N
    #Solution explicite de N en fonction des conditions initiales au point x et ? la date t
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
    #Solution explicite de N en fonction des conditions initiales au point x et ? la date t
    def density(self,t,x,indexing):
        k = np.array(np.inf*np.ones(t.shape[0]))
        if np.shape(indexing) != np.shape(t):    
            return "Les dimensions et toi ?a fait deux... x et t!!!!!!"
        if np.shape(indexing) != np.shape(t):
            return "mauvaise indexation"
        i = 0
        for Cond in self.Conditions:
            i+=1
            ActionArea = index==1
            k[ActionArea] = Density(self.funddiag,t[ActionArea],x[ActionArea],Cond)
        return k
    
    def Dens_Ini(self,x,kx):
        # On set up les conditions initiliales en fonction des densit?s initiales de la route ? chaque abscisse 
        # ainsi d(0,x) = kx(i) pour tout x dans [x[i] , x[i+1]] dim(x)=n et dim(k)=n-1
        if len(x) - 1 != len(kx):
            return "Probl?me de dimension de x et de la densit?"
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
            return "Probl?me de dimension de t et du flux"
        N = self.Start_Count(t[0],self.xmin) #
        timeint = np.diff(t)
        timestart = t[1: len(t)-1]
        timeend = t[2 : len(t)]
        Numbcars = np.multiply(qt , timeint) # l integrale de qt sur toute la longeur de la route pour chaque abscisse
        sumc = np.array(np.cumsum(Numbcars[0:len(Numbcars)-1]))
        Carstotal = N + np.array([0] + [sumc[0],sumc[1]])
        b = np.one(np.shape(np.transpose(qt))*(self.xmin))
        self.Conditions = np.transpose(np.stack( self.Conditions , np.transpose(timestart),np.transpose(timeend),np.transpose(b) 
        , np.transpose(b), np.transpose(Numbcars),np.transpose(Carstotal)))
     
    def DownFlow(self,t,qt):
        if t.shape[0] != 1 or (qt).shape[0] != 1 or t.shape[1] - 1 != (qt).shape[1]:
            return "Probl?me de dimension de t et du flux"
        N = self.Start-Count(self,t[0],self.xmax) #
        timeint = np.diff(t)
        timestart = t[1: t.shape[1]-1]
        timeend = t[2 : t.shape[1]]
        Numbcars = np.multiply(qt , timeint) # l integrale de qt sur toute la longeur de la route pour chaque abscisse
        sumc = np.array(np.cumsum(Numbcars[0:len(Numbcars)-1]))
        Carstotal = N + np.array([0] + [sumc[0],sumc[1]])
        b = np.one(np.shape(np.transpose(qt))*(self.xmax))
        self.Conditions = np.transpose(np.stack( self.Conditions , np.transpose(timestart),np.transpose(timeend),np.transpose(b) 
        , np.transpose(b), np.transpose(Numbcars),np.transpose(Carstotal)))