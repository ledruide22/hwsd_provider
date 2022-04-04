import json

from flask import Flask, Response, request


from hwsd_provider.tools import retrieve_soil_composition
from hwsd_provider.object.db_connection import DbConnection


def launch(port="8180", host="0.0.0.0"):
    app = Flask(__name__)
    db_connection = DbConnection(is_permanent=True)
    db_connection.open_connection()

    @app.route('/')
    def status():
        return "READY TO RETURN HWSD DATA"

    @app.route('/soil_data', methods=['GET'])
    def get_soil_data():
        arguments = request.args

        try:
            lat = float(arguments.get('lat'))
            long = float(arguments.get('long'))
            soil_data_list = retrieve_soil_composition([(lat, long)], db_connection=db_connection)
            soil_data = soil_data_list[0]
            return Response(response=json.dumps(soil_data.to_dict(), sort_keys=True, ensure_ascii=False),
                            mimetype='application/json')
        except Exception as err:
            return Response(
                response=json.dumps({"error": str(err)}, sort_keys=True, ensure_ascii=False),
                mimetype='application/json', status=500
            )

    app.run(host=host, port=port)


if __name__ == '__main__':
    launch()
