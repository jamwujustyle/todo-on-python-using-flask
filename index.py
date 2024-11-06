from flask import Flask, jsonify, request, abort

app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "title": "buy groceries",
        "description": "carrot, potato, tomato",
        "completed": False,
    },
    {
        "id": 2,
        "title": "complete Python assignment",
        "description": "finish the Flask Api project",
        "completed": False,
    },
]


@app.route("/todos", methods=["GET"])
def get():
    return jsonify(tasks)


@app.route("/todos", methods=["POST"])
def post():
    data = request.get_json()

    if not data or not data.get("title") or not data.get("description"):
        abort(400, description="both title and description are required")

    new_task = {
        "id": len(tasks) + 1,
        "title": data.get("title"),
        "description": data.get("description"),
        "completed": False,
    }

    tasks.append(new_task)
    return jsonify(new_task), 201


@app.route("/todos/<int:id>", methods=["PUT"])
def put(id):
    task = next((task for task in tasks if task["id"] == id), None)

    if task is None:
        print(f"id {id} is not found in tasks")
        abort(404)

    data = request.get_json()

    if not data:
        print("no data was entered")
        abort(400)

    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    task["completed"] = data.get("completed", task["completed"])

    return jsonify(task)


@app.route("/todos/<int:id>", methods=["DELETE"])
def delete(id):
    task = next((task for task in tasks if task["id"] == id), None)
    if task is None:
        print(f"id {id} is not found in tasks")
        abort(404)

    tasks.remove(task)
    return jsonify(task), 204


if __name__ == "__main__":
    app.run(debug=True)
