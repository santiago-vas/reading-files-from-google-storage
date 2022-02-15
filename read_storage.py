import pandas

GCS_projectName='nombre_proyecto'
GCS_bucketName ='nombre_bucket


crdl = service_account.Credentials.from_service_account_file(f"{ruta}/credenciales_personales.json")
client = storage.Client(project=GCS_projectName,credentials=crdl)


def GCS_read_kml(tipo_mapa,Id):
    kml_file=f"{nombre_archivo}.kml"
    bucket = client.get_bucket(GCS_bucketName)
    blob = bucket.get_blob('temp/archivos_KML/'+kml_file)     #--------------- lectura archivo unico de poligonos del cliente por storage
    data = blob.download_as_string()

    # -------------------------------------- archivos temporales
    tmp_kml = tempfile.TemporaryFile('w+t')
    tmp_kml.write(data.decode('UTF-8'))
    tmp_kml.seek(0)
    # --------------------------------------

    # LECTURA INMEDIATA DEL ARCHIVO GUARDO ----- para convertirlo a topojson
    gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
    df = gpd.read_file(tmp_kml, driver='KML').reset_index(drop=True)
    # --------------------------------------
    tmp_kml.close()
    # --------------------------------------
    try:
        df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
    except:
        print('el dataframe contiene las varaibles correctas geometry')

    df = gpd.GeoDataFrame( df, geometry=df.geometry)

    try:
        df.geometry = convert_3D_2D(df.geometry) # new geodf with 2D geometry series
        print('el archivo trae poligonos Z y se necesitan cambiar de 3D a 2D')
    except:
        print('el archivo viene con formatos correctos 2D')

    df=df.rename(columns={'Name':'polyg_name'})
    df.plot()
    
    # guardar archivo KML- TOPOJSON en GCS
    tj = topojson.Topology(df, prequantize=False, topology=True)

    return df,tj
