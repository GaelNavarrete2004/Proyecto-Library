from email.message import EmailMessage
import subprocess
from cryptography.fernet import Fernet, InvalidToken
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, 
                             QLineEdit, QLabel, QDialog, QDesktopWidget, 

                             QMessageBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QComboBox, QHBoxLayout, QDoubleSpinBox, QTextEdit)

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from datetime import datetime, timedelta
import json, os, ssl, smtplib, sys, re, mariadb
from Database import conectar

# Datos para enviar correos electrónicos
password = "gvqr gzpl irqn mqzk"            # Contraseña de app generada para el correo electrónico
                                            # No debería estar aquí, pero es necesario para enviar correos electrónicos
                                            # Y es una cuenta de correo propia para pruebas (Pueden usar dotenv para ocultarla)
                                            # Creen una cuenta de correo para la app y generen una contraseña de app
                                            # Para crear una contraseña de app, vayan a https://myaccount.google.com/u/0/apppasswords
                                            # Ocupan activar la verificación en dos pasos para poder generar una contraseña de app
                                            # La contraseña de app solo se puede ver una vez, así que guárdenla en un lugar seguro
                                            # Si les sirve, pueden usar la cuenta de correo que puse aquí, pero así no tendrán acceso
                                            # Yo ví este video para hacerlo: https://www.youtube.com/watch?v=oPAo8Hh8bj0
                                            # No vayan a dejar estos comentarios en su código, es solo para que sepan cómo hacerlo xd

email_sender = "librarypy2024@gmail.com"    # Correo electrónico del remitente
email_reciver = " "                         # Correo electrónico del destinatario
email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'   # Expresión regular para validar correos electrónicos
subject = " "                               # Asunto del correo
body = " "                                  # Cuerpo del correo

# Versión de la aplicación
version = "2.0.1"

# Obtiene el directorio del script
script_dir = os.path.dirname(__file__)  

# Obtiene el directorio de la aplicación
appdata = os.environ["APPDATA"]
directorio_libreria = os.path.join(appdata, "LibraryPy")

# Abre el directorio de la librería, se los dejo por si quieren usarlo para saber dónde se guardan los archivos
# No es necesario para la aplicación, pero puede ser útil para que sepan dónde se guardan los archivos
# Básicamente, el directorio es C:\Users\Usuario\AppData\Roaming\LibraryPy
def abrir_directorio():
    if os.path.exists(directorio_libreria):
        subprocess.Popen(['explorer', directorio_libreria])
            
    else:
        print(f"El directorio {directorio_libreria} no existe.")

# Quitar comentario para abrir el directorio
# abrir_directorio()

class VentanaCalificar(QDialog):
    def __init__(self, id_libro, titulo_libro, account_id, parent=None):
        super().__init__(parent)
        self.id_libro = id_libro
        self.titulo_libro = titulo_libro
        self.account_id = account_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Calificar libro")
        self.setFixedSize(500, 250)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # Aplicamos un nuevo estilo CSS
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #dac8ae, stop:1 #eae1d0);
                color: #111111;
                font-family: 'Arial', sans-serif;
                font-size: 14px;
            }

            QPushButton {
                background-color: #EFDECD;
                color: #1A1110;
                border: 2px solid #1A1110;
                border-radius: 8px;
                padding: 8px;
                transition: background-color 0.3s ease;
            }

            QPushButton:hover {
                background-color: #CC7722;
                border-color: #8B4513;
            }

            QLineEdit, QDoubleSpinBox {
                background-color: #FFFFFF;
                color: #111111;
                border: 2px solid #00416A;
                padding: 6px;
                border-radius: 5px;
            }

            QLabel {
                color: #1A1110;
                font-weight: bold;
                margin-bottom: 5px;
            }
        """)

        # Añadimos los elementos visuales
        self.labelTitulo = QLabel(self)
        self.labelTitulo.setText(f"Libro: {self.titulo_libro}")
        self.labelTitulo.setAlignment(Qt.AlignCenter)

        self.labelCalificacion = QLabel(self)
        self.labelCalificacion.setText("Calificación (0.0 - 5.0):")

        # Cambiamos QComboBox por QDoubleSpinBox para permitir decimales
        self.spinCalificacion = QDoubleSpinBox(self)
        self.spinCalificacion.setRange(0.0, 5.0)  # Rango entre 0.0 y 5.0
        self.spinCalificacion.setSingleStep(0.1)  # Incrementos de 0.1
        self.spinCalificacion.setDecimals(1)  # Mostrar solo un decimal
        
        self.labelReseña = QLabel(self)
        self.labelReseña.setText("Escribe una reseña:")

        # Campo para escribir la reseña
        self.textReseña = QTextEdit(self)
        self.textReseña.setPlaceholderText("Escribe tu reseña aquí...")

        # Mejoramos el botón "Calificar"
        self.btnCalificar = QPushButton("Calificar y Reseñar", self)
        self.btnCalificar.setIcon(QIcon("icono_calificar.png"))  # Agrega un ícono si lo deseas
        self.btnCalificar.setCursor(Qt.PointingHandCursor)
        self.btnCalificar.clicked.connect(self.calificar)

        # Disposición y espaciado
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(self.labelTitulo)
        layout.addWidget(self.labelCalificacion)
        layout.addWidget(self.spinCalificacion)
        layout.addWidget(self.labelReseña)
        layout.addWidget(self.textReseña)  # Añadir el campo de texto para la reseña
        layout.addWidget(self.btnCalificar)

        self.setLayout(layout)
        self.center()

    def center(self):
        """Centrar la ventana en la pantalla."""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def calificar(self):
        """Función para calificar el libro."""
        calificacion = self.spinCalificacion.value()  # Obtener el valor decimal del QDoubleSpinBox
        reseña = self.textReseña.toPlainText()
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()

                # 1. Insertar la calificación del usuario en la tabla 'calificaciones'
                cursor.execute(
                    "INSERT INTO calificaciones (id_usuario, id_libro, calificacion, reseña) VALUES (?, ?, ?, ?)",
                    ( self.id_libro, self.account_id, calificacion, reseña)  # Cambié el orden aquí
                )
                conn.commit()

                # 2. Calcular el promedio de las calificaciones de este libro
                cursor.execute("SELECT AVG(calificacion) FROM calificaciones WHERE id_libro = ?", (self.account_id,))
                promedio_calificacion = cursor.fetchone()[0]

                # 3. Actualizar el campo 'calificacion' en la tabla 'libros' con el nuevo promedio
                cursor.execute("UPDATE libro SET calificacion = ? WHERE id = ?", (promedio_calificacion, self.account_id))
                conn.commit()

                # Mostrar un mensaje de éxito
                QtWidgets.QMessageBox.information(self, "Calificación y Reseña", "Calificación realizada con éxito.")
                self.accept()

            except mariadb.Error as e:
                print(f"Error al calificar el libro: {e}")
            finally:
                conn.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")

        





class VentanaPago(QDialog):
    def __init__(self, account_id, credit, account_email, main_window):
        super().__init__()
        self.credit = credit
        self.account_id = account_id
        self.account_email = account_email
        self.main_window = main_window  # Almacena la referencia a la ventana principal
        self.sancion_aplicada = False
        self.init_ui()

    def init_ui(self):
        # Título de la ventana
        self.setWindowTitle("Pagar")
        # Tamaño fijo de la ventana
        self.setFixedSize(500, 500)
        # Quitar el botón de ayuda
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # Aplica la hoja de estilo a la ventana
        self.setStyleSheet("""
            QWidget {
                background-color: #DAC8AE;
                color: #111111;
            }

            /* Estilo para los botones */
            QPushButton {
                background-color: #EFDECD;
                color: #1A1110;
                border: 2px solid #1A1110;
                padding: 5px;
            }

            QPushButton:hover {
                background-color: #CC7722;
            }

            /* Estilo para los cuadros de texto */
            QLineEdit {
                background-color: #FFFFFF;
                color: #111111;
                border: 1px solid #00416A;
                padding: 4px;
            }

            QLineEdit:focus {
                border: 2px solid #00416A;
            }

            /* Estilo para las etiquetas */
            QLabel {
                color: #1A1110;
            }
        """)
        # Saldo pendiente
        self.labelCredit = QLabel(self)
        self.labelCredit.setText(f"Saldo pendiente: ${self.credit}")
        # Etiqueta para nombre del beneficiario
        self.labelNombre = QLabel(self)
        self.labelNombre.setText("Nombre del beneficiario:")
        self.inputNombre = QLineEdit(self)

        # Etiqueta para numero de tarjeta
        self.labelTarjeta = QLabel(self)
        self.labelTarjeta.setText("Número de tarjeta:")
        self.inputTarjeta = QLineEdit(self)
        self.inputTarjeta.setInputMask("9999-9999-9999-9999")
        
        # Selector de mes
        self.labelMes = QLabel(self)
        self.labelMes.setText("Mes de vencimiento:")
        self.comboMes = QComboBox(self)
        self.comboMes.addItems(["01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril", "05 - Mayo", "06 - Junio",
                                "07 - Julio", "08 - Agosto", "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"])

        # Selector de año
        self.labelAño = QLabel(self)
        self.labelAño.setText("Año de vencimiento:")
        self.comboAño = QComboBox(self)
        current_year = datetime.now().year
        self.comboAño.addItems([str(año) for año in range(current_year, current_year+15)])

        # Iconos de Visa y Mastercard
        
        image_visa = os.path.join(script_dir, "imagenes/visa.png")
        image_master = os.path.join(script_dir, "imagenes/mastercard.png")
        pixmap_visa = QPixmap(image_visa)
        pixmap_mastercard = QPixmap(image_master)
        self.labelVisa = QLabel(self)
        self.labelVisa.setPixmap(pixmap_visa.scaledToHeight(30))
        self.labelVisa.setAlignment(Qt.AlignCenter)
        self.labelVisa.setScaledContents(True)
        self.labelMastercard = QLabel(self)
        self.labelMastercard.setPixmap(pixmap_mastercard.scaledToHeight(30))
        self.labelMastercard.setAlignment(Qt.AlignCenter)
        self.labelMastercard.setScaledContents(True)

        # Layout para los iconos
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.labelVisa)
        icon_layout.addWidget(self.labelMastercard)
        icon_layout.setAlignment(Qt.AlignCenter)

        self.btnPay = QPushButton("Pagar", self)
        self.btnPay.clicked.connect(self.pay)

        layout = QVBoxLayout()
        layout.addLayout(icon_layout)
        layout.addWidget(self.labelCredit)
        layout.addWidget(self.labelNombre)
        layout.addWidget(self.inputNombre)
        layout.addWidget(self.labelTarjeta)
        layout.addWidget(self.inputTarjeta)
        layout.addWidget(self.labelMes)
        layout.addWidget(self.comboMes)
        layout.addWidget(self.labelAño)
        layout.addWidget(self.comboAño)
        layout.addWidget(self.btnPay)

        self.setLayout(layout)
        self.center()


    def init_ui2(self):
        # Título de la ventana
        self.setWindowTitle("Pagar")
        # Tamaño fijo de la ventana
        self.setFixedSize(500, 500)
        # Quitar el botón de ayuda
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # Aplica la hoja de estilo a la ventana
        self.setStyleSheet("""
            QWidget {
                background-color: #DAC8AE;
                color: #111111;
            }

            /* Estilo para los botones */
            QPushButton {
                background-color: #EFDECD;
                color: #1A1110;
                border: 2px solid #1A1110;
                padding: 5px;
            }

            QPushButton:hover {
                background-color: #CC7722;
            }

            /* Estilo para los cuadros de texto */
            QLineEdit {
                background-color: #FFFFFF;
                color: #111111;
                border: 1px solid #00416A;
                padding: 4px;
            }

            QLineEdit:focus {
                border: 2px solid #00416A;
            }

            /* Estilo para las etiquetas */
            QLabel {
                color: #1A1110;
            }
        """)
        # Saldo pendiente
        self.labelCredit = QLabel(self)
        self.labelCredit.setText(f"Costo del libro: ${self.credit}")
        # Etiqueta para nombre del beneficiario
        self.labelNombre = QLabel(self)
        self.labelNombre.setText("Nombre del beneficiario:")
        self.inputNombre = QLineEdit(self)

        # Etiqueta para numero de tarjeta
        self.labelTarjeta = QLabel(self)
        self.labelTarjeta.setText("Número de tarjeta:")
        self.inputTarjeta = QLineEdit(self)
        self.inputTarjeta.setInputMask("9999-9999-9999-9999")
        
        # Selector de mes
        self.labelMes = QLabel(self)
        self.labelMes.setText("Mes de vencimiento:")
        self.comboMes = QComboBox(self)
        self.comboMes.addItems(["01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril", "05 - Mayo", "06 - Junio",
                                "07 - Julio", "08 - Agosto", "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"])

        # Selector de año
        self.labelAño = QLabel(self)
        self.labelAño.setText("Año de vencimiento:")
        self.comboAño = QComboBox(self)
        current_year = datetime.now().year
        self.comboAño.addItems([str(año) for año in range(current_year, current_year+15)])

        # Iconos de Visa y Mastercard
        
        image_visa = os.path.join(script_dir, "imagenes/visa.png")
        image_master = os.path.join(script_dir, "imagenes/mastercard.png")
        pixmap_visa = QPixmap(image_visa)
        pixmap_mastercard = QPixmap(image_master)
        self.labelVisa = QLabel(self)
        self.labelVisa.setPixmap(pixmap_visa.scaledToHeight(30))
        self.labelVisa.setAlignment(Qt.AlignCenter)
        self.labelVisa.setScaledContents(True)
        self.labelMastercard = QLabel(self)
        self.labelMastercard.setPixmap(pixmap_mastercard.scaledToHeight(30))
        self.labelMastercard.setAlignment(Qt.AlignCenter)
        self.labelMastercard.setScaledContents(True)

        # Layout para los iconos
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.labelVisa)
        icon_layout.addWidget(self.labelMastercard)
        icon_layout.setAlignment(Qt.AlignCenter)

        self.btnPay = QPushButton("Pagar", self)
        self.btnPay.clicked.connect(self.payBook)

        layout = QVBoxLayout()
        layout.addLayout(icon_layout)
        layout.addWidget(self.labelCredit)
        layout.addWidget(self.labelNombre)
        layout.addWidget(self.inputNombre)
        layout.addWidget(self.labelTarjeta)
        layout.addWidget(self.inputTarjeta)
        layout.addWidget(self.labelMes)
        layout.addWidget(self.comboMes)
        layout.addWidget(self.labelAño)
        layout.addWidget(self.comboAño)
        layout.addWidget(self.btnPay)

        self.setLayout(layout)
        self.center()


    def center(self):
        # Obtenemos la geometría de la ventana principal
        qr = self.frameGeometry()
        # Obtenemos la posición central de la pantalla
        cp = QDesktopWidget().availableGeometry().center()
        # Movemos la ventana al centro de la pantalla
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def luhn_check(self, tarjeta):

        tarjeta = tarjeta.replace("-", "")
        tarjeta = tarjeta.replace(" ", "")

        digits = [int(d) for d in tarjeta]
   
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9

        checksum = sum(digits)

        return checksum % 10 == 0

    def payBook(self):
        # Obtener los datos ingresados por el usuario
        nombre = self.inputNombre.text()
        tarjeta = self.inputTarjeta.text().replace(" ", "")
        # Verificar si el nombre es válido
        if not nombre:
            QtWidgets.QMessageBox.critical(None, "Error", "Por favor, ingrese el nombre del beneficiario.")
            return
        # Verificar si la tarjeta es válida (solo números y longitud de 16)
        if not re.match("^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$", tarjeta):
            QtWidgets.QMessageBox.critical(None, "Error", "Número de tarjeta inválido.")
            return
        # Validar el número de la tarjeta utilizando el algoritmo de Luhn
        if not self.luhn_check(tarjeta):
            QtWidgets.QMessageBox.critical(None, "Error", "Número de tarjeta inválido según la verificación de Luhn.")
            return

        # Cerrar la ventana de pago
        self.accept()

        return True
    
    def pay(self):
        if self.credit == 0:
            QtWidgets.QMessageBox.information(None, "Saldo pendiente", "Actualmente no tienes saldo pendiente por pagar.")
            return
        else:
            ventana_pago = VentanaPago(self.account_id, self.credit, self.account_email, self.main_window)
            ventana_pago.exec_()
             # Verificar la bandera antes de llamar a sancionar_usuarios
            if not self.sancion_aplicada:
                ventana_pago.sancionar_usuarios()
                self.sancion_aplicada = True  # Actualizar la bandera después de llamar a sancionar_usuarios
            
        # Obtener los datos ingresados por el usuario
        nombre = self.inputNombre.text()
        tarjeta = self.inputTarjeta.text().replace(" ", "")
        mes_vencimiento = self.comboMes.currentText()
        año_vencimiento = self.comboAño.currentText()
        # Verificar si el nombre es válido
        # Verificar si la tarjeta es válida (solo números y longitud de 16)
        if not re.match("^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{4}$", tarjeta):
            QtWidgets.QMessageBox.critical(None, "Error", "Número de tarjeta inválido.")
            return
        # Validar el número de la tarjeta utilizando el algoritmo de Luhn
        if not self.luhn_check(tarjeta):
            QtWidgets.QMessageBox.critical(None, "Error", "Número de tarjeta inválido según la verificación de Luhn.")
            return
        # Realizar el pago y actualizar la base de datos
        conn = conectar()
        if conn:
            try:
                cursor = conn.cursor()
                # Realizar el pago y actualizar el crédito del usuario
                cursor.execute("UPDATE usuarios SET credit = 0, cuenta_cancelada = 1, multa = 0 WHERE id = ?", (self.account_id,))
                conn.commit()
                QtWidgets.QMessageBox.information(None, "Pago exitoso", "El pago se ha realizado con éxito. Y se han eliminado las sanciones\nPuede que el pago tarde un poco en verse reflejado, reinicie la aplicación si el pago no se ve reflejado.")
                conn.commit()
            except mariadb.Error as e:
                print(f"Error al actualizar la base de datos: {e}")
            finally:
                conn.close()
            fecha_hoy = datetime.now().strftime('%d / %m / %Y')
            subject = f"Saldo pendiente liquidado"
            body = f"""
Has realizado el pago de tu saldo pendiente con éxito el día {fecha_hoy}.

Gracias por tu preferencia.
    """
            email_reciver = self.account_email
            if re.match(email_regex, email_reciver):
                em = EmailMessage()
                em["From"] = email_sender
                em["To"] = email_reciver
                em["Subject"] = subject
                em.set_content(body)

                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                        smtp.login(email_sender, password)
                        smtp.sendmail(email_sender, email_reciver, em.as_string())
                    print("Correo enviado correctamente.")
                except Exception as e:
                    print(f"Error al enviar el correo: {e}")
            else:
                print("Dirección de correo electrónico no válida.")
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "No se pudo conectar a la base de datos.")
    
        # Cerrar la ventana de pago
        self.accept()

    def sancionar_usuarios(self):
        try:
            conn = conectar()
            if conn:
                cursor = conn.cursor()
                # Obtener solo el usuario que ha iniciado sesión
                cursor.execute("SELECT DATEDIFF(NOW(), fecha_prestamo) as dias_retraso FROM prestamo WHERE id_usuario = ? AND fecha_prestamo < NOW() AND devuelto = 0", (self.account_id,))
                resultado = cursor.fetchone()  # Usamos fetchone() para obtener solo una fila

                if resultado:  # Verificamos si se encontró un resultado
                    dias_retraso = resultado[0]  # Días de retraso
                    if dias_retraso > 0:
                        if dias_retraso <= 7:
                            multa = dias_retraso * 5  # Multa de 5 unidades por día de retraso
                            cursor.execute("UPDATE usuarios SET multa = multa + ? WHERE id = ?", (multa, self.account_id))
                            conn.commit()
                            QtWidgets.QMessageBox.information(self.main_window, "Sanción aplicada", f"Se ha aplicado una multa de {multa} unidades por {dias_retraso} días de retraso.")
                            conn.commit()
                        else:
                            cursor.execute("UPDATE usuarios SET cuenta_cancelada = 2, multa = 10 WHERE id = ?", (self.account_id,))
                            conn.commit()
                            QtWidgets.QMessageBox.information(self.main_window, "Sanción aplicada", "Se ha cancelado la cuenta del usuario por más de 7 días de retraso.")
                else:
                    QtWidgets.QMessageBox.information(self.main_window, "Información", "No hay libros no devueltos a tiempo.")
                
                conn.commit()  # Asegúrate de hacer commit para guardar los cambios en la base de datos
            else:
                QtWidgets.QMessageBox.critical(self.main_window, "Error", "No se pudo conectar a la base de datos.")
        except mariadb.Error as e:
            print(f"Error al actualizar la base de datos: {e}")
        finally:
            if conn:
                conn.close()

class VentanaRegistro(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Define los elementos de la ventana modal aquí
        self.setWindowTitle("Registrarse")
        self.setGeometry(600, 300, 600, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        # Aplica la hoja de estilo a la ventana
        self.setStyleSheet("""
            QWidget {
                background-color: #DAC8AE;
                color: #111111;
            }

            /* Estilo para los botones */
            QPushButton {
                background-color: #EFDECD;
                color: #1A1110;
                border: 2px solid #1A1110;
                padding: 5px;
            }

            QPushButton:hover {
                background-color: #CC7722;
            }

            /* Estilo para los cuadros de texto */
            QLineEdit {
                background-color: #FFFFFF;
                color: #111111;
                border: 1px solid #00416A;
                padding: 4px;
            }

            QLineEdit:focus {
                border: 2px solid #00416A;
            }

            /* Estilo para las etiquetas */
            QLabel {
                color: #1A1110;
            }
        """)

        # Etiqueta para email
        self.labelEmail = QLabel(self)
        self.labelEmail.setText("Email:")
        self.inputEmail = QLineEdit(self)
        # Etiqueta para contraseña
        self.labelPassword = QLabel(self)
        self.labelPassword.setText("Contraseña:")
        self.inputPassword = QLineEdit(self)
        # Etiqueta para nombre
        self.labelName = QLabel(self)
        self.labelName.setText("Nombre:")
        self.inputName = QLineEdit(self)
        # Etiqueta para Apellido1
        self.labelLastName1 = QLabel(self)
        self.labelLastName1.setText("Apellido paterno:")
        self.inputLastName1 = QLineEdit(self)
        # Etiqueta para Apellido2
        self.labelLastName2 = QLabel(self)
        self.labelLastName2.setText("Apellido materno:")
        self.inputLastName2 = QLineEdit(self)

        # Botón para eliminar el registro
        self.btnRegister = QPushButton("Registrarse", self)
        self.btnRegister.clicked.connect(self.insertar)

        # Layout vertical para organizar los elementos
        layout = QVBoxLayout()
        layout.addWidget(self.labelEmail)
        layout.addWidget(self.inputEmail)
        layout.addWidget(self.labelPassword)
        layout.addWidget(self.inputPassword)
        layout.addWidget(self.labelName)
        layout.addWidget(self.inputName)
        layout.addWidget(self.labelLastName1)
        layout.addWidget(self.inputLastName1)
        layout.addWidget(self.labelLastName2)
        layout.addWidget(self.inputLastName2)
        layout.addWidget(self.btnRegister)
        # Asigna el layout a la ventana modal
        self.setLayout(layout)
        self.center()

    def center(self):
        # Obtenemos la geometría de la ventana principal
        qr = self.frameGeometry()
        # Obtenemos la posición central de la pantalla
        cp = QDesktopWidget().availableGeometry().center()
        # Movemos la ventana al centro de la pantalla
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # Método para validar el correo electrónico
    def validarcorreo(self, txtAValidar):
        x=re.search("^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", txtAValidar)
        return x

    # Método para validar la contraseña
    def validarpass(self, txtAValidar):
        x=re.search("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$¡!%*¿?&(){}[\]<>^;:,./\\|_~`+=-])[A-Za-z\d@$¡!%*¿?&(){}[\]<>^;:,./\\|_~`+=-]{8,}$", txtAValidar)
        return x

    # Método para validar campos vacíos
    def validarVacio(self, txtAValidar, n = 3):
        if txtAValidar is None or len(txtAValidar.strip()) < n:
            return True
        return False

    # Método para llamar a la función de insertar un usuario en la base de datos
    def insertar(self):
        # Obtener los valores ingresados por el usuario
        email = self.inputEmail.text()
        contraseña = self.inputPassword.text()
        nombre = self.inputName.text()
        apellido1 = self.inputLastName1.text()
        apellido2 = self.inputLastName2.text()

        if not self.validarcorreo(email):
            QtWidgets.QMessageBox.critical(self, "Error", "Formato de correo inválido.")
            return

        if not self.validarpass(contraseña):
            QtWidgets.QMessageBox.critical(self, "Error", "La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.")
            return
        
        if self.validarVacio(nombre):
            QtWidgets.QMessageBox.critical(self, "Error", "El nombre es obligatorio y debe tener al menos 3 caracteres.")
            return
        
        if self.validarVacio(apellido1):
            QtWidgets.QMessageBox.critical(self, "Error", "El apellido paterno es obligatorio y debe tener al menos 3 caracteres.")
            return
        
        if self.validarVacio(apellido2):
            QtWidgets.QMessageBox.critical(self, "Error", "El apellido materno es obligatorio y debe tener al menos 3 caracteres.")
            return
        
        # Insertar el registro en la base de datos
        try:
            # Asignar el ID del usuario registrado a la variable usuario_id
            usuario_id = self.insertar_usuarios(email, contraseña, nombre, apellido1, apellido2)
            if usuario_id:
                QtWidgets.QMessageBox.information(self, "Éxito", "Registro realizado correctamente.")
                print("ID del usuario registrado:", usuario_id)
                self.close()

        except mariadb.Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al realizar el registro: {e}")

    # Ejecutar una consulta en la base de datos
    def ejecutar_query(self, query, values):
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            return cur.lastrowid
        except mariadb.Error as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error al realizar el registro: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # Método para insertar un nuevo registro en la base de datos
    def insertar_usuarios(self, email, contraseña, nombre, apellido1, apellido2):
        query = "INSERT INTO usuarios (email, password, name, last_name1, last_name2) VALUES (?, ?, ?, ?, ?)"
        values = (email, contraseña, nombre, apellido1, apellido2)
class Ui_MainWindow(object):
    def __init__(self):
        self.key = self.cargar_clave()  # Carga la clave en una variable de instancia
        self.cipher_suite = Fernet(self.key)  # Crea la suite de cifrado
        self.main_window = MainWindow
        self.sancion_aplicada = False  # Bandera para rastrear si sancionar_usuarios ya ha sido llamada
        self.key = self.cargar_clave()  # Carga la clave en una variable de instancia
        self.cipher_suite = Fernet(self.key)  # Crea la suite de cifrado
        self.main_window = MainWindow
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(1055, 718)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("QWidget {\n"
"            background-color: #DAC8AE;\n"
"            color: #111111\n"
"        }\n"
"\n"
"/* Estilo para los botones */\n"
"QPushButton {\n"
"            background-color: #EFDECD;\n"
"            color: #1A1110;\n"
"            border: 2px solid #1A1110;\n"
"            padding: 5px;\n"
"}    \n"
"\n"
"/*Estilo de color cuando el mouse está encima del botón */\n"
"QPushButton:hover {\n"
"            background-color: #CC7722;  \n"
"}\n"
"\n"
"/* Estilo para las pestañas */\n"
"QTabWidget::pane {\n"
"            border-top: 2px solid #674C47;\n"
"            border-left: 2px solid #674C47;\n"
"            border-right: 2px solid #674C47;\n"
"            border-bottom: 2px solid #674C47;\n"
"}\n"
"\n"
"/*Estilo de color para las pestañas superiores*/\n"
"QTabBar::tab {\n"
"            background: #DAC8AE;\n"
"            color: #111111;\n"
"            padding: 8px;\n"
"            border-top: 0.5px solid #1A1110;\n"
"            border-left: 0.5px solid #1A1110;\n"
"            border-right: 0.5px solid #1A1110;\n"
"            border-bottom: 0.5px solid #1A1110;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"            background: #EAE0C8;\n"
"            color: #1A1110;\n"
"}\n"
"\n"
"/* Estilo para las tablas */\n"
"QTableWidget {\n"
"            background-color: #FFFFFF;\n"
"            color: #111111;\n"
"            gridline-color: #00416A;\n"
"            border: 1px solid #00416A;\n"
"}\n"
"\n"
"/*Estilo para los headers de las tablas*/\n"
"QHeaderView::section {\n"
"            background-color: #91A3B0;\n"
"            color: #1A1110;\n"
"            padding: 4px;\n"
"            border: 1px solid #1A1110;\n"
"}\n"
"\n"
"/* Estilo para los cuadros de texto */\n"
"QLineEdit {\n"
"            background-color: #FFFFFF;\n"
"            color: #111111;\n"
"            border: 1px solid #00416A;\n"
"            padding: 4px;\n"
"}\n"
"\n"
"        QLineEdit:focus {\n"
"            border: 2px solid #00416A;  /* Borde más grueso cuando está enfocado */\n"
"        }")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_search = QtWidgets.QWidget()
        self.tab_search.setObjectName("tab_search")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_search)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.btnReservar = QtWidgets.QPushButton(self.tab_search)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnReservar.setFont(font)
        self.btnReservar.setObjectName("btnReservar")
        self.gridLayout_3.addWidget(self.btnReservar, 6, 3, 1, 1)
        self.btnReservar.clicked.connect(self.reservar)

        self.btnComprar = QtWidgets.QPushButton(self.tab_search)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.btnComprar.setFont(font)
        self.btnComprar.setObjectName("btnComprar")
        self.gridLayout_3.addWidget(self.btnComprar, 6, 2, 1, 1)
        self.btnComprar.clicked.connect(self.comprar)
                
        self.label = QtWidgets.QLabel(self.tab_search)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(25, 25))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("imagenes/lupa1.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        
        self.btnSearchAutor = QtWidgets.QPushButton(self.tab_search)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.btnSearchAutor.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imagenes/autor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearchAutor.setIcon(icon)
        self.btnSearchAutor.setObjectName("btnSearchAutor")
        self.gridLayout_3.addWidget(self.btnSearchAutor, 2, 1, 1, 1)
        self.btnSearchAutor.clicked.connect(self.searchAuthor)
        
        self.btnSearchTitle = QtWidgets.QPushButton(self.tab_search)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.btnSearchTitle.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imagenes/title.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearchTitle.setIcon(icon1)
        self.btnSearchTitle.setCheckable(False)
        self.btnSearchTitle.setObjectName("btnSearchTitle")
        self.gridLayout_3.addWidget(self.btnSearchTitle, 2, 2, 1, 1)
        self.btnSearchTitle.clicked.connect(self.searchTitle)
        
        self.btnSearchGenre = QtWidgets.QPushButton(self.tab_search)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.btnSearchGenre.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imagenes/dragon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearchGenre.setIcon(icon2)
        self.btnSearchGenre.setAutoDefault(False)
        self.btnSearchGenre.setDefault(False)
        self.btnSearchGenre.setFlat(False)
        self.btnSearchGenre.setObjectName("btnSearchGenre")
        self.gridLayout_3.addWidget(self.btnSearchGenre, 2, 3, 1, 1)
        self.btnSearchGenre.clicked.connect(self.searchGenre)
        
        self.searchBar = QtWidgets.QLineEdit(self.tab_search)
        self.searchBar.setText("")
        self.searchBar.setObjectName("lineEdit")
        self.gridLayout_3.addWidget(self.searchBar, 0, 1, 1, 3)
        self.searchBar.returnPressed.connect(self.searchTitle)
        
        self.tableSearch = QtWidgets.QTableWidget(self.tab_search)
        self.tableSearch.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableSearch.setAlternatingRowColors(False)
        self.tableSearch.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableSearch.setColumnCount(7)
        self.tableSearch.setObjectName("tableSearch")
        self.tableSearch.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSearch.setHorizontalHeaderItem(6, item)
        header = self.tableSearch.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        self.tableSearch.verticalHeader().setVisible(False)
        self.tableSearch.horizontalHeader().setVisible(True)
        self.tableSearch.horizontalHeader().setCascadingSectionResizes(False)
        self.tableSearch.horizontalHeader().setSortIndicatorShown(False)
        self.tableSearch.horizontalHeader().setStretchLastSection(False)
        self.tableSearch.verticalHeader().setCascadingSectionResizes(False)
        self.tableSearch.verticalHeader().setSortIndicatorShown(False)
        self.gridLayout_3.addWidget(self.tableSearch, 5, 0, 1, 4)
        self.tabWidget.addTab(self.tab_search, "")
        #end of tab_search
        self.tab_history = QtWidgets.QWidget()
        self.tab_history.setObjectName("tab_history")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_history)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tableHistory = QtWidgets.QTableWidget(self.tab_history)
        self.tableHistory.setColumnCount(6)
        self.tableHistory.setObjectName("tableHistory")
        self.tableHistory.setRowCount(0)
        header = self.tableHistory.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.tableHistory.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableHistory.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableHistory.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableHistory.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableHistory.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableHistory.setHorizontalHeaderItem(5, item)
        self.gridLayout_4.addWidget(self.tableHistory, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_history, "")
        #end of tab_history

        self.tab_mybooks = QtWidgets.QWidget()
        
        self.tab_mybooks.setObjectName("tab_mybooks")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_mybooks)
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.tableMyBooks = QtWidgets.QTableWidget(self.tab_mybooks)
        self.tableMyBooks.setColumnCount(8)
        self.tableMyBooks.setObjectName("tableWidget")
        self.tableMyBooks.setRowCount(0)
        header = self.tableMyBooks.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        header.setSectionResizeMode(6, QHeaderView.Stretch)
        header.setSectionResizeMode(7, QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableMyBooks.setHorizontalHeaderItem(7, item)
        self.gridLayout_2.addWidget(self.tableMyBooks, 0, 0, 1, 3)
        
        
        self.tabWidget.currentChanged.connect(self.tab_changed)
        self.tableMyBooks.verticalHeader().setVisible(False)
        self.tableSearch.verticalHeader().setVisible(False)
        self.tableHistory.verticalHeader().setVisible(False)
        
        self.btnCancelar = QtWidgets.QPushButton(self.tab_mybooks)
        self.btnCancelar.setObjectName("btnCancelar")
        self.gridLayout_2.addWidget(self.btnCancelar, 1, 0, 1, 1)
        self.btnCancelar.clicked.connect(self.cancelar_reserva)
        
        self.btnDevolver = QtWidgets.QPushButton(self.tab_mybooks)
        self.btnDevolver.setObjectName("btnDevolver")
        self.gridLayout_2.addWidget(self.btnDevolver, 1, 1, 1, 1)
        self.btnDevolver.clicked.connect(self.devolver_reserva)

        self.btnCalificar = QtWidgets.QPushButton(self.tab_mybooks)
        self.btnCalificar.setObjectName("btnCalificar")
        self.gridLayout_2.addWidget(self.btnCalificar, 1, 2, 1, 1)
        self.btnCalificar.clicked.connect(self.calificar)
        
        
        self.tabWidget.addTab(self.tab_mybooks, "")
        self.tab_account = QtWidgets.QWidget()
        self.tab_account.setEnabled(True)
        self.tab_account.setObjectName("tab_account")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_account)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        
        self.label_2 = QtWidgets.QLabel(self.tab_account)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 7, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(self.tab_account)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMaximumSize(QtCore.QSize(300, 70))
        self.label_10.setText("")
        self.label_10.setPixmap(QtGui.QPixmap("imagenes/logoLP2.png"))
        self.label_10.setScaledContents(True)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout_5.addLayout(self.verticalLayout, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 7, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        
        self.label_4 = QtWidgets.QLabel(self.tab_account)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 0))
        self.label_4.setMaximumSize(QtCore.QSize(35, 35))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("imagenes/avatar.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 9, 0, 1, 1)
        
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem3, 7, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem4, 11, 3, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        
        self.label_5 = QtWidgets.QLabel(self.tab_account)
        self.label_5.setMinimumSize(QtCore.QSize(0, 0))
        self.label_5.setMaximumSize(QtCore.QSize(40, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("imagenes/lock - Copy.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.gridLayout_5.addLayout(self.horizontalLayout_3, 11, 0, 1, 1)
        
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 9, 3, 1, 1)
        
        self.label_3 = QtWidgets.QLabel(self.tab_account)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setItalic(False)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_5.addWidget(self.label_3, 14, 2, 1, 1)
        
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem7, 0, 2, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem8, 2, 3, 1, 1)
        self.inputEmail = QtWidgets.QLineEdit(self.tab_account)
        self.inputEmail.setMinimumSize(QtCore.QSize(0, 35))
        self.inputEmail.setObjectName("inputEmail")
        self.gridLayout_5.addWidget(self.inputEmail, 9, 2, 1, 1)
        
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_account)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_5.addWidget(self.pushButton_8, 16, 2, 1, 1)
        self.pushButton_8.clicked.connect(self.registrarse)
        
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem9, 13, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tab_account)
        self.label_11.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMaximumSize(QtCore.QSize(300, 70))
        self.label_11.setAutoFillBackground(False)
        self.label_11.setStyleSheet("opacity:0;\n""")
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap("imagenes/trans.png"))
        self.label_11.setScaledContents(True)
        self.label_11.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 0, 3, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem10, 17, 2, 1, 1)
        
        self.btnLogin = QtWidgets.QPushButton(self.tab_account)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnLogin.setFont(font)
        self.btnLogin.setObjectName("btnLogin")
        self.gridLayout_5.addWidget(self.btnLogin, 12, 2, 1, 1)
        self.btnLogin.clicked.connect(lambda: self.iniciar_sesion(True))
        
        self.inputPassword = QtWidgets.QLineEdit(self.tab_account)
        self.inputPassword.setMinimumSize(QtCore.QSize(0, 35))
        self.inputPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inputPassword.setObjectName("inputPassword")
        self.gridLayout_5.addWidget(self.inputPassword, 11, 2, 1, 1)
        self.inputPassword.returnPressed.connect(lambda: self.iniciar_sesion(True))
                
        

        #aqui empieza el tab de calificacion
        self.tab_calification = QtWidgets.QWidget()
        self.tab_calification.setObjectName("tab_calification")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_calification)
        self.gridLayout_7.setObjectName("gridLayout_7")

        self.label = QtWidgets.QLabel(self.tab_calification)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(25, 25))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("imagenes/lupa1.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 0, 0, 1, 1) 

        self.searchBar2 = QtWidgets.QLineEdit(self.tab_calification)
        self.searchBar2.setText("")
        self.searchBar2.setObjectName("lineEdit")
        self.gridLayout_7.addWidget(self.searchBar2, 0, 1, 1, 3)
        self.searchBar2.returnPressed.connect(self.searchReview)       

        self.tableCalification = QtWidgets.QTableWidget(self.tab_calification)
        self.tableCalification.setColumnCount(3)
        self.tableCalification.setObjectName("tableCalification")
        self.tableCalification.setRowCount(0)
        header = self.tableCalification.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.tableCalification.verticalHeader().setVisible(False)
        item = QtWidgets.QTableWidgetItem()
        self.tableCalification.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableCalification.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableCalification.setHorizontalHeaderItem(2, item)
        self.gridLayout_7.addWidget(self.tableCalification, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab_calification, "")

                #CLON DE HISTORIAL DE PRESTAMOS, SI SALE ALGO MAL ES CULPA DE DANI
        self.tab_orders = QtWidgets.QWidget()
        self.tab_orders.setObjectName("tab_order")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_orders)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.tableOrder = QtWidgets.QTableWidget(self.tab_orders)

        #esta es la tabla
        self.tableOrder.setColumnCount(6)
        self.tableOrder.setObjectName("tableOrder")
        self.tableOrder.setRowCount(0)
        header = self.tableOrder.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Stretch)
        item = QtWidgets.QTableWidgetItem()
        self.tableOrder.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableOrder.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableOrder.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableOrder.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableOrder.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableOrder.setHorizontalHeaderItem(5, item)
        self.gridLayout_9.addWidget(self.tableOrder, 10, 10, 10, 10)
        
        self.tabWidget.addTab(self.tab_orders, "")
        
        self.tableOrder.verticalHeader().setVisible(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem11)
        self.label_9 = QtWidgets.QLabel(self.tab_account)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMaximumSize(QtCore.QSize(150, 150))
        self.label_9.setText("")
        self.label_9.setPixmap(QtGui.QPixmap("imagenes/perfil.png"))
        self.label_9.setScaledContents(True)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setWordWrap(False)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem12)
        self.gridLayout_5.addLayout(self.horizontalLayout, 2, 2, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem13, 15, 2, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_account, "")
        
        self.tab_user = QtWidgets.QWidget()
        self.tab_user.setObjectName("tab_user")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_user)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem14)
        self.gridLayout_7.addLayout(self.horizontalLayout_5, 11, 0, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem15, 7, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem16, 13, 2, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem17)
        self.gridLayout_7.addLayout(self.horizontalLayout_4, 9, 0, 1, 1)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem18, 11, 4, 1, 1)
        self.labelUserID = QtWidgets.QLabel(self.tab_user)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelUserID.setFont(font)
        self.labelUserID.setObjectName("labelUserID")
        self.gridLayout_7.addWidget(self.labelUserID, 11, 2, 1, 1)
        self.transparent = QtWidgets.QLabel(self.tab_user)
        self.transparent.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.transparent.sizePolicy().hasHeightForWidth())
        self.transparent.setSizePolicy(sizePolicy)
        self.transparent.setMaximumSize(QtCore.QSize(300, 70))
        self.transparent.setAutoFillBackground(False)
        self.transparent.setStyleSheet("opacity:0;\n"
"")
        self.transparent.setText("")
        self.transparent.setPixmap(QtGui.QPixmap("imagenes/trans.png"))
        self.transparent.setScaledContents(True)
        self.transparent.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.transparent.setObjectName("transparent")
        self.gridLayout_7.addWidget(self.transparent, 0, 4, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem19)
        self.label_18 = QtWidgets.QLabel(self.tab_user)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMaximumSize(QtCore.QSize(150, 150))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("imagenes/usuarioIn.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setWordWrap(False)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_6.addWidget(self.label_18)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem20)
        self.gridLayout_7.addLayout(self.horizontalLayout_6, 2, 2, 1, 1)
        
        self.labelNombre = QtWidgets.QLabel(self.tab_user)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelNombre.setFont(font)
        self.labelNombre.setObjectName("labelNombre")
        self.gridLayout_7.addWidget(self.labelNombre, 7, 2, 1, 1)
        
        self.labelCredit = QtWidgets.QLabel(self.tab_user)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.labelCredit.setFont(font)
        self.labelCredit.setObjectName("labelCredit")
        self.gridLayout_7.addWidget(self.labelCredit, 9, 2, 1, 1)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem21, 9, 4, 1, 1)
        spacerItem22 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem22, 2, 4, 1, 1)
        
        self.btnLogout = QtWidgets.QPushButton(self.tab_user)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("imagenes/logout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnLogout.setIcon(icon3)
        self.btnLogout.setObjectName("btnLogout")
        self.gridLayout_7.addWidget(self.btnLogout, 15, 2, 1, 1)
        self.btnLogout.clicked.connect(self.logout)
        
        self.btnPay = QtWidgets.QPushButton(self.tab_user)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("imagenes/wallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPay.setIcon(icon4)
        self.btnPay.setObjectName("btnPay")
        self.gridLayout_7.addWidget(self.btnPay, 14, 2, 1, 1)
        self.btnPay.clicked.connect(self.pay)
        
        spacerItem23 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem23, 0, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.tab_user)
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.gridLayout_7.addWidget(self.label_12, 15, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_13 = QtWidgets.QLabel(self.tab_user)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMaximumSize(QtCore.QSize(300, 70))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap("imagenes/logoLP2.png"))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        spacerItem24 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem24)
        self.gridLayout_7.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        spacerItem25 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_7.addItem(spacerItem25, 7, 4, 1, 1)
        spacerItem26 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem26, 17, 2, 1, 1)
        self.gridLayout_8.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        
        self.tabWidget.addTab(self.tab_user, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.tabWidget.addTab(self.tab_user, "")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.account_id = 0
        self.credit = 0
        self.account_email = ""
        self.cargar_credenciales()
        self.tabWidget.removeTab(6)
        self.tabWidget.setCurrentIndex(0)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.searchBar, self.btnSearchAutor)
        MainWindow.setTabOrder(self.btnSearchAutor, self.btnSearchGenre)
        MainWindow.setTabOrder(self.btnSearchGenre, self.btnComprar)
        MainWindow.setTabOrder(self.btnComprar, self.btnReservar)
        MainWindow.setTabOrder(self.btnReservar, self.btnCancelar)
        MainWindow.setTabOrder(self.btnCancelar, self.btnDevolver)
        MainWindow.setTabOrder(self.btnDevolver, self.btnLogin)
        MainWindow.setTabOrder(self.btnLogin, self.btnSearchTitle)
        MainWindow.setTabOrder(self.btnSearchTitle, self.inputEmail)
        MainWindow.setTabOrder(self.inputEmail, self.inputPassword)
        MainWindow.setTabOrder(self.inputPassword, self.pushButton_8)
        MainWindow.setTabOrder(self.pushButton_8, self.tableHistory)
        MainWindow.setTabOrder(self.tableHistory, self.tableSearch)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", f"LibraryPy - {version}"))
        icon = os.path.join(script_dir, 'imagenes/icon.ico').replace("\\", "/")
        MainWindow.setWindowIcon(QIcon(icon))
        self.btnComprar.setText(_translate("MainWindow", "Comprar"))
        self.btnReservar.setText(_translate("MainWindow", "Reservar"))
        self.btnSearchAutor.setText(_translate("MainWindow", "   Buscar autor"))
        self.btnSearchTitle.setText(_translate("MainWindow", "    Buscar título"))
        self.btnSearchGenre.setText(_translate("MainWindow", "   Buscar género"))
        self.searchBar.setPlaceholderText(_translate("MainWindow", "Título, autor o género"))
        item = self.tableSearch.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Título"))
        item = self.tableSearch.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Autor"))
        item = self.tableSearch.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Género"))
        item = self.tableSearch.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableSearch.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Estado"))
        item = self.tableSearch.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Calificación"))
        item = self.tableSearch.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Precio"))
        self.tableSearch.resizeColumnsToContents()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_search), _translate("MainWindow", "Busqueda"))
        item = self.tableHistory.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableHistory.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "ID del libro"))
        item = self.tableHistory.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Título del libro"))
        item = self.tableHistory.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Fecha de préstamo"))
        item = self.tableHistory.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Fecha de devolución"))
        item = self.tableHistory.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Estado"))
        self.tableHistory.resizeColumnsToContents()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), _translate("MainWindow", "Historial de prestamos"))

        #LO MISMO DE ARRIBA

        item = self.tableOrder.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Titulo"))
        item = self.tableOrder.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Autor"))
        item = self.tableOrder.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Genero"))
        item = self.tableOrder.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Calificación"))
        item = self.tableOrder.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Precio"))
        item = self.tableOrder.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Fecha de compra"))
        self.tableOrder.resizeColumnsToContents()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_orders), _translate("MainWindow", "Historial de compras"))

        self.btnCancelar.setText(_translate("MainWindow", "Cancelar reserva"))
        self.btnDevolver.setText(_translate("MainWindow", "Devolver libro"))
        self.btnCalificar.setText(_translate("MainWindow", "Calificar libro"))
        item = self.tableMyBooks.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableMyBooks.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Título"))
        item = self.tableMyBooks.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Autor"))
        item = self.tableMyBooks.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "ID Libro"))
        item = self.tableMyBooks.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Fecha de préstamo"))
        item = self.tableMyBooks.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Fecha de devolución"))
        item = self.tableMyBooks.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Estado"))
        item = self.tableMyBooks.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Mi Calificación"))
        self.tableMyBooks.resizeColumnsToContents()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mybooks), _translate("MainWindow", "Mis libros"))
        self.label_2.setText(_translate("MainWindow", "Iniciar Sesión"))
        self.label_3.setText(_translate("MainWindow", "¿Aún no tienes una cuenta?"))
        self.inputEmail.setPlaceholderText(_translate("MainWindow", "Correo electrónico"))
        self.pushButton_8.setText(_translate("MainWindow", "Registrarse"))
        self.btnLogin.setText(_translate("MainWindow", "Entrar"))
        self.inputPassword.setPlaceholderText(_translate("MainWindow", "Contraseña"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_account), _translate("MainWindow", "Cuenta"))
        self.btnLogout.setText(_translate("MainWindow", "  Cerrar Sesión"))
        self.btnPay.setText(_translate("MainWindow", "   Pagar Saldo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_user), _translate("MainWindow", "Datos de usuario"))
        self.searchBar2.setPlaceholderText(_translate("MainWindow", "ID del libro a buscar"))
        item = self.tableCalification.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Título"))
        item = self.tableCalification.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Reseña"))
        item = self.tableCalification.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Calificación"))
        self.tableCalification.resizeColumnsToContents()
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_calification), _translate("MainWindow", "Calificaciones"))


    def registrarse(self):
        ventana_registro = VentanaRegistro()
        if ventana_registro.exec_() == QDialog.Accepted:
            usuario_id = ventana_registro.insertar_usuarios()
            if usuario_id:
                # Aquí puedes hacer lo que necesites con el ID del usuario
                print("ID del usuario insertado:", usuario_id)
                self.account_id = usuario_id

    def iniciar_sesion(self, showMessage):
        email = self.inputEmail.text()
        contraseña = self.inputPassword.text()

        if not email or not contraseña:
            QtWidgets.QMessageBox.critical(None, "Error", "Por favor, ingrese email y contraseña.")
            return

        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT id, name, last_name1, last_name2, credit, email FROM usuarios WHERE email = ? AND password = ?", (email, contraseña))
            usuario = cur.fetchone()

            if usuario:
                self.account_id = usuario[0]
                self.credit = usuario[4]
                self.account_email = usuario[5]
                self.tabWidget.setCurrentIndex(3)  # Cambia a la pestaña tab_account
                self.labelNombre.setText("Nombre: " + usuario[1] + " " + usuario[2] + " " + usuario[3])
                self.labelCredit.setText(f"Saldo pendiente: ${str(self.credit)}")
                self.labelUserID.setText(f"ID: {str(self.account_id)}")
                # self.labelApellido2.setText("Apellido Materno: " + usuario[3])
                if(showMessage):
                    QtWidgets.QMessageBox.information(None, "Inicio de sesión exitoso", f"¡Bienvenido {usuario[1]} {usuario[2]} {usuario[3]}!")
                self.guardar_credenciales(email, contraseña)
                self.tabWidget.removeTab(5)  # Oculta la pestaña tab_user al iniciar sesión
                self.tabWidget.insertTab(5, self.tab_user, "Datos de usuario")  # Muestra la pestaña tab_user al cerrar sesión
                self.tabWidget.setCurrentIndex(0)  # Cambia a la pestaña tab_account
            else:
                if(showMessage):
                    QtWidgets.QMessageBox.critical(None, "Error", "Credenciales inválidas.\n¿El usuario está registrado?")

        except mariadb.Error as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"Error al iniciar sesión: {e}")

        finally:
            if conn:
                conn.close()

    def guardar_credenciales(self, email, contraseña):
        credenciales = {'email': email, 'contraseña': contraseña}
        credenciales_encriptadas = self.cipher_suite.encrypt(json.dumps(credenciales).encode())  # Encripta las credenciales
        data = {'credenciales': credenciales_encriptadas.decode()}  # Crea un objeto JSON con las credenciales encriptadas
        # Crea un directorio para guardar la clave si no existe
        os.makedirs(f'{directorio_libreria}', exist_ok=True)
        # Guarda las credenciales en un archivo
        credenciales_file = os.path.join(directorio_libreria, 'credenciales.json')
        with open(credenciales_file, 'w') as file:
            json.dump(data, file)  # Guarda el objeto JSON en un archivo
    
    def cargar_credenciales(self):
        # Crea un directorio para guardar la clave si no existe
        os.makedirs(f'{directorio_libreria}', exist_ok=True)
        # Carga las credenciales desde un archivo
        credenciales_file = os.path.join(directorio_libreria, 'credenciales.json')
        if not os.path.exists(credenciales_file):
            return

        with open(credenciales_file, 'r') as file:
            data = json.load(file)  # Carga el objeto JSON de un archivo

        if not data or 'credenciales' not in data:
            return

        try:
            credenciales_desencriptadas = self.cipher_suite.decrypt(data['credenciales'].encode()).decode()  # Desencripta las credenciales
            credenciales = json.loads(credenciales_desencriptadas)
            self.inputEmail.setText(credenciales['email'])
            self.inputPassword.setText(credenciales['contraseña'])
            self.iniciar_sesion(showMessage=False)  # Evitar que se muestre el mensaje al cargar las credenciales
        except (json.JSONDecodeError, InvalidToken):
            QtWidgets.QMessageBox.critical(None, "Error", "El archivo de credenciales no tiene un formato JSON válido o la clave de encriptación es incorrecta.")
            return

    # Método para cargar la clave de encriptación        
    def cargar_clave(self):
        # Crea un directorio para guardar la clave si no existe
        os.makedirs(f'{directorio_libreria}', exist_ok=True)
        # Carga la clave de un archivo o genera una nueva si no existe
        key_file = os.path.join(directorio_libreria, 'clave.key')
        if not os.path.exists(key_file):
            key = Fernet.generate_key()  # Genera una nueva clave si no existe una
            with open(key_file, 'w') as file:
                file.write(key.decode())  # Guarda la clave en un archivo
            return key
        else:
            with open(key_file, 'r') as file:
                key = file.read().encode()  # Lee la clave de un archivo
            return key
    
    # Método para cerrar sesión
    def logout(self):
        # Crea un directorio para guardar la clave si no existe
        os.makedirs(f'{directorio_libreria}', exist_ok=True)
        # Elimina el archivo de credenciales al cerrar sesión
        credenciales = os.path.join(directorio_libreria, "credenciales.json")
        if os.path.exists(credenciales):
            os.remove(credenciales)
            # NO DEBE ELIMINARSE clave.key, ESTO GENERARÍA UNA NUEVA CLAVE Y NO SE PODRÍAN DESCIFRAR LOS DATOS
            # SI SE ELIMINA SE DEBERÁN ELIMINAR TAMBIÉN LOS ARCHIVOS CIFRADOS Y VOLVER A INICIAR SESIÓN
            self.account_id = 0
            self.inputEmail.clear()
            self.inputPassword.clear()
            self.tabWidget.removeTab(5)  # Oculta la pestaña tab_user al cerrar sesión
            self.tabWidget.insertTab(5, self.tab_account, "Cuenta")  # Muestra la pestaña tab_user al cerrar sesión
            self.tabWidget.setCurrentIndex(3)  # Cambia a la pestaña tab_account

    # Busqueda por título
    def searchTitle(self):
        title = self.searchBar.text()
        if title:
            query = f"SELECT * FROM libro WHERE titulo LIKE '%{title}%'"
            self.mostrar_resultados(query, "título", title)
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Primero escribe algo en el buscador.")

    def searchReview(self):
        id_libro = self.searchBar2.text()
        if id_libro:
            query = f"SELECT libro.titulo, calificaciones.reseña, calificaciones.calificacion FROM libro INNER JOIN calificaciones ON libro.id = calificaciones.id_libro WHERE libro.id = {id_libro}"
            self.mostrar_resultados_review(query, "ID", id_libro)
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Primero escribe algo en el buscador.")

    # Busqueda por autor
    def searchAuthor(self):
        author = self.searchBar.text()
        if author:
            query = f"SELECT * FROM libro WHERE autor LIKE '%{author}%'"
            self.mostrar_resultados(query, "autor", author)
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Primero escribe algo en el buscador.")

    # Busqueda por genero
    def searchGenre(self):
        genre = self.searchBar.text()
        if genre:
            query = f"SELECT * FROM libro WHERE genero LIKE '%{genre}%'"
            self.mostrar_resultados(query, "género", genre)
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Primero escribe algo en el buscador.")

    def mostrar_resultados_review(self, query, tipo_busqueda, busqueda):
        try:
            self.tableCalification.clearContents()
            self.tableCalification.setRowCount(0)
            
            cur = self.consulta(query)
            if cur:
                found = False
                for row_number, row_data in enumerate(cur):
                    self.tableCalification.insertRow(row_number)
                    # Ajusta el orden de los datos para mostrarlos en la tabla
                    data_order = [0, 1, 2]  # Orden de las columnas: titulo, reseña, calificacion
                    for column_number, index in enumerate(data_order):
                        item = QTableWidgetItem(str(row_data[index]))
                        # Establecer el hint para mostrar el texto completo cuando el mouse pasa sobre la celda
                        item.setToolTip(str(row_data[index]))
                        self.tableCalification.setItem(row_number, column_number, item)
                    found = True
                    
                self.tableCalification.resizeColumnsToContents()
                
                if not found:
                    QtWidgets.QMessageBox.information(None, "Información", f"No se encontraron resultados para el {tipo_busqueda} '{busqueda}'.")
                    
                # Aquí ajustamos el tamaño de las columnas y la tabla
                header = self.tableCalification.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)  # Estirar la columna "Título"
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # Columna "Reseña"
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Columna "Calificación"
                self.tableCalification.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.tableCalification.horizontalHeader().setStretchLastSection(True)
                
            else:
                QtWidgets.QMessageBox.information(None, "Información", f"No se encontraron resultados para el {tipo_busqueda} '{busqueda}'.")
        except Exception as e:
            print("Error al mostrar resultados:", e)

    # Método para mostrar los resultados de la búsqueda
    def mostrar_resultados(self, query, tipo_busqueda, busqueda):
        try:
            self.tableSearch.clearContents()
            self.tableSearch.setRowCount(0)
            
            cur = self.consulta(query)
            if cur:
                found = False
                for row_number, row_data in enumerate(cur):
                    self.tableSearch.insertRow(row_number)
                    # Ajusta el orden de los datos para mostrarlos en la tabla
                    data_order = [3, 1, 4, 0, 2, 5, 6]  # Orden de las columnas: titulo, autor, genero, id, estado, calificacion

                    for column_number, index in enumerate(data_order):
                        if index == 2:  # Si la columna es la del estado
                            estado = "Disponible" if row_data[index] == 1 else "No disponible"
                            item = QTableWidgetItem(estado)
                        else:
                            item = QTableWidgetItem(str(row_data[index]))
                        # Establecer el hint para mostrar el texto completo cuando el mouse pasa sobre la celda
                        if index == 2:
                            item.setToolTip(estado)
                        else:
                            item.setToolTip(str(row_data[index]))
                        self.tableSearch.setItem(row_number, column_number, item)
                    found = True
                    
                self.tableSearch.resizeColumnsToContents()
                
                if not found:
                    QtWidgets.QMessageBox.information(None, "Información", f"No se encontraron resultados para el {tipo_busqueda} '{busqueda}'.")
                    
                # Aquí ajustamos el tamaño de las columnas y la tabla
                header = self.tableSearch.horizontalHeader()
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # Estirar la columna "Título"
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # Columna "ID"
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)  # Columna "Autor"
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)  # Columna "ID Libro"
                header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)  # Columna "Estado"
                header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
                self.tableSearch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                self.tableSearch.horizontalHeader().setStretchLastSection(True)
                
            else:
                QtWidgets.QMessageBox.information(None, "Información", f"No se encontraron resultados para el {tipo_busqueda} '{busqueda}'.")
        except Exception as e:
            print("Error al mostrar resultados:", e)

    # Método para realizar una consulta en la base de datos
    def consulta(self, query, values=None):
        try:
            conn = conectar()
            if conn:
                cur = conn.cursor()
                if values:
                    if not isinstance(values, (tuple, list)):
                        values = (values,)
                    cur.execute(query, values)
                else:
                    cur.execute(query)
                return cur
        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            return None
        finally:
            if conn:
                conn.close()

    # Reservar un libro
    def reservar(self):
        # Verificar si el usuario ha iniciado sesión
        if self.account_id == 0:
            QtWidgets.QMessageBox.critical(None, "Error", "Debes iniciar sesión para reservar un libro.")
            return
        # Obtener el índice de la fila seleccionada
        selected_row = self.tableSearch.currentRow()
        if selected_row >= 0:
            # Obtener los datos de la fila seleccionada
            id_libro = self.tableSearch.item(selected_row, 3).text()  # ID del libro
            disponibilidad = self.tableSearch.item(selected_row, 4).text()  # Disponibilidad del libro
            titulo = self.tableSearch.item(selected_row, 0).text()  # Título del libro
            autor = self.tableSearch.item(selected_row, 1).text()  # Autor del libro

            # Verificar si el libro está disponible
            if disponibilidad == 'Disponible':
                reply = QMessageBox.question(None, 'Reserva', 'El costo por reserva de cada libro es de $7.00 MXN por día, se te dará un limite de 15 días para retornarlo. Si no se devuelve a tiempo se cobrará una multa de $20 por cáda día que pase.\n(Es posible devolver antes el libro, solo se te cobrará lo correspondiente)',
                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
                if reply == QMessageBox.Ok:
                    # Obtener la fecha actual
                    fecha_prestamo = datetime.now().strftime('%Y-%m-%d')
                    # Obtener la fecha de devolución (15 días después de la fecha actual)
                    fecha_devolucion = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
                    # Obtener el ID de usuario
                    id_usuario = self.account_id
                    
                    # Insertar el préstamo en la base de datos
                    query = "INSERT INTO prestamo (fecha_devolucion, fecha_prestamo, id_usuario, id_libro) VALUES (?, ?, ?, ?)"
                    values = (fecha_devolucion, fecha_prestamo, id_usuario, id_libro)
                    id_pedido = self.ejecutar_query(query, values)
                    query = "INSERT INTO historial (id, fecha_devolucion, fecha_prestamo, id_usuario, id_libro) VALUES (?, ?, ?, ?, ?)"
                    values = (id_pedido, fecha_devolucion, fecha_prestamo, id_usuario, id_libro)
                    self.ejecutar_query(query, values)
                    if id_pedido:
                        self.correo_pedido(id_pedido, fecha_prestamo, fecha_devolucion, titulo, autor)
                        # Cambiar la disponibilidad del libro a 0
                        query = "UPDATE libro SET disponibilidad = 0 WHERE id = ?"
                        values = (id_libro,)
                        self.ejecutar_query(query, values)
                        
                        QtWidgets.QMessageBox.information(None, "Información", "Libro reservado con éxito.")
                        self.tableSearch.item(selected_row, 4).setText("No disponible")
            else:
                QtWidgets.QMessageBox.critical(None, "Error", "El libro seleccionado no está disponible.")
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Selecciona un libro para reservar.")
    
    def comprar(self):
        if self.account_id == 0:
            QtWidgets.QMessageBox.critical(None, "Error", "Debes iniciar sesión para reservar un libro.")
            return
        
        selected_row = self.tableSearch.currentRow()

        id_libro = self.tableSearch.item(selected_row, 3).text()  # ID del libro
        disponibilidad = self.tableSearch.item(selected_row, 4).text()  # Disponibilidad del libro
        titulo = self.tableSearch.item(selected_row, 0).text()  # Título del libro
        precio = self.tableSearch.item(selected_row, 6).text()  # Título del libro

        if selected_row < 0:
            QtWidgets.QMessageBox.critical(None, "Error", "Selecciona un libro para comprar")
            return

        if disponibilidad == 'No disponible':
            QtWidgets.QMessageBox.critical(None, "Error", "No hay libros disponibles para comprar")
            return
        
        reply = QMessageBox.question(None, 'Comprar libro', 'Confirmar compra del libro: ' + titulo,
                    QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        
        if reply != QMessageBox.Ok:
            return
        
        pago = VentanaPago(self.account_id, precio, self.account_email, self.main_window)
        pago.exec_()

        if pago.payBook():

            fecha_compra = datetime.now().strftime('%Y-%m-%d')
            id_usuario = self.account_id

            query = "INSERT INTO orden (id_usuario, id_libro, fecha) VALUES (?, ?, ?)"
            values = (id_usuario, id_libro, fecha_compra)
            self.ejecutar_query(query, values)

            query = "UPDATE libro SET disponibilidad = disponibilidad - 1 WHERE id = ?"
            values = (id_libro,)
            self.ejecutar_query(query, values)

            QtWidgets.QMessageBox.information(None, "Información", "Libro comprado con éxito.")
        

    # Método para ejecutar una consulta en la base de datos
    def ejecutar_query(self, query, values):
        try:
            conn = conectar()
            if conn:
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                return cur.lastrowid
        except Exception as e:
            print("Error al ejecutar la consulta:", e)
        finally:
            if conn:
                conn.close()

    # Actualizar la disponibilidad de un libro
    def actualizar_disponibilidad_libro(self, id_libro, disponibilidad):
        query = "UPDATE libro SET disponibilidad = ? WHERE id = ?"
        values = (disponibilidad, id_libro)
        self.ejecutar_query(query, values)
    
    # Insertar un nuevo préstamo en la base de datos
    def insertar_prestamo(self, fecha_devolucion, fecha_prestamo, id_usuario, id_libro):
        query = "INSERT INTO prestamo (fecha_devolucion, fecha_prestamo, id_usuario, id_libro) SELECT ?, ?, (SELECT id FROM usuarios WHERE id = ?), (SELECT id FROM libro WHERE id = ?)"
        values = (fecha_devolucion, fecha_prestamo, id_usuario, id_libro)
        self.insertar(query, values)
    
    # Método para insertar un nuevo registro en la base de datos
    def insertar(self, query, values):
        try:
            conn = conectar()
            if conn:
                cur = conn.cursor()
                cur.execute(query, values)
                conn.commit()
                print("Datos insertados correctamente.")
        except Exception as e:
            print(f"Error al insertar datos: {e}")
        finally:
            if conn:
                conn.close()

    # Consultar los libros reservados por el usuario actual
    def actualizar_mis_libros(self, estado = ""):
        # Limpiar la tabla
        self.tableMyBooks.clearContents()
        self.tableMyBooks.setRowCount(0)
        # Verificar si el usuario ha iniciado sesión
        if self.account_id == 0:
            QtWidgets.QMessageBox.critical(None, "Error", "Debes iniciar sesión para ver tus libros.")
            return
        # Obtener los préstamos del usuario actual
        query = "SELECT prestamo.id, libro.titulo, libro.autor, libro.id, prestamo.fecha_prestamo, prestamo.fecha_devolucion, prestamo.devuelto, libro.calificacion FROM prestamo INNER JOIN libro ON prestamo.id_libro = libro.id WHERE prestamo.id_usuario = ?"
        values = (self.account_id)
        cur = self.consulta(query, values)
        if cur.rowcount > 0:
            for row_number, row_data in enumerate(cur):
                self.tableMyBooks.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    if column_number == 6:  # Columna 6
                        if data == 0:
                            item.setText("Reservado")
                        elif data == 2:
                            item.setText("Cancelado")

                    # Insertar el item en la tabla
                    self.tableMyBooks.setItem(row_number, column_number, item)
            
            self.tableMyBooks.resizeColumnsToContents()
            # Aquí ajustamos el tamaño de las columnas y la tabla
            header = self.tableMyBooks.horizontalHeader()
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)  # Estirar la columna "Título"
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            self.tableMyBooks.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.tableMyBooks.horizontalHeader().setStretchLastSection(True)
            
        else:
            QtWidgets.QMessageBox.information(None, "Información", "No tienes libros reservados.")

    # Actualizar el historial de préstamos del usuario actual
    def actualizar_historial(self):
        # Limpiar la tabla
        self.tableHistory.clearContents()
        self.tableHistory.setRowCount(0)
        if self.account_id == 0:
            QtWidgets.QMessageBox.critical(None, "Error", "Debes iniciar sesión para ver tu historial.")
            return
        # Obtener el historial del usuario actual
        query = "SELECT h.id, l.id, l.titulo, h.fecha_prestamo, h.fecha_devolucion, h.devuelto FROM historial AS h INNER JOIN libro AS l ON h.id_libro = l.id WHERE h.id_usuario = ?"
        values = (self.account_id,)
        cur = self.consulta(query, values)
        if cur.rowcount > 0:
            for row_number, row_data in enumerate(cur):
                self.tableHistory.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    if column_number == 5:  # Verificar si estamos en la columna de "devuelto"
                        if data == 0:
                            item.setText("Reservado")
                        elif data == 1:
                            item.setText("Devuelto")
                        elif data == 2:
                            item.setText("Cancelado")
                    # Insertar el item en la tabla
                    self.tableHistory.setItem(row_number, column_number, item)
            
            self.tableHistory.resizeColumnsToContents()
            header = self.tableHistory.horizontalHeader()
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            self.tableHistory.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.tableHistory.horizontalHeader().setStretchLastSection(True)
            
        else:
            QtWidgets.QMessageBox.information(None, "Información", "No tienes historial de préstamos.")

    def show_orders(self):
        # Limpiar la tabla
        self.tableOrder.clearContents()
        self.tableOrder.setRowCount(0)
        if self.account_id == 0:
            QtWidgets.QMessageBox.critical(None, "Error", "Debes iniciar sesión para ver tu historial.")
            return
        # Obtener el historial del usuario actual
        query = "SELECT l.titulo, l.autor, l.genero, l.calificacion, l.precio, o.fecha FROM orden o JOIN libro l ON o.id_libro = l.id WHERE o.id_usuario = ?"
        values = (self.account_id,)
        cur = self.consulta(query, values)
        if cur.rowcount > 0:
            for row_number, row_data in enumerate(cur):
                self.tableOrder.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    # Insertar el item en la tabla
                    self.tableOrder.setItem(row_number, column_number, item)
            
            self.tableOrder.resizeColumnsToContents()
            header = self.tableOrder.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            self.tableOrder.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.tableOrder.horizontalHeader().setStretchLastSection(True)
            
        else:
            QtWidgets.QMessageBox.information(None, "Información", "No tienes historial de préstamos.")

    # Cancelar un préstamo
    def cancelar_reserva(self):
        # Obtener el índice de la fila seleccionada
        selected_row = self.tableMyBooks.currentRow()
        if selected_row >= 0:
            # Obtener los datos de la fila seleccionada
            id_prestamo = int(self.tableMyBooks.item(selected_row, 0).text())  # ID de prestamo
            id_libro = int(self.tableMyBooks.item(selected_row, 3).text())  # ID de libro
            fecha_prestamo = self.tableMyBooks.item(selected_row, 4).text()  # Fecha de prestamo
            fecha_hoy = datetime.now().strftime('%Y-%m-%d')
            if fecha_prestamo == fecha_hoy:
                try:
                    # Cambiar 'disponibilidad' del libro con id = id_libro a 1
                    query = "UPDATE libro SET disponibilidad = 1 WHERE id = ?"
                    self.ejecutar_query(query, (id_libro,))

                    # Cambiar 'devuelto' del prestamo con id = id_prestamo a 2
                    query2 = "UPDATE historial SET devuelto = 2 WHERE id = ?"
                    self.ejecutar_query(query2, (id_prestamo,))

                    # Borrar la tupla de la tabla 'prestamo' con 'id' = id_prestamo
                    query3 = "DELETE FROM prestamo WHERE id = ?"
                    self.ejecutar_query(query3, (id_prestamo,))
                    self.correo_cancelacion(id_prestamo)
                    QtWidgets.QMessageBox.information(None, "Cancelación de reserva", "Reserva cancelada con éxito.")

                    # Actualizar la tabla de mis libros
                    self.actualizar_mis_libros()

                except mariadb.Error as e:
                    QtWidgets.QMessageBox.critical(None, "Error", f"Error al cancelar reserva: {e}")

            else:
                QtWidgets.QMessageBox.warning(None, "Error", "Solo puedes cancelar reservas que se han hecho el mismo día.")

    # Devolver un libro
    def devolver_reserva(self):
        # Obtener el índice de la fila seleccionada
        selected_row = self.tableMyBooks.currentRow()
        if selected_row >= 0:
            # Obtener los datos de la fila seleccionada
            id_prestamo = int(self.tableMyBooks.item(selected_row, 0).text())  # ID de prestamo
            id_libro = int(self.tableMyBooks.item(selected_row, 3).text())  # ID de libro
            fecha_devolucion = datetime.strptime(self.tableMyBooks.item(selected_row, 5).text(), '%Y-%m-%d')  # Fecha de devolucion
            fecha_prestamo = datetime.strptime(self.tableMyBooks.item(selected_row, 4).text(), '%Y-%m-%d')  # Fecha de prestamo
            fecha_hoy = datetime.now()
            fecha_hoy_sin_tiempo = fecha_hoy.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # Calcular la diferencia de días
            dias_diferencia = (fecha_hoy_sin_tiempo - fecha_prestamo).days
            # Si se pasa de los 15 días, agregar la multa de $20 por día adicional
            if dias_diferencia > 15:
                costo = (dias_diferencia - 15) * 20
            else:
                costo = max(0, dias_diferencia) * 7
            try:
                # Obtener el crédito actual del usuario
                query_credito = "SELECT credit FROM usuarios WHERE id = ?"
                cur_credito = self.consulta(query_credito, (self.account_id,))
                credito_actual = cur_credito.fetchone()[0]

                # Sumar el costo al crédito actual
                nuevo_credito = credito_actual + costo
                self.credit = nuevo_credito
                # Actualizar el crédito del usuario en la base de datos
                query_actualizar_credito = "UPDATE usuarios SET credit = ? WHERE id = ?"
                self.ejecutar_query(query_actualizar_credito, (nuevo_credito, self.account_id))

                # Cambiar 'disponibilidad' del libro con id = id_libro a 1
                query1 = "UPDATE libro SET disponibilidad = 1 WHERE id = ?"
                self.ejecutar_query(query1, (id_libro,))

                # Cambiar 'devuelto' del prestamo con id = id_prestamo a 1
                query2 = "UPDATE historial SET devuelto = 1 WHERE id = ?"
                self.ejecutar_query(query2, (id_prestamo,))

                # Borrar la tupla de la tabla 'prestamo' con 'id' = id_prestamo
                query3 = "DELETE FROM prestamo WHERE id = ?"
                self.ejecutar_query(query3, (id_prestamo,))
                self.correo_devolucion(id_prestamo, fecha_devolucion, costo)
                QtWidgets.QMessageBox.information(None, "Devolución de reserva", f"Libro devuelto con éxito.\nCosto: ${costo}")

                # Actualizar la tabla de mis libros
                self.actualizar_mis_libros()

            except mariadb.Error as e:
                QtWidgets.QMessageBox.critical(None, "Error", f"Error al devolver reserva: {e}")

    # Actualizar tablas al cambiar de pestaña
    def tab_changed(self):
        if self.tabWidget.currentIndex() == 2:  
            self.actualizar_mis_libros()
        elif self.tabWidget.currentIndex() == 1:
            self.actualizar_historial()
        elif self.tabWidget.currentIndex() == 4:
            self.show_orders()
        elif self.tabWidget.currentIndex() == 5:
            self.actualizar_usuario()

    # Actualizar el crédito del usuario
    def actualizar_usuario(self):
        if self.account_id != 0:
            self.labelCredit.setText(f"Saldo pendiente: ${str(self.credit)}")

    # Método para enviar un correo electrónico al realizar un pedido
    def correo_pedido(self, id_pedido, fecha_prestamo, fecha_devolucion, titulo, autor):
        fecha_prestamo = datetime.strptime(fecha_prestamo, '%Y-%m-%d').strftime('%d / %m / %Y')
        fecha_devolucion = datetime.strptime(fecha_devolucion, '%Y-%m-%d').strftime('%d / %m / %Y')
        subject = f"Pedido realizado | Folio Nro.#{id_pedido}"
        body = f"""Tu pedido con folio #{id_pedido} ha sido realizado con éxito.
{titulo} de {autor}.

Pedido realizado el día: {fecha_prestamo}
Devolver antes del: {fecha_devolucion}

Recuerda que el costo por reserva de cada libro es de $7.00 MXN por día, se te dará un límite de 15 días para retornarlo. Si no se devuelve a tiempo se cobrará una multa de $20 por cáda día que pase.
(Es posible devolver antes el libro, solo se te cobrará lo correspondiente)
Gracias por tu preferencia.
"""
        email_reciver = self.account_email
        if re.match(email_regex, email_reciver):
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_reciver
            em["Subject"] = subject
            em.set_content(body)

            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, password)
                    smtp.sendmail(email_sender, email_reciver, em.as_string())
                print("Correo enviado correctamente.")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
        else:
            print("Dirección de correo electrónico no válida.")


    def correo_cancelacion(self, id_pedido):
        subject = f"Cancelación de pedido | Folio Nro.{id_pedido}"
        body = f"""Tu pedido con folio #{id_pedido} ha sido cancelado con éxito.

Has cancelado el pedido el mismo día de la reserva por lo que no se te cobrará ningun cargo.

Gracias por tu preferencia.
"""
        email_reciver = self.account_email
        if re.match(email_regex, email_reciver):
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = email_reciver
            em["Subject"] = subject
            em.set_content(body)

            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, password)
                    smtp.sendmail(email_sender, email_reciver, em.as_string())
                print("Correo enviado correctamente.")
            except Exception as e:
                print(f"Error al enviar el correo: {e}")
        else:
            print("Dirección de correo electrónico no válida.")

    # Método para enviar un correo electrónico al realizar una devolución
    def correo_devolucion(self, id_pedido, fecha_devolucion, costo):
            fecha_hoy = datetime.now().strftime('%d / %m / %Y')
            subject = f"Devolución de pedido | Folio Nro.{id_pedido}"
            body = f"""Tu pedido con folio #{id_pedido} ha sido devuelto con éxito.

Has devuelto el libro el día {fecha_hoy}, la fecha de devolución está marcada para el día {fecha_devolucion.strftime('%d / %m / %Y')}.
Se ha agregado un cargo de ${costo} a tu cuenta, actualmente se debe un total de ${self.credit}.

Gracias por tu preferencia.
    """
            email_reciver = self.account_email
            if re.match(email_regex, email_reciver):
                em = EmailMessage()
                em["From"] = email_sender
                em["To"] = email_reciver
                em["Subject"] = subject
                em.set_content(body)

                try:
                    context = ssl.create_default_context()
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                        smtp.login(email_sender, password)
                        smtp.sendmail(email_sender, email_reciver, em.as_string())
                    print("Correo enviado correctamente.")
                except Exception as e:
                    print(f"Error al enviar el correo: {e}")
            else:
                print("Dirección de correo electrónico no válida.")
    
    # Método para pagar el saldo pendiente
    def pay(self):
        if self.credit == 0:
            QtWidgets.QMessageBox.information(None, "Saldo pendiente", "Actualmente no tienes saldo pendiente por pagar.")
            return
        else:
            ventana_pago = VentanaPago(self.account_id, self.credit, self.account_email, self.main_window)  # Pasa main_window aquí
            if not self.sancion_aplicada:
                ventana_pago.sancionar_usuarios()
                self.sancion_aplicada = True  # Actualizar la bandera después de llamar a sancionar_usuarios
            ventana_pago.exec_()

    def calificar(self):
        selected_row = self.tableMyBooks.currentRow()
        if selected_row >= 0:
            titulo_libro = self.tableMyBooks.item(selected_row, 1).text()  # Nombre del libro
            id_libro = int(self.tableMyBooks.item(selected_row, 3).text()) 
            ventana_calificar = VentanaCalificar(self.account_id, titulo_libro, id_libro)
            ventana_calificar.exec_()
        else:
            QtWidgets.QMessageBox.critical(None, "Error", "Selecciona un libro para calificar.")

    def sancionar_usuarios(self):
        try:
            conn = conectar()
            if conn:
                cursor = conn.cursor()
                # Obtener solo el usuario que ha iniciado sesión
                cursor.execute("SELECT DATEDIFF(NOW(), fecha_prestamo) as dias_retraso FROM prestamo WHERE id_usuario = ? AND fecha_prestamo < NOW() AND devuelto = 0", (self.account_id,))
                resultado = cursor.fetchone()  # Usamos fetchone() para obtener solo una fila

                if resultado:  # Verificamos si se encontró un resultado
                    dias_retraso = resultado[0]  # Días de retraso
                    if dias_retraso > 0:
                        if dias_retraso <= 7:
                            multa = dias_retraso * 5  # Multa de 5 unidades por día de retraso
                            cursor.execute("UPDATE usuarios SET multa = multa + ? WHERE id = ?", (multa, self.account_id))
                            conn.commit()
                            QtWidgets.QMessageBox.information(self.main_window, "Sanción aplicada", f"Se ha aplicado una multa de {multa} unidades por {dias_retraso} días de retraso.")
                            conn.commit()
                        else:
                            cursor.execute("UPDATE usuarios SET cuenta_cancelada = 2, multa = 10 WHERE id = ?", (self.account_id,))
                            conn.commit()
                            QtWidgets.QMessageBox.information(self.main_window, "Sanción aplicada", "Se ha cancelado la cuenta del usuario por más de 7 días de retraso.")
                            conn.commit()
                else:
                    QtWidgets.QMessageBox.information(self.main_window, "Información", "No hay libros no devueltos a tiempo.")
                
                conn.commit()  # Asegúrate de hacer commit para guardar los cambios en la base de datos
            else:
                QtWidgets.QMessageBox.critical(self.main_window, "Error", "No se pudo conectar a la base de datos.")
        except mariadb.Error as e:
            print(f"Error al actualizar la base de datos: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())