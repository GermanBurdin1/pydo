import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Configuration de la connexion à la base de données
db_config = {
    'host': 'localhost',
    'user': 'votre_user',
    'password': 'votre_password',
    'database': 'pydo'
}

# Fonction pour se connecter à la base de données
def connect_to_db():
    connection = mysql.connector.connect(**db_config)
    return connection

# 1. Afficher la liste de tâches à faire et en cours
def afficher_taches():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT libelle, libelle_etat FROM tache
        INNER JOIN etat ON tache.Id_Etat = etat.Id_Etat
        WHERE libelle_etat IN ('à faire', 'en cours')
    """)
    for (libelle, libelle_etat) in cursor:
        print(f"{libelle} - {libelle_etat}")
    cursor.close()
    conn.close()

# 2a. Ajouter une nouvelle tâche
def ajouter_tache(libelle, date_fixee):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tache (libelle, date_creation, date_fixee, Id_Etat)
        VALUES (%s, NOW(), %s, (SELECT Id_Etat FROM etat WHERE libelle_etat = 'à faire'))
""", (libelle, date_fixee))
    conn.commit()
    cursor.close()
    conn.close()
print("Tâche ajoutée avec succès.")

def demarrer_tache(libelle):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE tache SET Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'en cours')
WHERE libelle = %s AND Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'à faire')
""", (libelle,))
    
    conn.commit()
    cursor.close()
    conn.close()
print("Tâche démarrée.")

#démarrer un tâche

def demarrer_tache(libelle):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE tache SET Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'en cours')
WHERE libelle = %s AND Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'à faire')
""", (libelle,))
    conn.commit()
    cursor.close()
    conn.close()
print("Tâche démarrée.")

# finaliser une tâche

def finaliser_tache(libelle):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE tache SET Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'terminée'), date_realisation = NOW()
WHERE libelle = %s
""", (libelle,))
    conn.commit()
    cursor.close()
    conn.close()
print("Tâche finalisée.")

# supprimer une tâche

def supprimer_tache(libelle):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM tache WHERE libelle = %s
""", (libelle,))
    conn.commit()
    cursor.close()
    conn.close()
print("Tâche supprimée.")

# bonus

def modifier_tache(libelle_original, libelle_nouveau, date_fixee_nouveau):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""UPDATE tache SET libelle = %s, date_fixee = %s WHERE libelle = %s
""", (libelle_nouveau, date_fixee_nouveau, libelle_original))
    conn.commit()
    cursor.close()
    conn.close()
print("Tâche modifiée.")

# fonction pour afficher le menu

def afficher_menu():
    while True:
        print("\nGestionnaire de Todolist")
        print("1. Afficher les tâches à faire et en cours")
        print("2. Ajouter une nouvelle tâche")
        print("3. Démarrer une tâche")
        print("4. Finaliser une tâche")
        print("5. Supprimer une tâche")
        print("6. Modifier une tâche")
        print("7. Quitter")
        choix = input("Choisissez une option: ")
        if choix == '1':
            afficher_taches()
        elif choix == '2':
            libelle = input("Entrez le libellé de la tâche: ")
            date_fixee = input("Entrez la date fixée (YYYY-MM-DD): ")
            ajouter_tache(libelle, date_fixee)
        elif choix == '3':
            libelle = input("Entrez le libellé de la tâche à démarrer: ")
            demarrer_tache(libelle)
        elif choix == '4':
            libelle = input("Entrez le libellé de la tâche à finaliser: ")
            finaliser_tache(libelle)
        elif choix == '5':
            libelle = input("Entrez le libellé de la tâche à supprimer: ")
            supprimer_tache(libelle)
        elif choix == '6':
            libelle_original = input("Entrez le libellé de la tâche à modifier: ")
            libelle_nouveau = input("Entrez le nouveau libellé de la tâche: ")
            date_fixee_nouveau = input("Entrez la nouvelle date fixée (YYYY-MM-DD) ou laissez vide si inchangée: ")
            modifier_tache(libelle_original, libelle_nouveau, date_fixee_nouveau)
        elif choix == '7':
            print("Fermeture du gestionnaire de Todolist.")
            break
        else:
            print("Option non reconnue, veuillez réessayer.")

    