"""
Analyse Nébuleuse Planétaire _ Fonctions
"""
import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt6.QtCore import Qt, QAbstractTableModel
import pandas as pd
import numpy as np

def remplir_tableau(table1, data_import):
    if data_import is None:
        return
        
    data_Imes = data_import['Imes']
    data_Imes = data_Imes.astype(float)
    
    # Récupérer le modèle
    model1 = table1.model()

    
    # Step 1: Populate the necessary data in the model
    for i in range(len(data_Imes)):
        index2 = model1.index(i, 2)  # Colonne 2 pour 'I₀Gauss'
        model1.setData(index2, str(data_Imes[i]), Qt.ItemDataRole.DisplayRole)

        index3 = model1.index(i, 3)  # Colonne 3 pour 'I₀/I(Hβ)=100'
        rapport_I = data_Imes[i] / data_Imes[3] * 100
        model1.setData(index3, f"{rapport_I:.1f}", Qt.ItemDataRole.DisplayRole)

    # Step 2: Calculate cHβ
    try:
        index = model1.index(9, 3)
        if index.isValid():
            data = index.data()
            if data:
                cHβ = 3.08 * np.log10(float(data)) - 7.55
            else:
                raise ValueError("No data in cell")
        else:
            raise ValueError("Invalid index")
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
        cHβ = 3.08 * np.log10(1) - 7.55

    # Step 3: Update the model with the calculated cHβ
    for i in range(len(data_Imes)):
        index3 = model1.index(i, 3)
        rapport_I_row = float(index3.data()) if index3.data() else 0
        
        index4 = model1.index(i, 4)  # Colonne 4 pour 'I_c'
        wavelength = model1.index(i, 0).data()
        wavelength = float(wavelength) if wavelength else 0
        
        f_lambda = 2.5634 * (wavelength/10000)**2 - 4.873 * (wavelength/10000) + 1.7636
        I_c = rapport_I_row * 10**(cHβ * f_lambda)
        
        model1.setData(index4, f"{I_c:.1f}", Qt.ItemDataRole.DisplayRole)

        index5 = model1.index(i, 5)  # Colonne 5 pour 'Δ%'
        model1.setData(index5, f"{(rapport_I_row - I_c) / I_c * 100:.0f}", Qt.ItemDataRole.DisplayRole)

        table1.resizeColumnsToContents()

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
                data_import[['Line', 'Imes']] = data_import[['Line', 'Imes']].replace(" ", None)
                
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
def adjustTableWidgetSize(table):
    # Calculer la taille optimale de la table
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
    table_width += 10  # Pour les bords et le défilement horizontal
    table_height += 50  # Pour les bords et le défilement vertical

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

def theme(self):
    self.setStyleSheet("""
        QWidget {
            background-color: #2E3440;
            color: #D8DEE9;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QPushButton {
            background-color: #4C566A;
            border-radius: 5px;
            padding: 5px 10px;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #81A1C1;
        }
        QTableWidget {
            background-color: #3B4252;
            color: #D8DEE9;
            gridline-color: #4C566A;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QTableWidget::item {
            padding: 5px;
        }
        QTableWidget::item:selected {
            background-color: #FFC107;
        }
        QHeaderView::section:horizontal {
            gridline-color: #4C566A;        
            padding: 5px;
            background-color: #4C566A;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
        QHeaderView::section:horizontal:checked {
            background-color: #5E81AC;
        }
        QHeaderView::section:horizontal:pressed {
            background-color: #81A1C1;
        }
        QToolTip {
            background-color: #4C566A;
            color: #D8DEE9;
            border: 1px solid #D8DEE9;
            font-family: 'Segoe UI';
            font-size: 12px;
        }
    """)
from PyQt6.QtGui import QColor

class TableModelTooltips(TableModel):
    def __init__(self, data, headers, tooltips):
        super().__init__(data, headers)
        self._tooltips = tooltips

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section]
            elif role == Qt.ItemDataRole.ToolTipRole:
                return self._tooltips[section]
        return None

class TableModelColors(TableModel):
    def __init__(self, data, headers):
        super().__init__(data, headers)
        self.index_colors = [
            QColor(68, 67, 255),    # 4340,47 Å - Bleu clair
            QColor(64, 63, 255),    # 4363,21 Å - Bleu clair
            QColor(12, 92, 255),    # 4685,68 Å - Bleu
            QColor(0, 156, 255),    # 4861,33 Å - Bleu clair
            QColor(0, 209, 255),    # 4958,92 Å - Bleu clair
            QColor(0, 255, 255),    # 5006,85 Å - Cyan
            QColor(255, 204, 0),    # 5754,57 Å - Jaune-orange
            QColor(255, 190, 0),    # 5875,65 Å - Jaune
            QColor(255, 73, 0),     # 6548,06 Å - Orange
            QColor(255, 0, 0),      # 6562,82 Å - Rouge
            QColor(255, 0, 0),      # 6583,39 Å - Rouge
            QColor(255, 0, 0),      # 6716,5 Å - Rouge
            QColor(255, 0, 0)       # 6730,7 Å - Rouge
        ]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section]
        elif orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return str("")
            if role == Qt.ItemDataRole.BackgroundRole:
                return self.index_colors[section % len(self.index_colors)]
        return None
    
class TableModelTooltipsWithColors(TableModel):
    def __init__(self, data, headers, tooltips):
        super().__init__(data, headers)
        self._tooltips = tooltips
        self._headers = headers
        self._data = data

        self.index_colors = [
            QColor(68, 67, 255),    # 4340,47 Å - Bleu clair
            QColor(64, 63, 255),    # 4363,21 Å - Bleu clair
            QColor(12, 92, 255),    # 4685,68 Å - Bleu
            QColor(0, 156, 255),    # 4861,33 Å - Bleu clair
            QColor(0, 209, 255),    # 4958,92 Å - Bleu clair
            QColor(0, 255, 255),    # 5006,85 Å - Cyan
            QColor(255, 204, 0),    # 5754,57 Å - Jaune-orange
            QColor(255, 190, 0),    # 5875,65 Å - Jaune
            QColor(255, 73, 0),     # 6548,06 Å - Orange
            QColor(255, 0, 0),      # 6562,82 Å - Rouge
            QColor(255, 0, 0),      # 6583,39 Å - Rouge
            QColor(255, 0, 0),      # 6716,5 Å - Rouge
            QColor(255, 0, 0)       # 6730,7 Å - Rouge
        ]

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section]
            elif role == Qt.ItemDataRole.ToolTipRole:
                return self._tooltips[section]
        elif orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return str("")
            if role == Qt.ItemDataRole.BackgroundRole:
                return self.index_colors[section % len(self.index_colors)]
        return None
