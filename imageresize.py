# -*- coding: utf-8 -*-
'''
Autor: Ricardo Antonello 
ricardo@antonello.com.br
www.antonello.com.br
'''

# Importação dos pacotes necessários
from imutils import paths
import numpy as np
import cv2
import os
import imutils
import time 
import datetime

# inicialização de variáveis
#ATENÇÃO!!! Os arquivos dentro de 'origem' devem estar dentro de pelo menos uma pasta
ORIGEM = '.' # nome da pasta com os arquivos. Esta pastsa não será apagada. 
DESTINO = 'redim' # nome da pasta de destino
FORMATO = 'jpg' # formato do arquivo de destino (a função imwrite escolhe o formato baseado ba extensão do arquivo)
LARGURA = 400 # em pixels
#Defina CROP = True e o crop é automático pela menor dimensão da imagem. O crop é feito antes de redimensionar
CROP = True # se true corta a imagem para não perder a proporção

pastas = ([pasta for pasta in os.listdir(ORIGEM) if os.path.isdir(os.path.join(ORIGEM, pasta))])
CLASSES = len(pastas)
print('Número de classes/pastas:', CLASSES)
NUM_IMAGENS = 0
for pasta in pastas:
    conteudo = os.listdir(os.path.join(ORIGEM, pasta)) # acessa o conteúdo da pasta
    print('Pasta', pasta, 'contém', len(conteudo), 'arquivos') # imprime a pasta e a quantidade de arquivos na pasta
    NUM_IMAGENS += len(conteudo)
print('Total:',NUM_IMAGENS,'arquivos')

caminhos = sorted(list(paths.list_images(ORIGEM)))

if not os.path.isdir(DESTINO): # este diretorio não existe
        os.mkdir(DESTINO) # aqui criamos a pasta caso nao exista
        print ('Pasta', DESTINO, 'criada com sucesso!')
        
for i, caminho in enumerate(caminhos):
    img = cv2.imread(caminho) # carrega a imagem
    if CROP:
        ALTURA = LARGURA
        if img.shape[0]>img.shape[1]: #se altura é maior então corta largula
            meio = img.shape[0]//2
            img = img[meio-(img.shape[1]//2):meio+(img.shape[1]//2) , : ]
        else: # se largura é maior então corta altura da imagem
            meio = img.shape[1]//2
            img = img[ :, meio-(img.shape[0]//2):meio+(img.shape[0]//2) ]
    else:
        ALTURA = int(img.shape[0]*(LARGURA/img.shape[1])) # cria altura proporcional
    
    #Redimensiona
    img = cv2.resize(img, (LARGURA, ALTURA)) #redimenciona para LARGURA x ALTURA pixels 
    
    #CRIA A PASTA SE NÃO EXISTIR
    pasta_destino = DESTINO + os.path.sep + caminho.split(os.path.sep)[-2]
    if not os.path.isdir(pasta_destino): # este diretorio não existe
        os.mkdir(pasta_destino) # aqui criamos a pasta caso nao exista
        print ('Pasta', pasta_destino, 'criada com sucesso!')
    nome_destino = '{0:07}'.format((i+1))+'.'+FORMATO

    caminho_destino = os.path.join(pasta_destino, nome_destino)
   
    print('{0:.4}'.format((i+1)/NUM_IMAGENS*100),'% Concluído.',str(i+1),'/',NUM_IMAGENS,':', caminho, ':', caminho_destino)
    cv2.imwrite(caminho_destino,img)
