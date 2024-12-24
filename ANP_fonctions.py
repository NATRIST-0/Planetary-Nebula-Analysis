"""
Analyse Nébuleuse Planétaire _ Fonctions
"""
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt, QAbstractTableModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import pandas as pd

# Fonction pour gérer le clic sur le bouton d'importation
def import_and_make_plot(self):
    # Ouvrir une boîte de dialogue pour sélectionner un fichier
    file_dialog = QFileDialog()
    file_dialog.setNameFilters(["DAT Files (*.dat)", "All Files (*)"])
    file_dialog.setWindowTitle("Ouvrir un fichier")
    
    if file_dialog.exec():
        file_path = file_dialog.selectedFiles()[0]
        if file_path:
            try:
                # Définition du spectre
                mySpectra = pd.read_csv(file_path, sep=" ", header=None, names=['wavelength', 'intensities'])
                mySpectra = mySpectra[(mySpectra['wavelength'] >= 3800) & (mySpectra['wavelength'] <= 7600)] #keep only the values between 3800 and 7600 Å

                print("Données importées avec succès.")
                # Create the plot after successful import
                create_and_update_plot(self, mySpectra, file_path)
                return mySpectra, file_path
            except Exception as e:
                print(f"Erreur lors du traitement : {e}")
                return None
        else:
            print("Aucun fichier sélectionné.")


# Fonction pour créer et mettre à jour le graphique
def create_and_update_plot(self, mySpectra, file_path):
    self.ax.clear()
    
    wavelengths = mySpectra['wavelength']
    spectrum = mySpectra['intensities']

    # Configuration des couleurs
    clim = (3800, 7500)
    norm = plt.Normalize(*clim)
    wl = np.arange(clim[0], clim[1] + 1, 2)
    colorlist = list(zip(norm(wl), [wavelength_to_rgb(w) for w in wl]))
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
    self.ax.set_ylim(0, 0.8*max(mySpectra['intensities']))
    self.ax.tick_params(axis='both', colors='white')
    self.ax.set_title(f'Spectre de {file_path.split("/")[-1].split(".")[0]}', color = "white", size=16)
    self.figure.set_facecolor('#4C566A')

    # Remplissage de la zone sous la courbe et contour
    self.ax.fill_between(wavelengths, max(spectrum), spectrum, color="black")
    
    # Mise à jour du canvas
    self.canvas.draw()

def wavelength_to_rgb(wavelength, gamma=1):
    """Convertit une longueur d'onde (Å) en une couleur RGB approximative."""
    wavelength = float(wavelength)
    if 3800 <= wavelength <= 7500:
        A = 1.0
    else:
        A = 0.5
    wavelength = max(3800, min(wavelength, 7500))
    
    if 3800 <= wavelength <= 4400:
        attenuation = 0.3 + 0.7 * (wavelength - 3800) / (4400 - 3800)
        R = ((-(wavelength - 4400) / (4400 - 3800)) * attenuation) ** gamma
        G = 0.0
        B = (1.0 * attenuation) ** gamma
    elif 4400 <= wavelength <= 4900:
        R = 0.0
        G = ((wavelength - 4400) / (4900 - 4400)) ** gamma
        B = 1.0
    elif 4900 <= wavelength <= 5100:
        R = 0.0
        G = 1.0
        B = (-(wavelength - 5100) / (5100 - 4900)) ** gamma
    elif 510 <= wavelength <= 580:
        R = ((wavelength - 5100) / (5800 - 5100)) ** gamma
        G = 1.0
        B = 0.0
    elif 5800 <= wavelength <= 6450:
        R = 1.0
        G = (-(wavelength - 6450) / (6450 - 5800)) ** gamma
        B = 0.0
    elif 6450 <= wavelength <= 7500:
        attenuation = 0.3 + 0.7 * (7500 - wavelength) / (7500 - 6450)
        R = (1.0 * attenuation) ** gamma
        G = 0.0
        B = 0.0
    else:
        R, G, B = 0.0, 0.0, 0.0
    return (R, G, B, A)

def remplir_tableau(table1, table2, table3, data_import):  # Added table2 parameter
    if data_import is None:
        return
        
    data_Imes = data_import['Imes']
    data_Imes = data_Imes.astype(float)
    
    # Récupérer le modèle
    model1 = table1.model()
    model2 = table2.model()
    model3 = table3.model()

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

    # Put cHβ in table2
    index_chb = model3.index(0, 0)  # Row 0, Column 0
    model3.setData(index_chb, f"{cHβ:.3f}", Qt.ItemDataRole.DisplayRole)
    
    # Put cHβ/1.46 in table2
    index_evb = model3.index(0, 1)  # Row 1, Column 0
    model3.setData(index_evb, f"{cHβ/1.46:.3f}", Qt.ItemDataRole.DisplayRole)

    # Valeur mesuré dans table2
    indexv_mes1 = model2.index(0, 2)  # Colonne 2 pour 'Valeur mesurée'
    HI1 = float(model1.index(9, 3).data() or 0) / 100
    model2.setData(indexv_mes1, f"{HI1:.3f}", Qt.ItemDataRole.DisplayRole)

    indexv_mes2 = model2.index(2, 2)  # Colonne 2 pour 'Valeur mesurée'
    HI2 = float(model1.index(0, 3).data() or 0) / 100
    model2.setData(indexv_mes2, f"{HI2:.3f}", Qt.ItemDataRole.DisplayRole)

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

    # Step 4: Update the model with the calculated rebleuïssement
    index_rebleuie1 = model2.index(0, 4)
    rebleuie1 = float(model1.index(9, 4).data()) / 100
    model2.setData(index_rebleuie1, f"{rebleuie1:.3f}", Qt.ItemDataRole.DisplayRole)

    
    index_rebleuie2 = model2.index(2, 4)
    rebleuie2 = float(model1.index(0, 4).data()) / 100
    model2.setData(index_rebleuie2, f"{rebleuie2:.3f}", Qt.ItemDataRole.DisplayRole)

    # Ajout des rapports de lambda 5 4      4 4 
    index_lambda1 = model3.index(0, 2)
    lambda1 = float(model1.index(5, 4).data()) / float(model1.index(4, 4).data())
    model3.setData(index_lambda1, f"{lambda1:.3f}", Qt.ItemDataRole.DisplayRole)

    index_lambda2 = model3.index(0, 3)
    lambda2 = float(model1.index(10, 4).data()) / float(model1.index(8, 4).data())
    model3.setData(index_lambda2, f"{lambda2:.3f}", Qt.ItemDataRole.DisplayRole)

    index_lambda3 = model3.index(0, 4)
    lambda3 = float(model1.index(10, 4).data()) / float(model1.index(9, 4).data())
    model3.setData(index_lambda3, f"{lambda3:.3f}", Qt.ItemDataRole.DisplayRole)

    return table1


# Fonction pour gérer le clic sur le bouton d'importation
def on_pushButton_import1_clicked():
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
                # print(data_import)
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
