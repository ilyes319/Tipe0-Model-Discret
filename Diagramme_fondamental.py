#!/usr/bin/env python3
#encoding: windows-1252

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class Diagramme_fondamental:
    """Decrit un diagramme fondamental et tout autre diagramme est une sous classe de celle l�"""
    def _init_(self,kmax):
        self.kmax=kmax
      
     
    def _methods_(self):
        
        q = flow(k) #Un diagramme fondamental est essentiellement la fonction reliant la densit au flux 
        
        v = speed(k) #Le diagramme fondamental est au moins une fois derivable sur l'intervalle [0,kmax]
        
        r = R(v) #La transform�e de Legendre du dragramme fondamental est une fonction covexe permettant de comprendre une fonction avec sa deriv�e
        
        resultat = densities(v,g) #Donne la densit� oiur un flow g pour un observateur � la vitesse v donc tel que flow(k)=k*v+g
        
        k = density(v) #Calcul la transform�e inverse de legendre la deriv�e de R. Il s'agit au final de trouver la densit� exacte
        
        
        
        
            
        
        
        
        
        
        
