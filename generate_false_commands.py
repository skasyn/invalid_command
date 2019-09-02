#!/usr/bin/python3

import sys
import random
import numpy as np
import pandas as pd

error_fields_old = ['contact.civilite',
             'modeLivraison.adresseLivraison.civilite',
             'modeLivraison.historiques.historiqueAdresseLivraison.valeur.civilite',
             'acheteur.representantLegal.civilite',
             'fichesRetour.modeLivraison.adresseLivraison.civilite',
             'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.civilite',
             'contact.nom',
             'modeLivraison.adresseLivraison.nom',
             'modeLivraison.historiques.historiqueAdresseLivraison.valeur.nom',
             'acheteur.representantLegal.nom',
             'fichesRetour.modeLivraison.adresseLivraison.nom',
             'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.nom',
             'modeLivraison.entiteReseauDistribution.nom',
             'repriseMobile.terminal.nom',
             'contact.prenom',
             'modeLivraison.adresseLivraison.prenom',
             'modeLivraison.historiques.historiqueAdresseLivraison.valeur.prenom',
             'acheteur.representantLegal.prenom',
             'fichesRetour.modeLivraison.adresseLivraison.prenom',
             'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.prenom',
             'adresseFacturation.civilite',
             'adresseFacturation.codePostal',
             'adresseFacturation.nom',
             'adresseFacturation.prenom',
             'adresseFacturation.pays',
             'adresseFacturation.rue',
             'adresseFacturation.ville',
             'adresseFacturation.boitePostale',
             'adresseFacturation.codeNIC',
             'adresseFacturation.complementAdresse1',
             'adresseFacturation.complementAdresse2',
             'adresseFacturation.dateCreation',
             'adresseFacturation.raisonSociale',
             'adresseFacturation.siren',
             'adresseFacturation.validGcp',
             'reseauLivraison',
             'modeLivraison.reseauLivraison.nomCommercial',
             'fichesRetour.modeLivraison.reseauLivraison.nomCommercial',
             'contexteContractuel.compteBancaire.iban',
             'compteBancaire.iban',
             'comptesPayeursCrees.compteBancaire.iban',
             'repriseMobile.iban',
             'email',
             'contact.email',
             'demandeDuplicatas.email',
             'identifiantAcces.coordonneesValidation.email',
             'acheteur.dateDeNaissance',
             'acheteur.dejaClient',
             'acheteur.comptePayeurAchat.noCompte',
             'acheteur.estProspect',
             'acheteur.departementNaissance',
             'acheteur.representantLegal.departementNaissance',
             'contact.departementNaissance',
             'typeParcours',
             'modeLivraison.entiteReseauDistribution.fermeturesExceptionnelles.plagesHoraires.debut',
             'modeLivraison.entiteReseauDistribution.fermeturesExceptionnelles.plagesHoraires.fin',
             'modeLivraison.entiteReseauDistribution.horairesHebdomadaires.plagesHoraires.debut',
             'modeLivraison.entiteReseauDistribution.horairesHebdomadaires.plagesHoraires.fin',
             'modeLivraison.entiteReseauDistribution.ouverturesExceptionnelles.plagesHoraires.debut',
             'modeLivraison.entiteReseauDistribution.ouverturesExceptionnelles.plagesHoraires.fin',
             'contexteContractuel.demandePortabilite.msisdnPorte',
             'acteurCreateur.noPersonne',
             'acteurCreateur.type',
             'acteurCreateur.entiteReseauDistribution.codeEnseigne',
             'acteurCreateur.entiteReseauDistribution.codePointVente',
             'acteurCreateur.login',
             'acteurCreateur.matricule',
             'modeLivraison.adresseLivraison.civilite',
             'modeLivraison.adresseLivraison.codePostal',
             'modeLivraison.adresseLivraison.nom',
             'modeLivraison.adresseLivraison.numero',
             'modeLivraison.adresseLivraison.pays',
             'modeLivraison.adresseLivraison.prenom',
             'modeLivraison.adresseLivraison.rue',
             'modeLivraison.adresseLivraison.ville',
             'fichesRetour.modeLivraison.adresseLivraison.civilite',
             'fichesRetour.modeLivraison.adresseLivraison.codePostal',
             'fichesRetour.modeLivraison.adresseLivraison.complementAdresse1',
             'fichesRetour.modeLivraison.adresseLivraison.complementAdresse2',
             'fichesRetour.modeLivraison.adresseLivraison.nom',
             'fichesRetour.modeLivraison.adresseLivraison.numero',
             'fichesRetour.modeLivraison.adresseLivraison.pays',
             'fichesRetour.modeLivraison.adresseLivraison.prenom',
             'fichesRetour.modeLivraison.adresseLivraison.raisonSociale',
             'fichesRetour.modeLivraison.adresseLivraison.rue',
             'fichesRetour.modeLivraison.adresseLivraison.siren',
             'fichesRetour.modeLivraison.adresseLivraison.ville',
             'modeLivraison.adresseLivraison.codeNIC',
             'modeLivraison.adresseLivraison.complementAdresse1',
             'modeLivraison.adresseLivraison.complementAdresse2',
             'modeLivraison.adresseLivraison.dateCreation',
             'modeLivraison.adresseLivraison.raisonSociale',
             'modeLivraison.adresseLivraison.siren',
             'modeLivraison.historiques.historiqueAdresseLivraison.valeur.ville',
             'adresseInstallation.ville',
             'fichesRetour.modeLivraison.adresseLivraison.ville',
             'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.ville',
             'repriseMobile.adresseEnvoi.ville',
             'modeLivraison.historiques.historiqueAdresseLivraison.valeur.codePostal',
             'adresseInstallation.codePostal',
             'fichesRetour.modeLivraison.adresseLivraison.codePostal',
             'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.codePostal',
             'repriseMobile.adresseEnvoi.codePostal'
             ]

error_fields = ['acheteur.representantLegal.civilite',
                'adresseFacturation.civilite',
                'contact.civilite',
                'fichesRetour.modeLivraison.adresseLivraison.civilite',
                'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.civilite',
                'modeLivraison.adresseLivraison.civilite',
                'modeLivraison.historiques.historiqueAdresseLivraison.valeur.civilite',
                'utilisateur.civilite',
                'acheteur.representantLegal.nom',
                'acheteur.representantLegal.prenom',
                'adresseFacturation.nom',
                'adresseFacturation.prenom',
                'contact.nom',
                'contact.prenom',
                'fichesRetour.modeLivraison.adresseLivraison.nom',
                'fichesRetour.modeLivraison.adresseLivraison.prenom',
                'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.nom',
                'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.prenom',
                'modeLivraison.adresseLivraison.nom',
                'modeLivraison.adresseLivraison.prenom',
                'modeLivraison.entiteReseauDistribution.nom',
                'modeLivraison.historiques.historiqueAdresseLivraison.valeur.nom',
                'modeLivraison.historiques.historiqueAdresseLivraison.valeur.prenom',
                'repriseMobile.terminal.nom',
                'utilisateur.nom',
                'utilisateur.prenom',
                'adresseFacturation.boitePostale',
                'adresseFacturation.civilite',
                'adresseFacturation.codeNIC',
                'adresseFacturation.codePostal',
                'adresseFacturation.complementAdresse1',
                'adresseFacturation.complementAdresse2',
                'adresseFacturation.dateCreation',
                'adresseFacturation.nom',
                'adresseFacturation.numero',
                'adresseFacturation.pays',
                'adresseFacturation.prenom',
                'adresseFacturation.raisonSociale',
                'adresseFacturation.rue',
                'adresseFacturation.siren',
                'adresseFacturation.validGcp',
                'adresseFacturation.ville',
                'fichesRetour.modeLivraison.reseauLivraison.nomCommercial',
                'modeLivraison.reseauLivraison.nomCommercial',
                'reseauLivraison',
                'compteBancaire.iban',
                'comptesPayeursCrees.compteBancaire.iban',
                'contexteContractuel.compteBancaire.iban',
                'repriseMobile.iban',
                'acheteur.dejaClient',
                'contact.email',
                'coordonnees.email',
                'demandeDuplicatas.email',
                'email',
                'identifiantAcces.coordonneesValidation.email',
                'pointsAcces.inscriptionAnnuaireUniversel.adresseElectronique.email',
                'utilisateur.adresseElectronique.email',
                'acheteur.dateDeNaissance',
                'acheteur.comptePayeurAchat.noCompte',
                'acheteur.estProspect',
                'acheteur.departementNaissance',
                'acheteur.representantLegal.departementNaissance',
                'contact.departementNaissance',
                'typeParcours',
                'modeLivraison.entiteReseauDistribution.fermeturesExceptionnelles.plagesHoraires.debut',
                'modeLivraison.entiteReseauDistribution.fermeturesExceptionnelles.plagesHoraires.fin',
                'modeLivraison.entiteReseauDistribution.horairesHebdomadaires.plagesHoraires.debut',
                'modeLivraison.entiteReseauDistribution.horairesHebdomadaires.plagesHoraires.fin',
                'modeLivraison.entiteReseauDistribution.ouverturesExceptionnelles.plagesHoraires.debut',
                'modeLivraison.entiteReseauDistribution.ouverturesExceptionnelles.plagesHoraires.fin',
                'contexteContractuel.demandePortabilite.msisdnPorte',
                'acteurCreateur.entiteReseauDistribution.codeEnseigne',
                'acteurCreateur.entiteReseauDistribution.codePointVente',
                'acteurCreateur.login',
                'acteurCreateur.matricule',
                'acteurCreateur.noPersonne',
                'acteurCreateur.type',
                'fichesRetour.modeLivraison.adresseLivraison.civilite',
                'fichesRetour.modeLivraison.adresseLivraison.codePostal',
                'fichesRetour.modeLivraison.adresseLivraison.complementAdresse1',
                'fichesRetour.modeLivraison.adresseLivraison.complementAdresse2',
                'fichesRetour.modeLivraison.adresseLivraison.nom',
                'fichesRetour.modeLivraison.adresseLivraison.numero',
                'fichesRetour.modeLivraison.adresseLivraison.pays',
                'fichesRetour.modeLivraison.adresseLivraison.prenom',
                'fichesRetour.modeLivraison.adresseLivraison.rue',
                'fichesRetour.modeLivraison.adresseLivraison.ville',
                'modeLivraison.adresseLivraison.civilite',
                'modeLivraison.adresseLivraison.codeNIC',
                'modeLivraison.adresseLivraison.codePostal',
                'modeLivraison.adresseLivraison.complementAdresse1',
                'modeLivraison.adresseLivraison.complementAdresse2',
                'modeLivraison.adresseLivraison.dateCreation',
                'modeLivraison.adresseLivraison.nom',
                'modeLivraison.adresseLivraison.numero',
                'modeLivraison.adresseLivraison.pays',
                'modeLivraison.adresseLivraison.prenom',
                'modeLivraison.adresseLivraison.raisonSociale',
                'modeLivraison.adresseLivraison.rue',
                'modeLivraison.adresseLivraison.siren',
                'modeLivraison.adresseLivraison.ville',
                'adresseFacturation.ville',
                'adresseInstallation.ville',
                'fichesRetour.modeLivraison.adresseLivraison.ville',
                'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.ville',
                'modeLivraison.adresseLivraison.ville',
                'modeLivraison.historiques.historiqueAdresseLivraison.valeur.ville',
                'pointsAcces.inscriptionAnnuaireUniversel.adresseDeclaree.ville',
                'repriseMobile.adresseEnvoi.ville',
                'adresseFacturation.codePostal',
                'adresseInstallation.codePostal',
                'fichesRetour.modeLivraison.adresseLivraison.codePostal',
                'fichesRetour.modeLivraison.historiques.historiqueAdresseLivraison.valeur.codePostal',
                'modeLivraison.adresseLivraison.codePostal',
                'modeLivraison.historiques.historiqueAdresseLivraison.valeur.codePostal',
                'repriseMobile.adresseEnvoi.codePostal',
                ]

def main(filename):
    df = pd.read_csv(filename, low_memory=False)
    print(df)
    return 0

    total_row = len(df.index) - 2
    try:
        valid, invalid = df['label'].value_counts()
    except ValueError:
        valid = total_row
        invalid = 0 #ou mettre une valeur negative par exemple pr le CP
    nb_to_falsify = int(total_row / 2 - invalid)
    print('The file contains currently %d valid and %d invalid commands' % (valid, invalid))
    print('Generating... Please wait\n')
    i = 0
    while i < nb_to_falsify:
    #while i < 5000:
        row_to_falsify = random.randint(0, total_row - 1)
        while (df.loc[row_to_falsify]['label'] == 0):
            row_to_falsify = random.randint(0, total_row + 1)
        random_field = random.randint(0, len(error_fields) - 1)
        if pd.isnull(df.loc[row_to_falsify, error_fields[random_field]]) == False:
            if (i % 500 == 0):
                print('%d/%d have been processed...' % (i, nb_to_falsify))
            try:
                df.at[row_to_falsify, error_fields[random_field]] = ''
            except ValueError:
                df.at[row_to_falsify, error_fields[random_field]] = np.nan
            df.at[row_to_falsify, 'label'] = 0
            i += 1
    valid, invalid = df['label'].value_counts()
    df.to_csv(filename, index=False)
    print('\033[92mFinished ! The file contains now %d valid and %d invalid commands.' % (valid, invalid))

def usage(argv):
    if len(argv) != 2:
        print('Usage:\n%s [filename]' % argv[0])
        exit(1)

if __name__ == '__main__':
    usage(sys.argv)
    main(sys.argv[1])
