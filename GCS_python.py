from google.cloud import storage

bucketName = 'bucket_name'
projectName = 'porject-id'

fileName='temp/Zona_Zapiola.kml'

crdl = service_account.Credentials.from_service_account_file('file.json')
client = storage.Client(project=projectName,credentials=crdl)

bucket = client.get_bucket(bucketName)
blob = bucket.get_blob(fileName)     #--------------- lectura archivo unico de poligonos del cliente por storage
data=blob.download_as_string()

type(data),len(data.decode('UTF-8'))

# es necesario GUARDAR UN ARCHIVO TXT para poder leerlo como archivo kml
archivo_kml='contenido_formato_kml.kml'

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

print(type(df))

try:
    df['geometry'] = gpd.GeoSeries.from_wkt(df['geometry'])
except:
    print('el dataframe contiene las varaibles correctas geometry')
    
df = gpd.GeoDataFrame( df, geometry=df.geometry)
df.plot()
df.dtypes



from shapely.geometry import Polygon, MultiPolygon, shape, Point
import geopandas as gp

def convert_3D_2D(geometry):
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo

geodf_2d = gp.GeoDataFrame( df, geometry=df.geometry)
try:
    geodf_2d.geometry = convert_3D_2D(geodf_2d.geometry) # new geodf with 2D geometry series
    print('el archivo trae poligonos Z y se necesitan cambiar de 3D a 2D')
except:
    print('el archivo viene con formatos correctos 2D')
    
geodf_2d=df.rename(columns={'Name':'polyg_name'})
geodf_2d.polyg_name.nunique()
geodf_2d.plot()
geodf_2d
