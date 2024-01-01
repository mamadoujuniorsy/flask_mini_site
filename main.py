from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, static_url_path= '/static')

# Fonction pour créer la table si elle n'existe pas
def create_table():
    conn = sqlite3.connect("Inscription_GLSI.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Fonction pour insérer un nouvel enregistrement
def insert_data(nom, prenom, age):
    conn = sqlite3.connect("Inscription_GLSI.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inscriptions (nom, prenom, age) VALUES (?, ?, ?)", (nom, prenom, age))
    conn.commit()
    conn.close()

# Fonction pour afficher tous les enregistrements
def read_data():
    conn = sqlite3.connect("Inscription_GLSI.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inscriptions")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fonction pour mettre à jour un enregistrement
def update_data(id, nom, prenom, age):
    conn = sqlite3.connect("Inscription_GLSI.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE inscriptions SET nom=?, prenom=?, age=? WHERE id=?", (nom, prenom, age, id))
    conn.commit()
    conn.close()

# Fonction pour supprimer un enregistrement
def delete_data(id):
    conn = sqlite3.connect("Inscription_GLSI.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inscriptions WHERE id=?", (id,))
    conn.commit()
    conn.close()

# Route pour la page d'accueil
@app.route('/')
def home():
    return render_template('index.html', data=read_data())

# Route pour le formulaire d'inscription
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        insert_data(nom, prenom, age)
        return redirect(url_for('home'))
    return render_template('inscription.html')

# Route pour la modification des informations
@app.route('/modification/<int:user_id>', methods=['GET', 'POST'])
def modification(user_id):
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        age = request.form['age']
        update_data(user_id, nom, prenom, age)
        return redirect(url_for('home'))
    user_data = read_data()[user_id-1]
    return render_template('modification.html', user_data=user_data)

# Route pour la suppression d'un inscrit
@app.route('/suppression/<int:user_id>')
def suppression(user_id):
    delete_data(user_id)
    return redirect(url_for('home'))

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
