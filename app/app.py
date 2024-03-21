from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': '127.0.0.1',
    'user': 'user',
    'password': 'password',
    'database': 'appdb'
}

# Route pour enregistrer la tâche dans la base de données
@app.route('/enregistrer_tache', methods=['POST'])
def enregistrer_tache():
    if request.method == 'POST':
        # Récupérer le nom de la tâche depuis le formulaire
        nom_tache = request.form['nom_tache']

        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Exécution de la requête SQL pour insérer la tâche dans la base de données
        sql = "INSERT INTO TODO (libelle) VALUES (%s)"
        cursor.execute(sql, (nom_tache,))

        # Valider la transaction et fermer la connexion à la base de données
        conn.commit()
        conn.close()

        # Redirection vers la page d'accueil une fois que la tâche est créée
        return redirect(url_for('afficher_taches'))

# Route pour supprimer une tâche
@app.route('/supprimer_tache', methods=['POST'])
def supprimer_tache():
    if request.method == 'POST':
        # Récupérer l'ID de la tâche à supprimer depuis le formulaire
        id_tache = request.form['id_tache']

        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Exécution de la requête SQL pour supprimer la tâche de la base de données
        sql = "DELETE FROM TODO WHERE id_todo = %s"
        cursor.execute(sql, (id_tache,))

        # Valider la transaction et fermer la connexion à la base de données
        conn.commit()
        conn.close()

        # Redirection vers la page d'accueil après la suppression de la tâche
        return redirect(url_for('afficher_taches'))

# Route pour afficher les tâches
@app.route('/')
def afficher_taches():
     # Connexion à la base de données
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    cur.execute("SELECT * FROM TODO")
    taches = cur.fetchall()
    cur.close()
    return render_template('taches.html', taches=taches)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)