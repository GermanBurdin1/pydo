import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Button
import mysql.connector

# Configuration de la connexion à la base de données
db_config = {
    'host': 'localhost',
    'user': 'votre_user',
    'password': '123',
    'database': 'pydo'
}

# Fonction pour se connecter à la base de données
def connect_to_db():
    connection = mysql.connector.connect(**db_config)
    return connection

# Application Tkinter
class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Gestionnaire de Todolist')
        self.geometry("500x500")  # Définit la taille de la fenêtre

        self.listbox = Listbox(self)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.refresh_button = Button(self, text="Rafraîchir la liste", command=self.afficher_taches)
        self.refresh_button.pack()

        self.add_task_button = Button(self, text="Ajouter une tâche", command=self.ajouter_tache)
        self.add_task_button.pack()

        self.start_task_button = Button(self, text="Démarrer une tâche", command=self.demarrer_tache)
        self.start_task_button.pack()

        self.finish_task_button = Button(self, text="Finaliser une tâche", command=self.finaliser_tache)
        self.finish_task_button.pack()

        self.delete_task_button = Button(self, text="Supprimer une tâche", command=self.supprimer_tache)
        self.delete_task_button.pack()

        self.modify_task_button = Button(self, text="Modifier une tâche", command=self.modifier_tache)
        self.modify_task_button.pack()

    def afficher_taches(self):
        self.listbox.delete(0, tk.END)  # Efface la liste actuelle
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT libelle, libelle_etat FROM tache
            INNER JOIN etat ON tache.Id_Etat = etat.Id_Etat
            WHERE libelle_etat IN ('à faire', 'en cours')
        """)
        for (libelle, libelle_etat) in cursor:
            self.listbox.insert(tk.END, f"{libelle} - {libelle_etat}")
        cursor.close()
        conn.close()

    def ajouter_tache(self):
        libelle = simpledialog.askstring("Ajouter Tâche", "Entrez le libellé de la tâche:")
        date_fixee = simpledialog.askstring("Ajouter Tâche", "Entrez la date fixée (YYYY-MM-DD):")
        if libelle and date_fixee:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tache (libelle, date_creation, date_fixee, id_Etat)
                VALUES (%s, NOW(), %s, (SELECT Id_Etat FROM etat WHERE libelle_etat = 'à faire'))
            """, (libelle, date_fixee))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Succès", "Tâche ajoutée avec succès.")
            self.afficher_taches()

    def demarrer_tache(self):
        selected = self.listbox.get(self.listbox.curselection())
        libelle = selected.split(" - ")[0]
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute(""" 
            UPDATE tache SET Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'en cours') 
            WHERE libelle = %s AND Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'à faire') 
        """, (libelle,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Tâche démarrée.")
        self.afficher_taches()

    def finaliser_tache(self):
        selected = self.listbox.get(self.listbox.curselection())
        libelle = selected.split(" - ")[0]
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tache SET Id_Etat = (SELECT Id_Etat FROM etat WHERE libelle_etat = 'terminée'), date_realisation = NOW()
            WHERE libelle = %s
        """, (libelle,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Succès", "Tâche finalisée.")
        self.afficher_taches()

    def supprimer_tache(self):
        selected = self.listbox.get(self.listbox.curselection())
        libelle = selected.split(" - ")[0]
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM tache WHERE libelle = %s
        """, (libelle,))
        conn.commit()
        cursor.close()
        conn.close()

    def modifier_tache(self):
        selected = self.listbox.get(self.listbox.curselection())
        libelle_original = selected.split(" - ")[0]
        
        libelle_nouveau = simpledialog.askstring("Modifier Tâche", "Entrez le nouveau libellé de la tâche:", initialvalue=libelle_original)
        date_fixee_nouveau = simpledialog.askstring("Modifier Tâche", "Entrez la nouvelle date fixée (YYYY-MM-DD) ou laissez vide si inchangée:")
        
        if libelle_nouveau and date_fixee_nouveau:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tache SET libelle = %s, date_fixee = %s WHERE libelle = %s
            """, (libelle_nouveau, date_fixee_nouveau, libelle_original))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Succès", "Tâche modifiée.")
            self.afficher_taches()
        elif libelle_nouveau:
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tache SET libelle = %s WHERE libelle = %s
            """, (libelle_nouveau, libelle_original))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Succès", "Tâche modifiée.")
            self.afficher_taches()

# vérification si l'appli est executée directement
if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()




