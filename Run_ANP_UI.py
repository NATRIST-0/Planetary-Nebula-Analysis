from PyQt6.QtWidgets import QApplication, QMainWindow
from ANP import Ui_MainWindow
import ANP_fonctions as af

# Création du graphique
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import pandas as pd
from PyQt6.QtWidgets import QVBoxLayout


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuration de la fenêtre principale
        af.theme(self)

        # Initialisation de l'interface graphique
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self)
        self.setGeometry(0, 0, 1920, 1080)


        self.ui_main_window.pushButton_import.clicked.connect(lambda: af.remplir_tableau(self.ui_main_window.table1, self.ui_main_window.table2, self.ui_main_window.table3, af.on_pushButton_import_clicked()))

##############################################################################################################
    
        # Données et en-têtes de table1
        self.headers_table1 = ["λ (Å)", "Raie", "I₀Gauss", "I₀/I(Hβ)=100", " I_c ", "Δ%"]
        self.ToolTips1 = [
            "Longueur d'onde en Angströms",
            "Nom de la raie spectrale",
            "Intensité observée (Gauss)",
            "Intensité relative à Hβ (normalisée à 100)",
            "Intensité corrigée de l'extinction",
            "Pourcentage de rebleuïssement"
        ]

        data_table1 = [
            [4340.47, "H I", "", "", "", ""],
            [4363.21, "[O III]", "", "", "", ""],
            [4685.68, "He II", "", "", "", ""],
            [4861.33, "H I", "", "", "", ""],
            [4958.92, "[O III]", "", "", "", ""],
            [5006.85, "[O III]", "", "", "", ""],
            [5754.57, "[N II]", "", "", "", ""],
            [5875.65, "He I", "", "", "", ""],
            [6548.06, "[N II]", "", "", "", ""],
            [6562.82, "H I", "", "", "", ""],
            [6583.39, "[N II]", "", "", "", ""],
            [6716.50, "[S II]", "", "", "", ""],
            [6730.70, "[S II]", "", "", "", ""],
        ]


        # Création et assignation du modèle avec tooltips
        model1 = af.TableModelTooltipsWithColors(data_table1, self.headers_table1, self.ToolTips1)
        self.ui_main_window.table1.setModel(model1)
        
        # Ajuster la taille des colonnes et des lignes automatiquement
        self.ui_main_window.table1.resizeColumnsToContents()
        self.ui_main_window.table1.resizeRowsToContents()

        # Ajuster la taille du widget de la table en fonction du contenu
        af.adjustTableWidgetSize(self.ui_main_window.table1)

##############################################################################################################

        # Données et en-têtes de table2
        self.headers_table2 = ["n", "Raie", "Valeur mesurée", "Valeur théorique", "Rebleuïssement"]
        self.ToolTips2 = ["Niveau d'énergie", "Nom de la raie spectrale", "Valeur mesurée de la raie", "Valeur théorique de la raie", "Pourcentage de rebleuïssement"]
        data_table2 = [
            [3, "Hα", "", "2.86", ""],
            [4, "Hβ", "1", "1", "1"],
            [5, "Hγ", "", "0.47", ""],
        ]

        # Création et assignation du modèle
        model2 = af.TableModelTooltips(data_table2, self.headers_table2, self.ToolTips2)
        self.ui_main_window.table2.setModel(model2)

        # Ajuster la taille des colonnes et des lignes automatiquement
        self.ui_main_window.table2.resizeColumnsToContents()
        self.ui_main_window.table2.resizeRowsToContents()

        # Ajuster la taille du widget de la table en fonction du contenu
        af.adjustTableWidgetSize(self.ui_main_window.table2)

##############################################################################################################

        # Données et en-têtes de table3
        self.headers_table3 = ["c(Hβ)", "E (V-B)", "λ 5007/4959", "λ 6583/6548", "λ 6583/6562"]
        self.ToolTips3 = [
            "Coefficient d'extinction",
            "Exces de couleur",
            "Rapport des longueurs d'onde [O III] 5007/4959\nValeur théorique : 2.98\nValeur observée : 3.01\n± 0.23",
            "Rapport des longueurs d'onde [N II] 6583/6548\nValeur théorique : 2.85\nValeur observée : 2.92\n± 0.32",
            "Rapport des longueurs d'onde [N II] 6583/6562\nIndicant si la nébueluse est ionisée par un rayonnement épais ou fin"
        ]

        data_table3 = [
            ["", "", "", "", ""],
        ]

        # Création et assignation du modèle avec tooltips
        model3 = af.TableModelTooltips(data_table3, self.headers_table3, self.ToolTips3)
        self.ui_main_window.table3.setModel(model3)
        
        # Ajuster la taille des colonnes et des lignes automatiquement
        self.ui_main_window.table3.resizeColumnsToContents()
        self.ui_main_window.table3.resizeRowsToContents()

        # Ajuster la taille du widget de la table en fonction du contenu
        af.adjustTableWidgetSize(self.ui_main_window.table3)

##############################################################################################################

        # Création de la figure matplotlib
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        
        # Ajout du canvas au layout existant
        layout = QVBoxLayout(self.ui_main_window.graph_layout)
        layout.addWidget(self.canvas)

        # Fonction pour créer et mettre à jour le graphique
        def update_graph(self):
            self.ax.clear()
            
            # Définition du spectre
            file_path = r"C:\Users\GAYRARD\Documents\GitHub\Planetary-Nebula-Analysis\add ons\_m42_20230220_862_Olivier Gayrard.dat"
            mySpectra = pd.read_csv(file_path, sep=" ", header=None, names=['wavelength', 'intensities'])
            mySpectra = mySpectra[(mySpectra['wavelength'] >= 3800) & (mySpectra['wavelength'] <= 7600)] #keep only the values between 3800 and 7600 Å

            wavelengths = mySpectra['wavelength']
            spectrum = mySpectra['intensities']

            # Configuration des couleurs
            clim = (3800, 7500)
            norm = plt.Normalize(*clim)
            wl = np.arange(clim[0], clim[1] + 1, 2)
            colorlist = list(zip(norm(wl), [af.wavelength_to_rgb(w) for w in wl]))
            spectralmap = matplotlib.colors.LinearSegmentedColormap.from_list("spectrum", colorlist)

            # Tracé du spectre d'intensité
            self.ax.plot(wavelengths, spectrum, color='black', linewidth=1)

            # Création de l'image du spectre
            extent = (np.min(wavelengths), np.max(wavelengths), np.min(spectrum), np.max(spectrum))
            self.ax.imshow(np.tile(wavelengths, (len(spectrum), 1)), 
            aspect='auto', extent=extent, cmap=spectralmap, clim=clim)

            # Configuration du graphique
            self.ax.set_xlabel('Longueur d\'onde (Å)', color="white")
            self.ax.set_ylabel('Intensité mesurée', color="white")
            self.ax.set_ylim(0, max(mySpectra['intensities']))
            self.ax.tick_params(axis='both', colors='white')
            self.ax.set_title(f'Spectre de {file_path.split("\\")[-1].split(".")[0]}', color="white")
            self.figure.set_facecolor('#4C566A')

            # Remplissage de la zone sous la courbe et contour
            self.ax.fill_between(wavelengths, max(spectrum), spectrum, color="black")
            
            # Mise à jour du canvas
            self.canvas.draw()

        # Appel initial pour afficher le graphique
        update_graph(self)



if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()