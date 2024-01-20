from tkcalendar import DateEntry
import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Button, font
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
        self.listbox.configure(bg="#F1EAFF")

        button_font = font.Font(family='Arial', size=10)

        self.refresh_button = Button(self, text="Rafraîchir la liste", command=self.afficher_taches, font = button_font)
        self.refresh_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.refresh_button.configure(bg="#DCBFFF")

        self.add_task_button = Button(self, text="Ajouter une tâche", command=self.ajouter_tache, font = button_font)
        self.add_task_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.add_task_button.configure(bg="#DCBFFF")

        self.add_multiple_tasks_button = Button(self, text="Ajouter Plusieurs Tâches", command=self.ajouter_taches_multiples, font=button_font)
        self.add_multiple_tasks_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.add_multiple_tasks_button.configure(bg="#DCBFFF")


        self.start_task_button = Button(self, text="Démarrer une tâche", command=self.demarrer_tache, font = button_font)
        self.start_task_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.start_task_button.configure(bg="#DCBFFF")

        self.finish_task_button = Button(self, text="Finaliser une tâche", command=self.finaliser_tache, font = button_font)
        self.finish_task_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.finish_task_button.configure(bg="#DCBFFF")

        self.delete_task_button = Button(self, text="Supprimer une tâche", command=self.supprimer_tache, font = button_font)
        self.delete_task_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.delete_task_button.configure(bg="#DCBFFF")

        self.modify_task_button = Button(self, text="Modifier une tâche", command=self.modifier_tache, font = button_font)
        self.modify_task_button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.modify_task_button.configure(bg="#DCBFFF")


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
        libelle = simpledialog.askstring("Ajouter une tâche", "Entrez le libellé de la tâche:")
        if libelle:
            # Création d'une fenêtre top-level pour la sélection de date
            date_window = tk.Toplevel(self)
            date_window.title("Choisir la date")

            # Ajout d'un widget DateEntry
            cal = DateEntry(date_window, width=12, background='darkblue', foreground='white', borderwidth=2)
            cal.pack(padx=10, pady=10)

            # Fonction pour gérer la sélection de date
            def confirm_date():
                date_fixee = cal.get_date()
                if date_fixee:
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
                    date_window.destroy()

            # Bouton pour confirmer la date
            confirm_button = tk.Button(date_window, text="Confirmer", command=confirm_date)
            confirm_button.pack()

    def ajouter_taches_multiples(self):
        def ajouter_tache(libelle, date_fixee, etat):
            conn = connect_to_db()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tache (libelle, date_creation, date_fixee, id_Etat)
                VALUES (%s, NOW(), %s, (SELECT Id_Etat FROM etat WHERE libelle_etat = %s))
            """, (libelle, date_fixee, etat))
            conn.commit()
            cursor.close()
            conn.close()

        def ajouter():
            taches = taches_entry.get("1.0", tk.END).strip().split("\n")
            for tache in taches:
                libelle, date_fixee, etat = tache.split(",")
                ajouter_tache(libelle, date_fixee, etat.strip())
            messagebox.showinfo("Succès", "Tâches ajoutées avec succès.")
            self.afficher_taches()
            add_window.destroy()

        add_window = tk.Toplevel(self)
        add_window.title("Ajouter Plusieurs Tâches")

        tk.Label(add_window, text="Entrez les tâches (format: libellé, YYYY-MM-DD, état):").pack()
        taches_entry = tk.Text(add_window, height=10, width=50)
        taches_entry.pack()

        submit_button = tk.Button(add_window, text="Ajouter Tâches", command=ajouter)
        submit_button.pack()

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




