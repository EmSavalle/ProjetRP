from gurobipy import *
class Vignette ():
    idPhoto=[]
    tags = []
    orientation = ""
    def __init__(self,id,tags, ori):
        self.idPhoto=id
        self.tags = list(set(tags))
        self.orientation = ori
    def testScore(self,v2):
        tag1 = self.tags
        tag2 = v2.tags
        nbCommuns = 0
        nbDiff1 = 0
        nbDiff2 = 0
        scoreTotal=0
        for i in tag1:
            if(i in tag2):
                nbCommuns+=1
        nbDiff1 = len(tag1) - nbCommuns
        nbDiff2 = len(tag2) - nbCommuns
        scoreTotal+=min(nbCommuns,nbDiff1,nbDiff2)
        return scoreTotal
    def combineV(self,v2):
        if(v2.orientation != "V" or self.orientation != "V" or isinstance(self.idPhoto,list)):
            return False
        self.tags.extend(v2.tags)
        self.tags=list(set(self.tags))
        self.idPhoto = [self.idPhoto,v2.idPhoto]
        return True
    def isSingleV(self):
        if(self.orientation == "H" or isinstance(self.idPhoto,list)):
            return False
        return True
    def toString(self):
        return "Vignette : Id : "+str(self.idPhoto) + " Tags : " + str(self.tags) + " Orientation : "+self.orientation

class Presentation():
    listeV = []
    def __init__(self,arrayVignette=[]):
        self.listeV = arrayVignette
    def addVignette(self,v):
        self.listeV.append(v)
    def evaluate(self):
        """ Question 1.6
        Calcul du score de la presentation selon les regles defini par le projet"""
        if (len(self.listeV) <=1):
            return 0
        else:
            scoreTotal = 0
            for i in range(0, len(self.listeV)-1):
                tag1 = self.listeV[i].tags
                tag2 = self.listeV[i+1].tags
                nbCommuns = 0
                nbDiff1 = 0
                nbDiff2 = 0
                for i in tag1:
                    if(i in tag2):
                        nbCommuns+=1
                nbDiff1 = len(tag1) - nbCommuns
                nbDiff2 = len(tag2) - nbCommuns
                scoreTotal+=min(nbCommuns,nbDiff1,nbDiff2)
        return scoreTotal
    def copy(self):
        new = Presentation(copy.deepcopy(self.listeV))
        return new
    def swap(self,id1,id2):
        v1 = self.listeV[id1]
        v2 = self.listeV[id2]
        self.listeV[id1] = v2
        self.listeV[id2] = v1
inst_b = "Instances/b_lovely_landscapes.txt"
import projet
def lireInstance(fileName,pourcent,verbose = False):
    """Exercice 1.2/1.3
    Prend un certain nombre de d'image dans une instance et en retourne deux tableaux:
    Un pour les images horizontales
    Un pour les verticales
    """
    instanceH = []
    instanceV = []
    fichier = open(fileName,"r")
    nb = int(fichier.readline())
    if(verbose):
        print(nb)
    cpt = 0
    line = fichier.readline()
    while(line != None and cpt < nb*pourcent):
        if(verbose):
            print(cpt)
            print(line)
        line = line.split(" ")
        ori = line[0]
        if(verbose):
            print("ori : "+ori)
        id = cpt
        nbTags = int(line[1])
        if(verbose):
            print("id : "+str(id))
        tags = []
        for i in range(2,len(line)):
            if("\n" in line[i]):
                tags.append(line[i][0:len(line[i])-1])
            else:
                tags.append(line[i])
            if(verbose):
                print(line[i])
        line = fichier.readline()
        if(ori == "H"):
            instanceH.append(Vignette(id,tags,ori))
        else:
            instanceV.append(Vignette(id,tags,ori))
        cpt+=1

    return instanceH,instanceV

def solveurPL(vignettes):
    
    
    # Range of plants and warehouses
    
    
    
    m = Model("mogplex")     
            
    # declaration variables de decision
    x = []
    for i in vignettes:
        #X : id de la vignette correspondant a la position i
        x.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))
    
    # maj du modele pour integrer les nouvelles variables
    m.update()
    
    obj = LinExpr();
    obj =0
    for j in range(0,len(vignettes)):
        
         #Calcul du score 
        if(j == 0):
            objt += 0
        else:
            obj+=score(vignettes,j,j-1)
                
            
    # definition de l'objectif
    if(boolMax):
        m.setObjective(obj,GRB.MAXIMIZE)
        for i in lignes:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) <= b[i], "Contrainte%d" % i)
    else:
        m.setObjective(obj,GRB.MINIMIZE)
        for i in lignes:
            m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)
    # Definition des contraintes
    
    # Resolution
    m.optimize()
    
    
    print("")                
    print('Solution optimale:')
    for j in colonnes:
        print(x[j])
        print(j)
        print('x%d'%(j+1), '=', x[j].x)
    print("")
    print('Valeur de la fonction objectif :', m.objVal)
    return x,m.objVal


inst= inst_b
taille_analyse = 0.01
h,v=lireInstance(inst,taille_analyse)
solveurPL(h)
