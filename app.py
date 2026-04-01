from flask import Flask, request, jsonify
from flask_cors import CORS
from pensionado import Pensionado
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

@app.route("/calcular", methods=["POST"])
def calcular():
    try:
        data = request.json
        logging.info(f"Datos recibidos: {data}")

        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400

        if "opciones" not in data or len(data["opciones"]) == 0:
            return jsonify({"error": "Debe enviar opciones"}), 400

        if int(data.get("expectativa", 0)) <= 0:
            return jsonify({"error": "Expectativa inválida"}), 400

        if float(data.get("valorUF", 0)) <= 0:
            return jsonify({"error": "Valor UF inválido"}), 400

        for op in data["opciones"]:
            if "monto" not in op or op["monto"] <= 0:
                return jsonify({"error": "Monto inválido"}), 400

        pen = Pensionado(
            data.get("nombre", ""),
            data.get("apellidos", ""),
            int(data.get("expectativa")),
            float(data.get("valorUF")),
            len(data.get("opciones"))
        )

        resultados = pen.calcular_opciones(data["opciones"])
        comparacion = pen.comparar(resultados)

        return jsonify(comparacion)

    except Exception as e:
        return jsonify({
            "error": "Error en servidor",
            "detalle": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)