from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QApplication,
    QTableWidgetItem
)

import sys, numpy as np
from timeit import default_timer
from app_ui import Ui_MainWindow
from Algo_genetique import genetic_algorithm

class MainWindow(QMainWindow):
    """Classe principale pour l'interface utilisateur de l'algorithme génétique TSP."""
    
    def __init__(self):
        """Initialise la fenêtre principale de l'application."""
        QWidget.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.buttons_actions()

        
    def buttons_actions(self):
        """Définit les actions associées aux boutons de l'interface."""
        # defining the buttons actions
        self.ui.pushButton_matrix.clicked.connect(
            self.generateMatrix
        )
        self.ui.Get_matrix_content.clicked.connect(
            self.getMatrixContent
        )
        self.ui.Random_matrix.clicked.connect(
            self.generate_random_matrix
        )
        self.ui.auto_complete.clicked.connect(
            self.auto_complete
        )


    def generateMatrix(self):
        """Génère une matrice vide avec des valeurs nulles sur la diagonale principale."""
        # generate an empty matrix with nulle values in the main diagonal
        number_of_line = int(self.ui.nbr_villes.text())
        
        for j in range(0,number_of_line):
            self.ui.tableWidget.insertColumn(j)

        for i in range(0,number_of_line):
            self.ui.tableWidget.insertRow(i)
            for j in range(0, number_of_line):
                self.ui.tableWidget.setItem(i , j, QTableWidgetItem(""))
                if i == j:
                    self.ui.tableWidget.setItem(i , j, QTableWidgetItem("0"))


    def generate_random_matrix(self):
        """Génère une matrice symétrique avec des valeurs entières aléatoires."""
        # generate a symtrical matrix with random int values 
        number_of_line = int(self.ui.nbr_villes.text())

        for j in range(0,number_of_line):
            self.ui.tableWidget.insertColumn(j)

        for i in range(0,number_of_line):
            self.ui.tableWidget.insertRow(i)
            for j in range(0, number_of_line):
                random_number=str(np.random.randint(1,100))
                self.ui.tableWidget.setItem(i , j, QTableWidgetItem(random_number))
                self.ui.tableWidget.setItem(j , i, QTableWidgetItem(random_number))
                if i == j:
                    self.ui.tableWidget.setItem(i , j, QTableWidgetItem("0"))


    def auto_complete(self):
        """Remplit l'autre moitié de la matrice avec les entrées utilisateur 
        pour créer une matrice symétrique."""
        # fills the other half of the matrix with user inputs,
        # to create a symetrical matrix 
        count_row = self.ui.tableWidget.columnCount()
        x=1
        if self.ui.tableWidget.item(0,1).text() == "":
            for k in range (1,count_row):
                for l in range(x):
                    item = self.ui.tableWidget.item(k,l).text()
                    self.ui.tableWidget.setItem(l , k, QTableWidgetItem(item))
                x+=1           
        else:
            for k in range (1,count_row):
                for l in range(x):
                    item = self.ui.tableWidget.item(l,k).text()
                    self.ui.tableWidget.setItem(k , l, QTableWidgetItem(item))
                x+=1           


    def getMatrixContent(self):
        """Récupère les valeurs de la matrice et exécute l'algorithme génétique.
        
        Extrait les données de la matrice de distances, les paramètres de l'algorithme,
        exécute l'algorithme génétique et affiche les résultats avec le temps d'exécution.
        """
        # retrieve the matrix values, and store them in a numpy array
        count_row = self.ui.tableWidget.columnCount()
        mat_distance = []
        for i in range(0,count_row):
            data=[]
            for j in range(0,count_row):
                data.append(
                    float(
                        self.ui.tableWidget.item(i,j).text()
                    )
                )
            mat_distance.append(data)    
        mat_distance=np.array(mat_distance)

        # retrieve the rest of the user inputs.
        nbr_population = int(self.ui.nbr_population.text())
        nbr_iteration = int(self.ui.nbr_iterations.text())
        nbr_villes=int(self.ui.nbr_villes.text())

        villes=range(nbr_villes)

        # calculate the execution time of the algorithm 
        debut=default_timer()
        (score,meilleur)= genetic_algorithm(villes,mat_distance,nbr_population,nbr_iteration)
        fin=default_timer()
        # prints theoutput of the results
        self.ui.affichage.setText(f"La meilleur solution trouvé est {meilleur} avec un score de {score}.\n\nLe temps d'execution est {fin-debut}s.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
