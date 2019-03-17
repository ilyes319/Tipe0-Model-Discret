#!/usr/bin/env python3
#encoding: windows-1252

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

def Density(Diagramme_fondamental,ti,xi,weak_cond):
    
    """Calcule la fonction de Moskowitz en t,x avec les conditions faibles donnees et le diagramme fondamental"""
    x = np.array(xi)
    t = np.array(ti)
    
    if t.shape != x.shape:
        return "t et x sont de dimensions differentes"
    
    k = np.array( math.inf*np.ones(t.shape) )   #Matrice representant les densités à chaque abscisse discretisee
    t0 = weak_cond[0]
    t1 = weak_cond[1]
    x0 = weak_cond[2]
    x1 = weak_cond[3]
    m = weak_cond[4]
    n0 = weak_cond[5]
    
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
    VirtualV0 = k
    VirtualV1 = k
    
    VirtualV0[AfterBeging] = np.array( ( np.divide((x[AfterBeging]-x0),(t[AfterBeging]-t0) ) ) )
    
    VirtualV1[AfterEnd] = np.array( ( np.divide( (x[AfterEnd]-x1),(t[AfterEnd]-t1) ) ) )
    
    ActionArea = np.array(np.bitwise_and( (np.min(virtualV0,virtualV1)) <= Diagramme_fondamental.speed(0) 
    
    , (np.max(virtualV0,virtualV1) >= np.array( Diagramme_fondamental.speed(Diagramme_fondamental.kmax) ) ) ) )
     
    EndArea = np.array( (np.bitwise_and( virtualV1 <= np.array(Diagramme_fondamental.speed(k1)) 
    
    , virtualV1 >= np.array( Diagramme_fondamental.speed(k2) ) ) ) )
    
    k[EndArea] = Diagramme_Fondamental.density(virtualV1[EndArea])
    
   CharacterArea = np.array( np.bitwise_and.reduce(
    
    VirtualV0 >= Diagramme_fondamental.speed(k1) , 
    
    np.bitwise_or( ( virtualV0 <= Diagramme_fondamental.speed(k1) , 
    
    np_bitwise_and( virtualV0 <= velObserver , virrtualV0 < Diagramme_fondamental.speed(0) ) ) ), 
    
    ( np.bitwise_not(EndArea) ) ) )
    
    UpCharacArea = np.array( np.bitwise_and(VirtualV0 > velObserver , CharacterArea) )
    
    k[UpCharacArea] = k1
    
    DownCharacArea = np.array( np.bitwise_and( VirtualV0 <= velObserver , CharacDomain ) )
    
    N[DownCharacArea] = k2
    
    BetweenArea = np.array( np.bitwise_and.reduce( ActionArea ,( np.bitwise_not(EndArea) ) , ( np.bitwise_not(CharacterArea) ) ) )
    
    N[BetweenArea] = Diagramme_fondamental.density(virtualV0[isInBegDomain])
    
    StartPoint = np.bitwise_and(t==t0 , x==x0)    
    
    N[StartPoint] = k2
    
    EndPoint = np.bitwise_and(t==t1 , x==x1)
    
    N[EndPoint] = k2
    return k
