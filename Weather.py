import sys
import requests as rq
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt 

class Weather_App(QWidget):
    def __init__(self):
        super().__init__()
        self.cityLabel = QLabel("Enter city name: ", self)
        self.cityInput = QLineEdit(self)
        self.getWeatherButton = QPushButton("Get Weather", self)
        self.temperatureLabel = QLabel(self)
        self.emojiLabel = QLabel(self)
        self.descriptionLabel = QLabel( self)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(self.cityLabel)
        vbox.addWidget(self.cityInput)
        vbox.addWidget(self.getWeatherButton)
        vbox.addWidget(self.temperatureLabel)
        vbox.addWidget(self.emojiLabel)
        vbox.addWidget(self.descriptionLabel)
        
        self.setLayout(vbox)
        
        self.cityLabel.setAlignment(Qt.AlignCenter)
        self.cityInput.setAlignment(Qt.AlignCenter)
        self.temperatureLabel.setAlignment(Qt.AlignCenter)
        self.emojiLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        
        self.cityLabel.setObjectName("cityLabel")
        self.cityInput.setObjectName("cityInput")
        self.getWeatherButton.setObjectName("getWeatherButton")
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.emojiLabel.setObjectName("emojiLabel")
        self.descriptionLabel.setObjectName("descriptionLabel")
        
        self.setStyleSheet(""" 
            Qlabel, QPushButton{
                font-family: calibri;
            }
            QLabel#cityLabel{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#cityInput{
                font-size: 40px;
            }
            QPushButton#getWeatherButton{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperatureLabel{
                font-size: 75px;
            }
            QLabel#emojiLabel{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#descriptionLabel{
                font-size: 50px;
            }
        """)

        self.getWeatherButton.clicked.connect(self.getWeather)

    def getWeather(self):
        apiKey = "2da558efa8667bda8de5239eaaa42994"
        city = self.cityInput.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}"

        try:
            response = rq.get(url)
            response.raise_for_status()
            data = response.json()
        
            if data["cod"] == 200:
                self.displayWeather(data)
                
        except rq.exceptions.HTTPError as httpError:
            match response.status_code:
                case 400:
                    self.displayError("Bad request:\nPlease check your input")
                case 401:
                    self.displayError("Unauthorized:\nInvalid API key")
                case 403:
                    self.displayError("Forbidden:\nAccess is denied")
                case 404:
                    self.displayError("Not found:\nCity not found")
                case 500:
                    self.displayError("Internal Server Error:\nPlease try again later")
                case 502:
                    self.displayError("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.displayError("Service Unavailable:\nService is down")
                case 504:
                    self.displayError("Gateway Timeout:\nNo response from the server")
                case _:
                    self.displayError(f"HTTP error occured:\n{httpError}")

        except rq.exceptions.ConnectionError:
            self.displayError("Connection Error:\nCheck your internet connection") 
        except rq.exceptions.Timeout:
            self.displayError("Timeout Error:\nThe request timed out") 
        except rq.exceptions.TooManyRedirects:
            self.displayError("Too many Redirects:\nCheck the URL") 
        except rq.exceptions.RequestException as reqError:
            self.displayError(f"Request Error:\n{reqError}") 
        
        
    def displayError(self, message):
        self.temperatureLabel.setStyleSheet("font-size: 30px") 
        self.temperatureLabel.setText(message) 
        self.emojiLabel.clear()
        self.descriptionLabel.clear()
    
    def displayWeather(self, data):
        self.temperatureLabel.setStyleSheet("font-size: 75px") 
        temperatureK = data["main"]["temp"]
        temperatureF = (temperatureK * 9/5) - 459.67
        weatherID = data["weather"][0]["id"] 
        weatherDescription = data["weather"][0]["description"] 
               
        self.temperatureLabel.setText(f"{temperatureF:.1f}°F") 
        self.emojiLabel.setText(self.getWeatherEmoji(weatherID))
        self.descriptionLabel.setText(weatherDescription)

    @staticmethod    
    def getWeatherEmoji(weatherID):
        if 200 <= weatherID <= 232:
            return "⛈️"
        elif 300 <= weatherID <= 321:
            return "🌦️"
        elif 500 <= weatherID <= 531:
            return "🌧️"
        elif 600 <= weatherID <= 622:
            return "❄️"
        elif 701 <= weatherID <= 741:
            return "🌫️"
        elif weatherID == 762:
            return "🌋"
        elif weatherID == 771:
            return "💨"
        elif weatherID == 781:
            return "🌪️"
        elif weatherID == 800:
            return "☀️"
        elif 801 <= weatherID <= 804:
            return "☁️"
        else:
            return ""
            
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherApp = Weather_App()
    weatherApp.show()
    sys.exit(app.exec_())
     
 
