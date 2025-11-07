from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

#Création de l'application Flask
app = Flask(__name__)

# Connexion à la base MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/students_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle Student
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nom": self.nom, "age": self.age}

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()



#Racine de l'API pour tester si le serveur fonctionne
@app.route('/')
def home():
    return "Bienvenue dans l API de gestion des etudiants"

#Lister tous les etudiants
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students]), 200

#Afficher un etudiant à partir de son id
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student is None:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    
    return jsonify(student.to_dict()), 200

#Ajouter un etudiant
@app.route('/addStudent', methods=['POST'])
def add_student():
    data = request.get_json()

    if not data or 'id' not in data or 'nom' not in data or 'age' not in data:
        return jsonify({"error": "Champs manquants (id, nom, age)"}), 400

    #verifier que l'ID est unique 
    if Student.query.get(data['id']):
        return jsonify({"error": f"ID {data['id']} déjà utilisé"}), 400
    
    new_student = Student(id=data['id'], nom=data['nom'], age=data['age'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Étudiant ajouté avec succès", "student": new_student.to_dict()}), 201

#Mettre à jour un étudiant
@app.route('/updateStudent/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    
    if 'nom' in data:
        student.nom = data['nom']
    if 'age' in data:
        student.age = data['age']

    db.session.commit()
    return jsonify({"message": "Étudiant mis à jour avec succès", "student": student.to_dict()}), 200

#Supprimer un étudiant
@app.route('/deleteStudent/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Étudiant non trouvé"}), 404
    
    deleted_student = student.to_dict()
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Étudiant supprimé avec succès", "deleted_student": deleted_student}), 200


if __name__ == "__main__":
    #activer le mode Debug pour voir les erreurs et recharger auto le serveur après chaque modification
    app.run(debug=True)