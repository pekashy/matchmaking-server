import logging
import schemas.find_game as find_game_structs
from flask import Flask, g, jsonify, request
import requestq

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
mq = requestq.MQ()


def create_logger(corr_id: str) -> logging.Logger:
    logger = logging.getLogger(corr_id)
    formatter = logging.Formatter(
        fmt=
        "%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    logger.setLevel(logging.WARNING)
    file_handler = logging.FileHandler("/logs/client.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


@app.route("/find_game", methods=["POST"])
def find_game():
    find_game_request = find_game_structs.RequestMessage.from_dict(
        request.json)
    corr_id = find_game_request.corr_id
    logger = create_logger(corr_id=corr_id)
    mq.send(logger, find_game_request)
    logger.warning("Handling FindGame")
    return find_game_request.to_json()


@app.route("/get_game", methods=["GET"])
def count():
    g.logger.warning("Handling GetGame")
    return jsonify({"Result": "Ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
