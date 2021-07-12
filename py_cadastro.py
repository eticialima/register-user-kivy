# ------------------------------------------------- #
# ---Registration and Photos
# ------------------------------------------------- #

# ----- Importing Modules ----- #
import base_dados
from py_captura_fotos import CapturaFotos, KivyCV

# ----- Imports ----- #
import cv2
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock


class TCadastro(Screen):

	def __init__(self):
		super().__init__()

		# --- Variable that controls the state of the camera 0/1 --- #
		self.estado_da_camera = 0
		# --- Variaveis que guardam os dados do formulário --- #
		self.nome = ''
		self.cpf = ''
		self.cargo = ''
		self.email = ''


	# --- Records form data in variables --- #
	def registra_dados(self):

		self.nome = self.ids.txt_input01.text
		self.cpf = self.ids.txt_input02.text
		self.cargo = self.ids.txt_input03.text
		self.email = self.ids.txt_input04.text


	def inicia_captura(self):

		self.registra_dados()

		if base_dados.confere_cpf(self.cpf) != 'ja_cadastrado':
			texto_formulario = [self.nome, self.cpf, self.cargo, self.email]

			# --- Variable that controls whether the form is filled out --- #
			nao_preenchido = 0

			# --- Checks if the form is completed --- #
			for dados in texto_formulario:
				if dados == '':
					nao_preenchido = 1

					# --- Enables unfilled form warning text --- #
					self.ids.faltam_dados.text = 'Faltam Dados'

			if len(self.cpf) != 11:
				# --- Enables incorrect cpf warning text --- #
				self.ids.faltam_dados.text = 'O Cpf só pode ter 11 digitos'
				nao_preenchido = 1
			
			# --- If the form is filled, turn on the camera and start capturing --- #
			if nao_preenchido == 0:
				self.estado_da_camera = KivyCV(capture=cv2.VideoCapture(0), fps=60)
				self.ids.camera_layout.add_widget(self.estado_da_camera)
				self.ids.faltam_dados.text = ''
				self.ids.inicia_camera.disabled = True
				self.ids.tirar_fotos.disabled = False

		else:
			# --- Warns that the CPF already exists --- #
			self.ids.faltam_dados.text = 'O CPF já está cadastrado'


	def inicia_captura_fotos(self):

		# --- Remove the image capture widget --- #
		self.ids.camera_layout.clear_widgets()
		self.estado_da_camera.capture.release()

		Clock.schedule_once(self.captura_fotos, 1)

	
	def captura_fotos(self, time):	

		fotos = CapturaFotos()
		fotos.fotofaces(self.cpf)
		self.ids.cadastro_usuario.disabled = False


	def mostra_fotos(self, face):
		pass


	# --- Register user in the database --- #
	def cadastra_formulario(self):

		# --- Register user in the database--- #
		base_dados.cadastrar_dados(self.nome, self.cpf, self.cargo, self.email)

		# --- Clear the form, button status and turn off the camera --- #
		self.limpa_formulario()


	# --- Clear the form, button status and turn off the camera --- #
	def limpa_formulario(self):
		self.ids.txt_input01.text = ''
		self.ids.txt_input02.text = ''
		self.ids.txt_input03.text = ''
		self.ids.txt_input04.text = ''
		self.ids.faltam_dados.text = ''

		# --- Button to start camera enabled --- #
		self.ids.inicia_camera.disabled = False
		# --- Button to take photo disabled --- #
		self.ids.tirar_fotos.disabled = True
		# --- Button to register disabled --- #
		self.ids.cadastro_usuario.disabled = True

		# --- Remove the image capture widget --- #
		self.ids.camera_layout.clear_widgets()

		# --- If the camera is on Turn off the camera --- #
		if self.estado_da_camera != 0:
			self.estado_da_camera.capture.release()
			self.estado_da_camera = 0
