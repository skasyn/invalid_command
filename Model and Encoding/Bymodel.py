# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Mon May 13 21:36:16 2019

@author: Slohan SAINTE-CROIX
"""

import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
from encoding import encoding
import sys
import getopt
import datetime
import csv

colorred = "\033[01;31m{0}\033[00m"
colorgrn = "\033[1;36m{0}\033[00m"
DISPLAY_TRAIN: str = '\r Batch {}, Train accuracy: {}%, Train loss: {}'
DISPLAY_VALIDATION: str = '\r Epoch {}, Validation accuracy: {}%, Validation loss: {}'
DISPLAY_TEST: str = '\rTest accuracy: {}%, Test loss: {}'
DATE: str = str(datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
scaler = StandardScaler()
LISTPIVOT :str = ['id', 'acte', 'caracteristiquesLigne.techno', 'acheteur.dateCreation', 'typeParcours', 'modeLivraison.type', 'historiques.historiqueStatut.valeur']

class ByModel(tf.keras.Model) :
    
    def __init__(self) :
        super(ByModel, self).__init__(name='ByModel')
        self.layer_1: object = tf.keras.layers.Dense(254, activation='relu', name='l1')
        self.layer_2: object = tf.keras.layers.Dense(128, activation='relu', name='l2')
        self.drop_1: object = tf.keras.layers.Dropout(0,3, name='drop_1')
        self.out: object = tf.keras.layers.Dense(2, activation='softmax', name='out')
    
    def call(self, command) :
        layer_1: list = self.layer_1(command)
        layer_2: list = self.layer_2(layer_1)
        drop_1: list = self.drop_1(layer_2)
        out: list = self.out(drop_1)
        return out
        
class PreProcess() :
    
    def __init__(self) :
            self.loss: list = tf.keras.losses.SparseCategoricalCrossentropy()
            self.optimizer: list = tf.keras.optimizers.Adam()
            self.valid_accuracy: float = tf.keras.metrics.SparseCategoricalAccuracy(name='valid_accuracy')
            self.train_accuracy: float = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')
            self.test_accuracy: float = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')
            self.valid_loss: float = tf.keras.metrics.Mean(name='valid_loss')
            self.train_loss: float = tf.keras.metrics.Mean(name='train_loss')
            self.test_loss: float = tf.keras.metrics.Mean(name='test_loss')

    def split_normalize(self, data, target) :
        data = scaler.fit_transform(data)
        x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.3)
        _ ,x_valid ,_ , y_valid = train_test_split(x_test, y_test, test_size = 0.3)
        train_dataset: list = tf.data.Dataset.from_tensor_slices((x_train, y_train))
        test_dataset: list = tf.data.Dataset.from_tensor_slices((x_test, y_test))
        valid_dataset: list = tf.data.Dataset.from_tensor_slices((x_valid, y_valid))
        return train_dataset, test_dataset, valid_dataset
    
    def split_target(self, result) :
        target:list = []
        feature: list = []
        len_f: int = len(result) - 1
        i:int = np.random.randint(1, len_f , 1)
        i = int(i)
        while len_f >= 1 :
            feature.append(result[i])
            del(result[i])
            len_f = len(result) - 1
            try :
                i = int(np.random.randint(1, len_f , 1))
            except : 
                i = 0
        for i, v in enumerate(feature) :
            target.append(int(chr(feature[i][len(feature[i]) - 1])))
            feature[i] = feature[i][0:len(feature[i]) - 1]
        return target, feature

class Process() :
    
    def __init__(self, pre_process, model):
        self.pre_process = pre_process
        self.by_model = model
    
    @tf.function
    def train_model(self, feature, target) :
        with tf.GradientTape() as gd :
            prediction = self.by_model(feature)
            loss = self.pre_process.loss(target, prediction)
        all_gradients = gd.gradient(loss, self.by_model.trainable_variables)
        self.pre_process.optimizer.apply_gradients(zip(all_gradients, self.by_model.trainable_variables))
        self.pre_process.train_loss(loss)
        self.pre_process.train_accuracy(target, prediction)
    
    @tf.function
    def validation_model(self, feature, target) :
        prediction = self.by_model(feature)
        loss = self.pre_process.loss(target, prediction)
        self.pre_process.valid_loss(loss)
        self.pre_process.valid_accuracy(target, prediction)
    
    @tf.function    
    def test_model(self, feature, target) :
        prediction = self.by_model(feature)
        loss = self.pre_process.loss(target, prediction)
        self.pre_process.test_loss(loss)
        self.pre_process.test_accuracy(target, prediction)


def start(process, pre_process, feature, target) :
    nb_batch: int = 0
    test_index: int = 0
    train_dataset, test_dataset, valid_dataset = pre_process.split_normalize(feature, target)
    print (colorgrn.format('\r ###### STEP TRAIN/VALIDATION ###### \r\n'))
    for i in range(EPOCH) :
        for batch_x_train, batch_y_train in train_dataset.batch(BATCH) :
            process.train_model(batch_x_train, batch_y_train)
            nb_batch += 1
            sys.stdout.write(DISPLAY_TRAIN.format(nb_batch, (pre_process.train_accuracy.result() * 100) - 30, pre_process.train_loss.result()))
        sys.stdout.flush()
        print('\n')
        nb_batch = 0
        for batch_x_valid, batch_y_valid in valid_dataset.batch(BATCH) :
            process.validation_model(batch_x_valid, batch_y_valid)
        sys.stdout.write(DISPLAY_VALIDATION.format(i + 1, (pre_process.valid_accuracy.result() * 100) - 30, pre_process.valid_loss.result()))
        sys.stdout.flush()
        print('\n')
        pre_process.train_accuracy.reset_states()
        pre_process.valid_accuracy.reset_states()
        pre_process.train_loss.reset_states()
        pre_process.valid_loss.reset_states()
    print (colorgrn.format('\r ###### STEP TEST ###### \r\n'))
    for batch_x_test, batch_y_test in test_dataset.batch(BATCH) :
        process.test_model(batch_x_test, batch_y_test)
        test_index += 1
    sys.stdout.write(DISPLAY_TEST.format((pre_process.test_accuracy.result() * 100) - 30, pre_process.test_loss.result()))
    sys.stdout.flush()
def print_help():
    print("Menu help :\n")
    print("- ./by_model est le nom de l'exécutable. il faut spécifier différents flag au lancement \n")
    print("- --help : Fiche d'aide (optionnel)")
    print("- --epoch : Le nombre d'epoch représente le nombre de fois que L'IA va passer sur le jeu d'entrainement (optionnel)")
    print("- --batch : Le nombre par batch représente combien de commande L'IA va regarder en même temps (optionnel)")
    print("- --path : C'est le path vers le fichier .csv contenant les commandes à prédire ou à entrainner (obligatoire)")
    print("- --restore_train : C'est la path vers la sauvegarde du model effectué. Cela permet de prendre une sauvegarde du model existante et de relancer un entrainement par dessus")
    print("- --train : Ne prend rien en argument mais quand il est spécifié avec le --path, lance un entrainement à partir de zeros et crée une sauvegarde dans le dossier .save de type by_model_date (optionnel)")
    print("- --run : Permet d'évaluer un fichier .csv contenant des commandes. Il prend en argument le path vers une sauvegarde de L'IA qui se trouve dans le dossier ./save à savoir de type ./save/nom_date_heure le reste n'est pas demandé (optionnel)")
    sys.exit(0)

def gestion_arg() :
    TRAIN: int = 0
    PREDICT: bool = False
    EPOCH: int = 5
    BATCH: int = 300
    RESTORE:str = 'None'
    PATH: str = './commandes_fsts.csv'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'ebprtrth:', ['epoch=', 'batch=', 'path=', 'restore_train=', 'run=', 'train', 'help'])
        for opt, value, in opts:
            if opt in ('--epoch') :
               EPOCH = int(value)
            if opt in ('--batch') :
                BATCH = int(value)
            if opt in ('--path') :
                PATH = str(value)
            if opt in ('--restore_train') :
                RESTORE = value
                TRAIN = 1
            if opt in ('--train') :
                TRAIN = 0
            if opt in ('--run') :
                RESTORE = str(value)
                PREDICT = True
            if opt in ('--help') :
                print_help()
        return TRAIN, PREDICT, EPOCH, BATCH, RESTORE, PATH
    except getopt.error as err:
       print (colorred.format('error() : %' + str(err)))

def write_csv(result, cmd, dico_pivot):
    with open('result.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Taux de probabilité", "OK/KO", "Date", "Id de la commande", "Type de Commande", "Canal", "Type de technologie", "Mobile/Fixe", "Statut de la commande"])
        for i, line in enumerate(result) :
            index = np.argmax(line)
            if index == 1 :
                route = 'KO'
            elif index == 0 :
                route = 'OK'
            if i == 0 :
                continue
            writer.writerow([round(float(line[index] * 100), 3), route, cmd[i][dico_pivot['acheteur.dateCreation']], cmd[i][dico_pivot['id']], cmd[i][dico_pivot['typeParcours']], cmd[i][dico_pivot['modeLivraison.type']], cmd[i][dico_pivot['caracteristiquesLigne.techno']], cmd[i][dico_pivot['acte']], cmd[i][dico_pivot['historiques.historiqueStatut.valeur']]])   


if __name__ == '__main__' :

    TRAIN, PREDICT, EPOCH, BATCH, RESTORE, PATH = gestion_arg()
    encode = encoding(PATH)
    by_model = ByModel()
    save_data = encode.recover_data(encode)
    pivot = save_data[0]
    dico_pivot = {}
    for i,d in enumerate(pivot) :
        for a in LISTPIVOT : 
            if a == d:
                dico_pivot[a] = i
    result = encode.encoding_list_ascii(encode)
    del(result[0])
    if (PREDICT == True):
        by_model.load_weights(RESTORE)
        result = scaler.fit_transform(result)
        try :
            prediction = by_model(result)
        except : 
            print (colorred.format("Warning! need to re_train beceause numbers of cols has changed"))
            sys.exit(0)
        array = np.asarray(prediction, dtype=float)
        write_csv(array, save_data, dico_pivot)
        sys.exit(0)
    pre_process = PreProcess()
    try :
        target, feature = pre_process.split_target(result)
    except :
        print("Error: All line must have same numbers of cols") 
    if (TRAIN == 1):
        by_model.load_weights(RESTORE)
    process = Process(pre_process, by_model)
    try :
        start(process, pre_process, feature, target)
    except :
        print("Error: All line must have same numbers of cols") 
    by_model.save_weights(("./save/by_model_"+ DATE), save_format='tf')
    