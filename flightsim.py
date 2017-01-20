# -*- coding: UTF-8 -*-

'''
La clase VentanaPrincipal hereda el entorno gráfico y la aeronave del usuario.
Entre sus métodos destaca el motor del juego (engine), la función ver_terreno 
que construye la visual del terreno y las aeronaves, y la función ver_mapa que 
pasa los datos de la anterior al entorno gráfico redirigiendo la salida 
estándar a un archivo y capturándola posteriormente.

El tiempo es controlado por la clase QTimer que actúa como demonio.

La clase InitialSettings capta la configuración deseada por el usuario y la 
pasa a los constructores de aviones como keywords.
'''

import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.uic import loadUiType
from terreno import *
from aeronaves import *

aviones = []

maingui_form = loadUiType('maingui.ui')[0]
dialoginit_form = loadUiType('dialoginit.ui')[0]
opening_form = loadUiType('opening.ui')[0]
instrucciones_form = loadUiType('instrucciones.ui')[0]
about_form = loadUiType('about.ui')[0]
exit_form = loadUiType('exit.ui')[0]

class VentanaPrincipal(Smuggler, QMainWindow, maingui_form):
	def __init__(self, parent=None, **kwargs):
		QMainWindow.__init__(self, parent)
		Nave.__init__(self,**kwargs)
		self.t= 0
		self.setupUi(self)
		self.bTerminar.clicked.connect(self.exit_dialog)
		self.bGears.clicked.connect(self.fun_gears)
		self.sThrottle.setValue(self.P)
		self.sThrottle.valueChanged.connect(self.sliderThrottle)
		self.sRudder.valueChanged.connect(self.sliderRudder)
		QObject.connect(self.bBrakes, SIGNAL('clicked()'), 
						self, SLOT('frenos()'))
		self.bPause.clicked.connect(self.fun_pause)
		self.actionInstrucciones.triggered.connect(self.instrucciones)
		self.actionAcerca_de.triggered.connect(self.about)

	@pyqtSlot()
	def engine(self):
		self.t += 1
		self.tiempoLineEdit.setText(str(self.t))
		
		for avion in aviones:
			avion.combustible()
			if avion.status == 'flying':
				avion.Volar()
				avion.Chocar(terreno)
				if avion.__str__() == 'DEA':
					avion.Radar(aviones)
			if avion.status == 'landed':
				avion.Rodar()
			if avion._evento:
				self.messageBoard.append(avion._msg)
				avion._evento = False
						
		self.ver_mapa()	
		self.distLineEdit.setText(str(int(self.pos)))
		self.velocidadLineEdit.setText(str(int(self.vel*(3600.0/1000))))
		self.alturaLineEdit.setText(str(int(self.alt)))
		self.fuelLineEdit.setText(str(int(self.fuel)))
		
	def fun_pause(self):
		if self.bPause.isChecked():
			timer.stop()
		else:
			timer.start(1000)	
		
	@pyqtSlot()
	def sliderThrottle(self):
		self.P = self.sThrottle.value()		
		self.vThrottle.setText(str(self.P))
		
	@pyqtSlot()
	def sliderRudder(self):
		self.d_alt = self.sRudder.value()
		
	@pyqtSlot()
	def fun_gears(self):
		if self.bGears.isChecked() == True:
			self.gears = True
			msg = 'Tren de aterrizaje desplegado'
		else:
			self.gears = False
			msg = 'Tren de aterrizaje recogido'
		self.formateador(msg)		
				
	@pyqtSlot()
	def frenos(self):
		if self.bBrakes.isChecked() == True:
			self.brakes = True
		elif self.bBrakes.isChecked() == False:
			self.brakes = False
    
#	@pyqtSlot()
	def exit_dialog(self):
		self.salir = DialogExit()
		self.salir.show()
		
	def instrucciones(self):
		self.instrucciones = Instrucciones()
		self.instrucciones.show()
		
	def about(self):
		self.about = About()
		self.about.show()		
    				
	def ver_mapa(self):
		oldstdout = sys.stdout
		File = open('datamap', 'w')
		sys.stdout = File
		
		self.display.clear()
		self.ver_terreno(terreno)
		
		sys.stdout.flush()
		File.close()
		sys.stdout = oldstdout
		File = open('datamap', 'r')
		mapa = File.read()
		File.close()
		self.display.textCursor().insertText(mapa)
		
	def ver_terreno(self, terreno):
		Map = genMap2(terreno)
		
		for n in range(0, len(aviones)):
			if aviones[n].direc == 'e':
				Map[aviones[n].h][aviones[n].x] = '>'
			elif aviones[n].direc == 'w':
				Map[aviones[n].h][aviones[n].x] = '<'
			Map[aviones[n].h+1][aviones[n].x] = n+1 

			if aviones[n].status == 'crashed':			# Si choca
				Map[aviones[n].h][aviones[n].x] = '*'	

		printMap(Map, terreno)
		for n in range(0, len(aviones)):
			print '%d: %s (%s)' % (n+1, aviones[n].__str__(), aviones[n].piloto)

class Opening(QDialog, opening_form):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		QObject.connect(self.pushButton, SIGNAL('clicked()'), self, SLOT('close()'))

class InitialSettings(QDialog, dialoginit_form):
	def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.setupUi(self)
		self.aeronaveComboBox.addItems(['Cessna', 'Embraer', 'Sukhoi'])	
		self.combustibleLineEdit.setText('950')
		self.cargaLineEdit.setText('600')
		self.mapaComboBox.addItems(['genTerr'])
		self.inicioComboBox.addItems(['landed', 'flying'])
		self.inicioComboBox.setCurrentIndex(1)
		QObject.connect(self.buttonBox, SIGNAL('accepted()'), self, SLOT('arranque()'))
		
	@pyqtSlot()
	def arranque(self):
		global vel_aviones
		vel_aviones = {'Cessna' : 450, 'Embraer' : 650, 'Sukhoi' : 1600}
		global player_init
		player_init = {'piloto'	:	str(self.pilotoLineEdit.text()),
			 		   'nombre'	:	str(self.aeronaveComboBox.currentText()),
				 	   'fuel'	:	int(self.combustibleLineEdit.text()),
					   'status'	:	str(self.inicioComboBox.currentText())
					  }
		player_init['Vmax'] = vel_aviones[player_init.get('nombre')]
		if player_init['status'] == 'flying':
			player_init['altitud'] = 400
			player_init['pos'] = 4000
			player_init['potencia'] = 80
			player_init['vel'] = 0.6 * player_init['Vmax']
		else:
			player_init['altitud'] = 0
			player_init['pos'] = 50
			player_init['potencia'] = 0
			player_init['vel'] = 0
			
class Instrucciones(QDockWidget, instrucciones_form):
	def __init__(self):
		QDockWidget.__init__(self)
		self.setupUi(self)
		
class About(QDockWidget, about_form):
	def __init__(self):
		QDockWidget.__init__(self)
		self.setupUi(self)					
			
class DialogExit(QDialog, exit_form):
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		QObject.connect(self.bQuit, SIGNAL('clicked()'), avion1, SLOT('close()'))
		sal = self
		sal.show()		

if __name__ == '__main__':
	app = QApplication(sys.argv)				

	Op = Opening()
	Op.show()
	app.exec_()

	settings_window = InitialSettings()
	settings_window.show()
	app.exec_()	
	
	# Crear mapa		
	terreno = genTerr()
	print 'Terreno creado\n'

	# Crear aviones
	avion1 = VentanaPrincipal(**player_init)
	aviones.append(avion1)

	avion2 = Nave(	altitud=200, pos=10000, status='flying', vel=200, 
					potencia=100, nombre = 'Embraer 200' )
	aviones.append(avion2)

	avion3 = Patrulla(	altitud=400, pos=18000, status='flying', vel= 350, 
						direccion='w', potencia=100, nombre='A-10 Intruder'  )
	aviones.append(avion3)

	print 'Aviones creados\n'

	# Mostrar interfase
	avion1.show()

	# iniciar demonios
	timer = QTimer()
	QObject.connect(timer, SIGNAL('timeout()'), avion1, SLOT('engine()'))
	timer.start(1000)
	 
	app.exec_()				
	timer.stop()
	print 'Saliendo del programa'	
