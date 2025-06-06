from PyQt6.QtWidgets import QApplication, QMainWindow
from ANP import Ui_MainWindow
import ANP_fonctions as af
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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


        self.ui_main_window.pushButton_import1.clicked.connect(lambda: af.remplir_tableau(self.ui_main_window.table1, self.ui_main_window.table2, self.ui_main_window.table3, self.ui_main_window.table4, af.on_pushButton_import1_clicked()))
        self.ui_main_window.pushButton_import2.clicked.connect(lambda: af.import_and_make_plot(self))

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

        # Données et en-têtes de table4
        self.headers_table4 = ["R[OIII]", "R[NII]", "R[SII]"]
        self.ToolTips4 = ["à venir","à venir","à venir"]

        data_table4 = [
            ["", "", ""],
            ["T (K)", "T (K)", "Ne (cm-3)"],
            ["", "", ""],
        ]

        # Création et assignation du modèle avec tooltips
        model4 = af.TableModelTooltips(data_table4, self.headers_table4, self.ToolTips4)
        self.ui_main_window.table4.setModel(model4)
        
        # Ajuster la taille des colonnes et des lignes automatiquement
        self.ui_main_window.table4.resizeColumnsToContents()
        self.ui_main_window.table4.resizeRowsToContents()

        # Ajuster la taille du widget de la table en fonction du contenu
        af.adjustTableWidgetSize(self.ui_main_window.table4)

##############################################################################################################

        # Création de la figure matplotlib
        self.figure = Figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.figure.set_facecolor('#4C566A')
        self.ax.set_facecolor('black')
        
        # Ajout du canvas au layout existant
        layout = QVBoxLayout(self.ui_main_window.graph_layout)
        layout.addWidget(self.canvas)

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()