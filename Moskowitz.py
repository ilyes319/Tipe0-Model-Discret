import numpy as np
def Moskowitz(Diagramme_fondamental,ti,xi,weak_cond):
    
    """Calcule la fonction de Moskowitz en t,x avec les conditions faibles donnees et le diagramme fondamental"""
    t = np.array(ti)
    x = np.array(xi)
    if t.shape != x.shape:
        return "t et x sont de dimensions differentes"
    
    N = np.array(math.inf*np.ones(t.shape))   #Matrice representant les densités à chaque abscisse discretisee
    t0 = weak_cond(1)
    t1 = weak_cond(2)
    x0 = weak_cond(3)
    x1 = weak_cond(4)
    m = weak_cond(5)
    n0 = weak_cond(6)
    
    if t1 == t0:
        k1 = 0
        k2 = -m/(x1-X0)
    else:
        dens = Diagramme_fondamental.densities((x1-xo)/(t1-t0),m/(t1-t0))
        k1 = dens[1]
        k2 = dens[2]
    
    AfterBeging = t>=t0
    AfterEnd = t >= t1
    
    velObserver= (x1-x0) / (t1-t0)
    VirtualV0 = N
    VirtualV1 = N
    
    VirtualV0[AfterBeging] = np.array( ( np.divide((x[AfterBeging]-x0),(t[AfterBeging]-t0) ) ) )
    
    VirtualV1[AfterEnd] = np.array( ( np.divide( (x[AfterEnd]-x1),(t[AfterEnd]-t1) ) ) )
    
    ActionArea = np.array(np.bitwise_and( (np.min(virtualV0,virtualV1)) <= Diagramme_fondamental.speed(0) 
    
    , (np.max(virtualV0,virtualV1) >= np.array( Diagramme_fondamental.speed(Diagramme_fondamental.kmax) ) ) ) )
     
    EndArea = np.array( (np.bitwise_and( virtualV1 <= np.array(Diagramme_fondamental.speed(k1)) 
    
    , virtualV1 >= np.array( Diagramme_fondamental.speed(k2) ) ) ) )
    
    N[EndArea] = n0 + m + np.multiply( np.array( (t[EndArea]-t1) ), np.array(Diagramme_fondamental.R(VirtualV1[EndArea]) ))
    
    CharacterArea = np.array( np.bitwise_and.reduce(
    
    VirtualV0 >= Diagramme_fondamental.speed(k1) , 
    
    np.bitwise_or( ( virtualV0 <= Diagramme_fondamental.speed(k1) , 
    
    np_bitwise_and( virtualV0 <= velObserver , virrtualV0 < Diagramme_fondamental.speed(0) ) ) ), 
    
    ( np.bitwise_not(EndArea) ) ) )
    
    UpCharacArea = np.array( np.bitwise_and(VirtualV0 > velObserver , CharacterArea) )
    
    N[UpCharacArea] = n0 + (x0 - x(UpCharacArea))*k1 + (t(UpCharacArea)-t0)*Diagramme_fondamental.flow(k1)
    
    DownCharacArea = np.array( np.bitwise_and( VirtualV0 <= velObserver , CharacDomain ) )
    
    N[DownCharacArea] = n0 + (x0 - x[DownCharacArea])*k2 + (t[DownCharacArea]-t0)*Diagramme_fondamental.flow(k1)
    
    BetweenArea = np.array( np.bitwise_and.reduce( ActionArea ,( np.bitwise_not(EndArea) ) , ( np.bitwise_not(CharacterArea) ) ) )
    
    N[BetweenArea] = n0 + np.multiply( (t[BetweenArea]  -t0) , np.array(Diagramme_fondamental.R(virtualV0(BetweenArea)) ) )
    
    StartPoint = np.array( np.bitwise_and(t==t0 , x==x0) )    
    
    N[StartPoint] = n0
    
    EndPoint = np.array( np.bitwise_and(t==t1 , x==x1) )
    
    N[EndPoint] = n0 + m
    
    return N
    
    
    
    
    
    
    
        
        
        
    

