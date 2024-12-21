from PyQt6.QtWidgets import QApplication, QMainWindow
from ANP import Ui_MainWindow
import ANP_fonctions as af

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuration de la fenêtre principale
        self.setGeometry(50, 50, 1920, 1080)
        af.theme(self)

        # Initialisation de l'interface graphique
        self.ui_main_window = Ui_MainWindow()
        self.ui_main_window.setupUi(self)

        self.ui_main_window.pushButton_import.clicked.connect(lambda: af.remplir_tableau(self.ui_main_window.table1, af.on_pushButton_import_clicked()))

##############################################################################################################

        # Données et en-têtes de table1
        headers_table1 = ["λ (Å)", "Raie", "I₀Gauss", "I₀/I(Hβ)=100", "I_c", "Δ%"]
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

        # Création et assignation du modèle
        model1 = af.TableModel(data_table1, headers_table1)
        self.ui_main_window.table1.setModel(model1)

        # Ajuster la taille des colonnes et des lignes automatiquement
        self.ui_main_window.table1.resizeColumnsToContents()
        self.ui_main_window.table1.resizeRowsToContents()

        # Ajuster la taille du widget de la table en fonction du contenu
        af.adjustTableWidgetSize(self.ui_main_window.table1)

##############################################################################################################

        # Données et en-têtes de table2
        headers_table2 = ["n", "Raie", "Valeur mesurée", "Valeur théorique", "ReBleuiement"]
        data_table2 = [
            [3, "Hα", "", "", "", ""],
            [4, "Hβ", "", "", "", ""],
            [5, "Hγ", "", "", "", ""],
        ]

        # Création et assignation du modèle
        model2 = af.TableModel(data_table2, headers_table2)
        self.ui_main_window.table2.setModel(model2)

        # Ajuster la taille des colonnes et des lignes automatiquement
        self.ui_main_window.table2.resizeColumnsToContents()
        self.ui_main_window.table2.resizeRowsToContents()

        # Ajuster la taille du widget de la table en fonction du contenu
        af.adjustTableWidgetSize(self.ui_main_window.table2)

##############################################################################################################

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    app.exec()