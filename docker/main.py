import json

from flask import Flask, Response, request

from hwsd_provider.object.db_connection import DbConnection
from hwsd_provider.tools import retrieve_soil_composition, retrieve_mu_global_from_raster_by_zone
from src.hwsd_provider.tools import aggregate_soil_data


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
            soil_data_list = retrieve_soil_composition((lat, long), db_connection=db_connection)
            return Response(response=json.dumps([soil_data.to_dict() for soil_data in soil_data_list], sort_keys=True,
                                                ensure_ascii=False),
                            mimetype='application/json')
        except Exception as err:
            return Response(
                response=json.dumps({"error": str(err)}, sort_keys=True, ensure_ascii=False),
                mimetype='application/json', status=500
            )

    @app.route('/soil_data_aggregate', methods=['GET'])
    def get_soil_data_aggregate():
        arguments = request.args

        try:
            lat = float(arguments.get('lat'))
            long = float(arguments.get('long'))
            soil_data_list = retrieve_soil_composition((lat, long), db_connection=db_connection)
            soil_data_mean = aggregate_soil_data(soil_data_list)
            return Response(response=json.dumps(soil_data_mean.to_dict(), sort_keys=True,
                                                ensure_ascii=False),
                            mimetype='application/json')
        except Exception as err:
            return Response(
                response=json.dumps({"error": str(err)}, sort_keys=True, ensure_ascii=False),
                mimetype='application/json', status=500
            )

    @app.route('/mu_global_by_zone', methods=['GET'])
    def get_mu_global_by_zone():
        arguments = request.args

        try:
            geojson = arguments.get('geojson')
            mu_globals_list = retrieve_mu_global_from_raster_by_zone(json.loads(geojson))
            return Response(response=json.dumps(mu_globals_list, sort_keys=True,
                                                ensure_ascii=False),
                            mimetype='application/json')
        except Exception as err:
            return Response(
                response=json.dumps({"error": str(err)}, sort_keys=True, ensure_ascii=False),
                mimetype='application/json', status=500
            )

    app.run(host=host, port=port)


if __name__ == '__main__':
    launch()
