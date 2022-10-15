from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# Mac user ====================================================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root' + \
                                        '@localhost:3306/skill'
# =============================================================================


# Windows user -------------------------------------------------------------------
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:' + \
#                                         '@localhost:3306/ljms'
# --------------------------------------------------------------------------------
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                        'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)

class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String(100))
    description = db.Column(db.String(100))
    image = db.Column(db.String(20000))

    __mapper_args__ = {
        'polymorphic_identity': 'skill',
    }

    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

######## SKILLS ########
#create skills (C)
@app.route('/skills' , methods=['POST'])
def create_skill():
    data = request.get_json()
    # print(data)
    if not all(key in data.keys() for
            key in ('name', 'description',
                    'image')):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500
    skill = Skill(**data)
    try:
        db.session.add(skill)
        db.session.commit()
        return jsonify(skill.to_dict()), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500


# Read Existing Skills (R)
@app.route("/skills")
def readSkills():
    skillList = Skill.query.all()
    return jsonify(
        {
            "data": [skill.to_dict()
                    for skill in skillList]
        }
    ), 200

# Update Existing Skills (U)
@app.route("/skills/<int:id>", methods=['PUT'])
def updateSkillInformation(id):
    chosenSkill = Skill.query.filter_by(id=id).first()
    if chosenSkill:
        data = request.get_json() 
        if data['name']:
            chosenSkill.name = data['name']
        if data['description']:
            chosenSkill.description = data['description']
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                # "data": chosenSkill.json()
            }
        )

#delete skills (D)
@app.route("/skill", methods=['DELETE'])
def delete_skill():
    data = request.get_json()
    # print(f"data.keys(): {not all(key in data.keys() for key in ('id', 'name2'))}")
    if not all(key in data.keys() for
                # only allows two or more inputs in tuple during checking
            key in ("id", "id")):
        return jsonify({
            "message": "Incorrect JSON object provided."
        }), 500

    try:
        try:
            skill = Skill.query.filter_by(id=data["id"]).one()
        except Exception:
            return jsonify({
            "message": f"Unable to find skill with id: {data['id']}"
            }), 500
        db.session.delete(skill)
        db.session.commit()
        return jsonify(data), 201
    except Exception:
        return jsonify({
            "message": "Unable to commit to database."
        }), 500
    
db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)