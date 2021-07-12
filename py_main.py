
# ----- Initial imports ----- #
# import kivy

import os

import cv2
from kivy import Config

# ----- Solves issues with OpenGL and old graphics cards ----- #
#try:
#	os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
#	Config.set('graphics', 'multisamples', '0')
#except:
#	pass

# ----- Window configuration ----- #
from kivy.clock import Clock

Config.set('graphics', 'resizable', True)
#Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'window_state', 'maximized')
#Config.set('graphics', 'width', 1000)
#Config.set('graphics', 'height', 600)

# ----- Imports ----- #
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
 
# ----- Importing Modules ----- #
import base_dados
from py_cadastro import TCadastro
from py_principal import TPrincipal, ResPesquisaWid 

# ----- Create Directories ----- #
try:
	os.mkdir(os.path.expanduser("~/Documents/Projeto Leticia"))
	os.mkdir(os.path.expanduser("~/Documents/Projeto Leticia/faces"))
	os.mkdir(os.path.expanduser("~/Documents/Projeto Leticia/DataBase"))
except:
	pass

# ----- Database Path ----- #
path_base_dados = os.path.expanduser(
	"~/Documents/Projeto Leticia/DataBase/DBProjetoLeticia.db")

# ----- Create Database ----- #
base_dados.cria_basedados(path_base_dados)

# ----- Application start ----- #
# ----- Window management class ----- #
class GerenciadorTelas(ScreenManager):
	def __init__(self):
		super().__init__()

		# --- Instantiate classes --- #
		self.tprincipal = TPrincipal()
		self.tcadastro = TCadastro() 
		self.respesquisawid = ResPesquisaWid()

		# --- Place the window classes in the ScreenManager --- #
		self.add_widget(self.tprincipal)
		self.add_widget(self.tcadastro) 

		# --- Controls search results widget on the main screen --- #
		self.cont_res_pesquisa = 0  # Controla wid dos resultados de pesquisa I \ O


	# ----- Place widget with the search result on the main screen----- #
	def resultado_final_pesquisa(self, texto_nome):

		if self.cont_res_pesquisa == 1:
			self.close_wid()
		
		if self.cont_res_pesquisa == 0:
			self.tprincipal.add_widget(self.respesquisawid)
			self.respesquisawid.dados_usuario(texto_nome)
			self.cont_res_pesquisa = 1


	# ----- Remove widget with the search result on the main screen ----- #
	def close_wid(self):

		self.tprincipal.remove_widget(self.respesquisawid)
		self.cont_res_pesquisa = 0

# --- Classe App --- #
class Kv_Main(App):

	title = 'Registration and Recognition'
	icon = 'ImagesApp/logo.png'

	def build(self):
		return GerenciadorTelas()


if __name__ == '__main__':
	Kv_Main().run()

