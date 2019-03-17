import numpy as np 
def Moskowitz(Diagramme_fondamental,ti,xi,weak_cond):
    
    """Calcule la fonction de Moskowitz en t,x avec les conditions faibles donnees et le diagramme fondamental"""
    t = np.array(ti)
    x = np.array(xi)
    if t.shape != x.shape:
        return "t et x sont de dimensions differentes"
    
    N = np.array(np.inf*np.ones(t.shape))   #Matrice representant les densit?s ? chaque abscisse discretisee
    
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
    
    
    CharacterArea = np.array( np.bitwise_and(
    
    virtualV0 >= Diagramme_fondamental.speed(k1) , 
    
    np.bitwise_and( np.bitwise_or( ( virtualV0 <= Diagramme_fondamental.speed(k1) , 
    
    (np.bitwise_and (np.bitwise_and( virtualV0 <= velObserver , virtualV0 <= np.array( Diagramme_fondamental.speed(0) ) )  , 
    
    ( np.invert(np.array(EndArea)) ) ) ) ) ) ) )  )
    
    
   
    DownCharacArea = np.array(np.bitwise_and( virtualV0 <= velObserver , CharacterArea ))
    
    UpCharacArea = np.array( np.bitwise_and(VirtualV0 >= velObserver , numpy.array(CharacterArea)) )
    N[UpCharacArea] = n0 + (x0 - x(UpCharacArea))*k1 + (t(UpCharacArea)-t0)*Diagramme_fondamental.flow(k1)
    N[DownCharacArea] = n0 + (x0 - x[DownCharacArea])*k2 + (t[DownCharacArea]-t0)*Diagramme_fondamental.flow(k1)
    
    BetweenArea = np.array( np.bitwise_and.reduce( ActionArea ,( np.bitwise_not(EndArea) ) , ( np.bitwise_not(CharacterArea) ) ) )
    
    N[BetweenArea] = n0 + np.multiply( (t[BetweenArea]  -t0) , np.array(Diagramme_fondamental.R(virtualV0(BetweenArea)) ) )
    
    StartPoint = np.array( np.bitwise_and(t==t0 , x==x0) )    
    
    N[StartPoint] = n0
    
    EndPoint = np.array( np.bitwise_and(t==t1 , x==x1) )
    
    N[EndPoint] = n0 + m
    
    return N