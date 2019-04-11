class Vignette ():
    idPhoto=[]
    tags = []
    orientation = "H"
    def __init__(self,id,tags, ori):
        self.idPhoto=id
        self.tags = list(set(tags))
        self.orientation = ori
    
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

def lireInstance(fileName,pourcent):
    """Exercice 1.2/1.3
    Prend un certain nombre de d'image dans une instance et en retourne deux tableaux:
    Un pour les images horizontales
    Un pour les verticales
    """
    instanceH = []
    instanceV = []
    fichier = open(fileName,"r")
    nb = int(fichier.readline())
    print(nb)
    cpt = 0
    line = fichier.readline()
    while(line != None and cpt < nb*pourcent/100):
        print(cpt)
        print(line)
        line = line.split(" ")
        ori = line[0]
        print("ori : "+ori)
        id = cpt
        nbTags = int(line[1])
        print("id : "+str(id))
        tags = []
        for i in range(2,len(line)):
            if("\n" in line[i]):
                tags.append(line[i][0:len(line[i])-1])
            else:
                tags.append(line[i])
            print(line[i])
        line = fichier.readline()
        if(ori == "H"):
            instanceH.append(Vignette(id,tags,ori))
        else:
            instanceV.append(Vignette(id,tags,ori))
        cpt+=1

    return instanceH,instanceV
        
def saveInstance(instance,fileName):
    """
    Sauvegarde une instance dans un fichier texte
    """
    fichier = open(fileName,"w")
    for i in instance.listeV:
        if(i.orientation == "H"):
            fichier.write(str(i.idPhoto)+"\n")
        else:
            fichier.write(str(i.idPhoto[0])+" "+str(i.idPhoto[1]))
    fichier.close()
def question13():
    """ Question 1.3
    lis les fichier de l'instance a_example.txt 
    Trie les photos dans deux tableau 
    Cree une presentation avec d abord les photos horizontales puis les verticales 2 a 2"""
    h,v = lireInstance("Instances/a_example.txt",100)
    pres = Presentation()
    print("H")
    for i in h:
        pres.addVignette(i)
    print("V")
    for i in range(0,len(v),2):
        v = Vignette([v[i].idPhoto,v[i+1].idPhoto],v[i].tags+v[i+1].tags,"V")
        pres.addVignette(v)

    print("Presentation")
    for i in pres.listeV:
        print(i.toString())

    print("Score : "+str(pres.evaluate()))
    saveInstance(pres,"resultat.txt")
question13()