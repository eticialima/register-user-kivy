# ------------------------------------------------- #
# --- Main Screen, user maintenance
# ------------------------------------------------- #

# ----- Importing Modules ----- #
import base_dados

# ----- Importações ----- #
import os
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout


class TPrincipal(Screen):

    def __init__(self):
        super().__init__()

        self.contp = 0  # Controls wid to search I \ O
        self.tipo_acao_pesq = None  # Variable of the desired action
        self.ids.btn_pesquisa.disabled = False

        self.res_pesquisa_wid = ResPesquisaWid()


    # ----- Clears the search form widgets ----- #
    def limpa_widpesquisa(self):

        self.ids.input_pesquisa.focus = True
        self.ids.input_pesquisa.text = ''
        self.ids.box_scrollwid.clear_widgets()
        self.ids.btn_pesquisa.disabled = False
        self.contp = 0


    def pesquisa_usuario(self):

        self.input_pesquisa = self.ids.input_pesquisa.text

        if self.input_pesquisa != '':

            self.ids.input_pesquisa.text = ''

            base_dados.pesquisa(self.input_pesquisa)

            for res in base_dados.retorno_cursor:

                self.ids.box_scrollwid.add_widget(ScroolWidChild(str(res[1])))

                self.contp = 1

                # ----- Disables the save button ----- #
                self.ids.btn_pesquisa.disabled = True
                # self.ids.btn_pesquisa.background_disabled_normal = 'Images/btn_azulDisable60.png'

            base_dados.retorno_cursor = []


# ----- Search results ----- #
class ScroolWidChild(Button):

    def __init__(self, texto):
        super().__init__()

        self.text = '{}'.format(texto)


# ----- Scrollview for search results ----- #
class Scrollwid(ScrollView):
    pass


# ----- Wid Choose search result ----- #
class ResPesquisaWid(FloatLayout):
    # pass
    def __init__(self):
        super().__init__()

    
    def dados_usuario(self, texto_nome):
        
        base_dados.pesquisa(texto_nome)

        resultado = base_dados.retorno_cursor

        self.ids.lbl_01.text = str(resultado[0][1])
        self.ids.lbl_02.text = str(resultado[0][2])
        self.ids.lbl_03.text = str(resultado[0][3])
        self.ids.lbl_04.text = str(resultado[0][4])

        inicial_cargo = str(resultado[0][3])[0]
        self.ids.lbl_05.text = f'{inicial_cargo.upper()} - 000{str(resultado[0][0])}'
        
        cpf = str(resultado[0][2])
        path_string = ['~/Documents/Projeto Leticia/faces',]
        path_img01 = os.path.expanduser("{}/{}_1.jpg".format(path_string[0], cpf))
        path_img02 = os.path.expanduser("{}/{}_2.jpg".format(path_string[0], cpf))
        path_img03 = os.path.expanduser("{}/{}_3.jpg".format(path_string[0], cpf))
        path_img04 = os.path.expanduser("{}/{}_4.jpg".format(path_string[0], cpf))


        self.ids.img01.source = path_img01
        self.ids.img02.source = path_img02
        self.ids.img03.source = path_img03
        self.ids.img04.source = path_img04

        base_dados.retorno_cursor = []


class WidLabelResultados(Label):
    pass


class WidLabelTexto(Label):
    pass

#     def resultado_pesq(self, texto):

#         conexao = sqlite3.connect(db_path)
#         cursor = conexao.cursor()

#         cursor.execute(''' SELECT IDARQPASS, NOME, CPF, RG, DATANASC, HISTORICO,
#                             CERTINASC, GRUPO, NUMGRUPO, NUM_NO_GRUPO
#                             FROM ARQUIVOPASS
#                             WHERE NOME = '{}' '''.format(texto))

#         for res in cursor:

#             self.ids.lbl_01.text = str(res[1])
#             self.ids.lbl_02.text = str(res[4])
#             self.ids.lbl_03.text = str(res[2])
#             self.ids.lbl_04.text = str(res[3])

#             if res[5] == 'True':
#                 self.ids.lbl_05.text = 'Sim'
#             if res[5] == 'False':
#                 self.ids.lbl_05.text = 'Não'
#             if res[6] == 'True':
#                 self.ids.lbl_06.text = 'Sim'
#             if res[6] == 'False':
#                 self.ids.lbl_06.text = 'Não'

#             self.ids.lbl_07.text = '{} - {}'.format(str(res[7]), str(res[8]))
#             self.ids.lbl_08.text = str(res[9])
#             self.ids.lbl_09.text = 'AP.{}'.format(str(res[0]))

#         conexao.close()

