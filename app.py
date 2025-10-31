from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ======= FRONTEND (Swagger UI + YAML) =======
@app.route('/api')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/openapi.yaml')
def serve_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype='text/yaml')


# ======= IN-MEMORY DATA =======
clients = []
policies = []
claims = []
documents = []
users = {"admin": "admin123"}  # jednoduché přihlášení


# ======= AUTH =======
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username in users and users[username] == password:
        token = str(uuid.uuid4())  # fake JWT
        return jsonify({"token": token})
    return jsonify({"code": "AUTH_ERROR", "message": "Neplatné přihlašovací údaje"}), 401


# ======= CLIENTS =======
@app.route('/clients', methods=['GET'])
def get_clients():
    q = request.args.get("q")
    if q:
        filtered = [c for c in clients if q.lower() in c["lastName"].lower()]
        return jsonify(filtered)
    return jsonify(clients)

@app.route('/clients', methods=['POST'])
def create_client():
    data = request.get_json()
    new_client = {
        "id": str(uuid.uuid4()),
        "firstName": data.get("firstName"),
        "lastName": data.get("lastName"),
        "birthDate": data.get("birthDate"),
        "type": data.get("type", "Fyzická osoba"),
        "createdAt": datetime.now().isoformat()
    }
    clients.append(new_client)
    return jsonify(new_client), 201

@app.route('/clients/<id>', methods=['GET'])
def get_client(id):
    client = next((c for c in clients if c["id"] == id), None)
    if not client:
        return jsonify({"code": "NOT_FOUND", "message": "Klient nenalezen"}), 404
    return jsonify(client)

@app.route('/clients/<id>', methods=['PUT'])
def update_client(id):
    client = next((c for c in clients if c["id"] == id), None)
    if not client:
        return jsonify({"code": "NOT_FOUND", "message": "Klient nenalezen"}), 404
    data = request.get_json()
    client.update({
        "firstName": data.get("firstName", client["firstName"]),
        "lastName": data.get("lastName", client["lastName"]),
        "birthDate": data.get("birthDate", client["birthDate"]),
        "type": data.get("type", client["type"])
    })
    return jsonify(client)

@app.route('/clients/<id>', methods=['DELETE'])
def delete_client(id):
    global clients
    clients = [c for c in clients if c["id"] != id]
    return '', 204


# ======= POLICIES =======
@app.route('/policies', methods=['GET'])
def get_policies():
    client_id = request.args.get("clientId")
    if client_id:
        filtered = [p for p in policies if p["insuredId"] == client_id]
        return jsonify(filtered)
    return jsonify(policies)

@app.route('/policies', methods=['POST'])
def create_policy():
    data = request.get_json()
    new_policy = {
        "id": str(uuid.uuid4()),
        "number": data.get("number"),
        "insuredId": data.get("insuredId"),
        "amount": data.get("amount"),
        "lineOfBusiness": data.get("lineOfBusiness"),
        "status": "aktivní",
        "createdAt": datetime.now().isoformat()
    }
    policies.append(new_policy)
    return jsonify(new_policy), 201

@app.route('/policies/<id>', methods=['GET'])
def get_policy(id):
    policy = next((p for p in policies if p["id"] == id), None)
    if not policy:
        return jsonify({"code": "NOT_FOUND", "message": "Pojistka nenalezena"}), 404
    return jsonify(policy)

@app.route('/policies/<id>', methods=['PATCH'])
def update_policy_status(id):
    policy = next((p for p in policies if p["id"] == id), None)
    if not policy:
        return jsonify({"code": "NOT_FOUND", "message": "Pojistka nenalezena"}), 404
    data = request.get_json()
    if "status" in data:
        policy["status"] = data["status"]
    return jsonify(policy)

@app.route('/policies/<id>', methods=['DELETE'])
def delete_policy(id):
    global policies
    policies = [p for p in policies if p["id"] != id]
    return '', 204


# ======= CLAIMS =======
@app.route('/claims', methods=['GET'])
def get_claims():
    status = request.args.get("status")
    if status:
        filtered = [c for c in claims if c["status"] == status]
        return jsonify(filtered)
    return jsonify(claims)

@app.route('/claims', methods=['POST'])
def create_claim():
    data = request.get_json()
    new_claim = {
        "id": str(uuid.uuid4()),
        "policyId": data.get("policyId"),
        "description": data.get("description"),
        "estimatedDamage": data.get("estimatedDamage", 0),
        "payout": 0,
        "status": "nahlášeno",
        "createdAt": datetime.now().isoformat(),
        "photos": []
    }
    claims.append(new_claim)
    return jsonify(new_claim), 201

@app.route('/claims/<id>', methods=['GET'])
def get_claim(id):
    claim = next((c for c in claims if c["id"] == id), None)
    if not claim:
        return jsonify({"code": "NOT_FOUND", "message": "Událost nenalezena"}), 404
    return jsonify(claim)

@app.route('/claims/<id>', methods=['PATCH'])
def update_claim_status(id):
    claim = next((c for c in claims if c["id"] == id), None)
    if not claim:
        return jsonify({"code": "NOT_FOUND", "message": "Událost nenalezena"}), 404
    data = request.get_json()
    if "status" in data:
        claim["status"] = data["status"]
    if "payout" in data:
        claim["payout"] = data["payout"]
    return jsonify(claim)

@app.route('/claims/<id>/documents', methods=['POST'])
def upload_claim_document(id):
    if "file" not in request.files:
        return jsonify({"code": "BAD_REQUEST", "message": "Soubor chybí"}), 400
    file = request.files["file"]
    filename = file.filename
    documents.append({"claimId": id, "fileName": filename})
    return jsonify({"message": f"Soubor {filename} nahrán."}), 201

@app.route('/claims/stats', methods=['GET'])
def claim_stats():
    total = len(claims)
    open_claims = len([c for c in claims if c["status"] != "uzavřeno"])
    closed = len([c for c in claims if c["status"] == "uzavřeno"])
    payout_sum = sum(c.get("payout", 0) for c in claims)
    return jsonify({
        "totalClaims": total,
        "openClaims": open_claims,
        "closedClaims": closed,
        "totalPayout": payout_sum
    })


# ======= DOCUMENTS (global) =======
@app.route('/documents', methods=['GET'])
def get_all_docs():
    return jsonify(documents)


# ======= RUN =======
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
