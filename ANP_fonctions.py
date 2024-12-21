"""
Analyse Nébuleuse Planétaire _ Fonctions
"""
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel
import pandas as pd

def remplir_tableau(table1, data_import):
    if data_import is None:
        return
        
    data_Imes = data_import['Imes']
    data_Imes = data_Imes.astype(float)
    
    # Récupérer le modèle
    model = table1.model()
    
    # Mettre à jour les données dans le modèle
    for i in range(len(data_Imes)):
        index = model.index(i, 2)  # Colonne 2 pour 'I₀Gauss'
        model.setData(index, str(data_Imes[i]), Qt.ItemDataRole.DisplayRole)

    return table1

# Fonction pour gérer le clic sur le bouton d'importation
def on_pushButton_import_clicked():
    # Ouvrir une boîte de dialogue pour sélectionner un fichier
    file_dialog = QFileDialog()
    file_dialog.setNameFilters(["TXT Files (*.txt)", "All Files (*)"])
    file_dialog.setWindowTitle("Ouvrir un fichier")
    
    if file_dialog.exec():
        file_path = file_dialog.selectedFiles()[0]
        if file_path:
            try:
                data_import = pd.read_csv(file_path, skiprows=[0, 15, 16, 17, 18, 19, 20])
                
                # Filtrer uniquement les colonnes 'Line' et 'Imes'
                data_import = data_import[['Line', 'Imes']]
                
                # Remplacer les valeurs vides par None
                data_import[['Line', 'Imes']] = data_import[['Line', 'Imes']].replace("", None)
                
                # Afficher les données importées
                print(data_import)
                print("Données importées avec succès.")
                
                return data_import
            except Exception as e:
                print(f"Erreur lors du traitement : {e}")
                return None
        else:
            print("Aucun fichier sélectionné.")

# Fonction pour ajuster la taille du widget de la table en fonction du contenu
def adjustTableWidgetSize(self):
    # Calculer la taille optimale de la table
    table = self.ui_main_window.table1
    row_count = table.model().rowCount()
    column_count = table.model().columnCount()

    # Ajuster la taille du widget en fonction de la taille des cellules
    table_width = 0
    table_height = 0

    for col in range(column_count):
        table_width += table.columnWidth(col)

    for row in range(row_count):
        table_height += table.rowHeight(row)

    # Ajouter des marges si nécessaire
    table_width += 30  # Pour les bords et le défilement horizontal
    table_height += 30  # Pour les bords et le défilement vertical

    # Redimensionner le widget de la table
    table.setFixedSize(table_width, table_height)

class TableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # Centrer toutes les cellules
            return Qt.AlignmentFlag.AlignCenter
            
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            # Centrer les en-têtes
            return Qt.AlignmentFlag.AlignCenter
            
        return None

    def setData(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole or role == Qt.ItemDataRole.DisplayRole:
            self._data[index.row()][index.column()] = value
            # Émet le signal que les données ont changé
            self.dataChanged.emit(index, index, [role])
            return True
        return False

    def flags(self, index):
        # Permet l'édition des cellules
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable

    def getData(self):
        # Méthode utilitaire pour récupérer toutes les données
        return self._data

    def setAllData(self, data):
        # Méthode pour mettre à jour toutes les données d'un coup
        self.beginResetModel()
        self._data = data
        self.endResetModel()