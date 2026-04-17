from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/test", methods=["GET"])
def test_route():
    return jsonify({"message":"TEST PASSED FROM API."})

if __name__ == "__main__":
    app.run(port=5328)