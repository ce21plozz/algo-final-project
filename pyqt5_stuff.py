import random
import sys

import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,
                             QPushButton,QHBoxLayout,QVBoxLayout,QLineEdit)
from PyQt5.QtCore import Qt#ngasih Qt.AlignCenter, Qt.AlignLeft, dsb
from PyQt5.QtGui import QFont,QIcon # Arial, Calibri, Times New Roman, Segoe UI, Consolas, Courier New, Verdana, Tahoma, Georgia, Cambria, Impact, Trebuchet MS, Comic Sans MS

headers = {
    "X-CSCAPI-KEY" : 'feae7cb3a129d6a50aa0c03d76fffa78af67892de06c95d31d3dd23d9e397ab6'
}
respon = requests.get(f'https://api.countrystatecity.in/v1/countries', headers=headers)
hasil = respon.json()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Very cool example window!")
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.setGeometry(650, 300, 700, 400)
        self.setFixedSize(825, 600)
        self.setStyleSheet("""
                            background: qlineargradient(
                            x1:0, y1:0,
                            x2:0, y2:1,
                            stop:0 #279ACC,
                            stop:1 #095575);
                            """)
        #User interfaces ---
        self.label = QLabel("Kamus Negara Seluruh Dunia", self)
        self.button = QPushButton("Lihat info negara",self)
        self.button_randomize = QPushButton("Info negara acak", self)
        self.button.clicked.connect(lambda: self.give_result("normal"))
        self.button_randomize.clicked.connect(lambda: self.give_result("random"))
        self.userinput = QLineEdit(self)

        self.vbox = QVBoxLayout(self)
        self.hbox = QHBoxLayout(self)

        self.vbox.setContentsMargins(0,0,0,0)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.userinput, alignment=Qt.AlignCenter)
        self.hbox.addWidget(self.button, alignment=Qt.AlignCenter)
        self.hbox.addWidget(self.button_randomize, alignment=Qt.AlignCenter)
        self.vbox.addLayout(self.hbox)

        self.country_name = QLabel("", self)
        self.capital = QLabel("",self)
        self.currency_name = QLabel("",self)
        self.phone_code = QLabel("",self)
        self.nationality = QLabel("",self)
        self.population = QLabel("",self)
        # ------------------

        self.initUI()

    def initUI(self):
        #result styling
        for info in [self.country_name, self.capital, self.currency_name, self.phone_code, self.nationality, self.population]:
            if info is self.country_name and not self.country_name.text() == "":
                info.setFont(QFont("Impact", 25))
            elif info is self.capital and len(self.capital.text()) > 50:
                info.setFont(QFont("Georgia", 15))
            else:
                info.setFont(QFont("georgia", 20))
            info.setStyleSheet("""
                                background-color: transparent;
                            """)
            self.vbox.addWidget(info, alignment=Qt.AlignCenter)

        # label
        self.label.setGeometry(0, 0, 700, 70) #
        self.label.setFont(QFont("tahoma", 30))
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
                            font-weight: bold;
                            border-bottom: 5px solid #31695e;
                            background-color: #27CCAC;
                            height: 100px;
                            """)
        #Layouts


        # button
        for tombol in [self.button, self.button_randomize]:
            tombol.setFont(QFont("verdana", 15))
            tombol.setGeometry(0,0,200,35)
            tombol.setObjectName("search-btn")
            tombol.setObjectName("search-btn")
            tombol.setContentsMargins(150, 0, 20, 0)
            tombol.setFixedSize(325, 40)
            tombol.setStyleSheet("""
                                        #search-btn {
                                            background-color: #27CC59;
                                            border-radius: 18px;
                                            border: 2px solid black;
                                            padding: 5px;
                                        }
                                        #search-btn:hover {
                                            padding: 1px;
                                            background-color: #067528;
                                            border-radius: 18px;
                                            border: 2px solid black;
                                        }
                                        #search-btn:pressed {
                                            padding: 1px;
                                            background-color: #66e38c;
                                            border-radius: 18px;
                                            border: 2px solid black;
                                        }
                                        
                                        """)


        #userinput
        self.userinput.setFont(QFont("verdana", 15))
        self.userinput.setObjectName("search-input")
        self.userinput.setFixedSize(550,40)
        self.userinput.setStyleSheet("""
                                    #search-input {
                                        background-color: lightgrey;
                                        border: 2px solid black;
                                        border-radius: 15px;
                                        padding: 4px;
                                    }
                                    #search-input:hover {
                                        background-color: white;
                                    }
                                    
                                    """)
        self.userinput.setPlaceholderText("Masukkan nama negara (bahasa Inggris)")

        #results
    def give_result(self, search_type):
        if search_type == "normal":
            countryname = self.userinput.text()
        elif search_type == "random":
            selected_country = random.choice(hasil)
            countryname = selected_country["name"]

        if not countryname:
            return [interface.setText("Inputmu kosong") if interface is self.country_name else interface.setText("") for interface in [self.country_name, self.capital, self.currency_name, self.phone_code, self.nationality, self.population] ], self.initUI()
        elif len(countryname) < 4:
            return [interface.setText("Inputmu terlalu pendek") if interface is self.country_name else interface.setText("") for interface in [self.country_name, self.capital, self.currency_name, self.phone_code, self.nationality, self.population] ], self.initUI()
        elif len(countryname) >= 50:
            return [interface.setText("Inputmu terlau panjang") if interface is self.country_name else interface.setText("") for interface in [self.country_name, self.capital, self.currency_name, self.phone_code, self.nationality, self.population] ], self.initUI()
        iso2 = None
        is_valid = list()
        valid_country_name = list()
        for data in hasil:
            if countryname.lower() in data["name"].lower():
                is_valid.append(data)
                valid_country_name.append(data["name"])
        if search_type == "random" or search_type == "normal":
            is_valid = [random.choice(is_valid)]

        if len(is_valid) == 0:
            return [interface.setText("Negara tersebut ga ditemukan") if interface is self.country_name else interface.setText("") for interface in [self.country_name, self.capital, self.currency_name, self.phone_code, self.nationality, self.population] ], self.initUI()

        elif len(is_valid) == 1: #biar input ambigu ga dikasih hasil yang random (kalau ada nama negara yang sama)
            iso2 = is_valid[0]["iso2"]
        else:
            negara_errormsg = ", ".join(list(valid_country_name[0:3]))
            if len(valid_country_name) > 2:
                negara_errormsg += " dan lain-lainya"
            return [interface.setText(
                "Nama Negara Kurang spesifik") if interface is self.country_name else interface.setText("") for
                    interface in
                    [self.country_name, self.capital, self.currency_name, self.phone_code, self.nationality,
                     self.population]], self.capital.setText(f"ada ( {negara_errormsg} )"), self.initUI()


        try:
            self.respon2 = requests.get(f'https://api.countrystatecity.in/v1/countries/{iso2}', headers=headers)
            countrydetails = self.respon2.json()
            capital = countrydetails.get("capital")
            currency_name = countrydetails.get("currency_name", "N/A")
            phone_code = countrydetails.get("phonecode", "N/A")
            nationality = countrydetails.get("nationality", "N/A")
            population = countrydetails.get("population", "N/A")
            name = countrydetails.get("name", "N/A")

            for thing in [[self.country_name,"Nama Negara", name],
                          [self.capital,"Ibu Kota", capital],
                          [self.currency_name,"Mata Uang", currency_name],
                          [self.phone_code,"Kode Telpon Negara" , phone_code],
                          [self.nationality,"Kebangsaan/Nationality", nationality],
                          [self.population,"Populasi", population]]:
                if thing[2] == "":
                    thing[2] = "N/A"
                thing[0].setText(f"{thing[1]} : {thing[2]}")
            self.initUI()

        except Exception as e:
            self.country_name.setText(f"Kena error: {e}")




def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()