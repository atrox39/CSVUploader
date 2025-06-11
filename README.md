# 🗄️ Database CSV Uploader

Una utilidad de línea de comandos en Python para cargar múltiples archivos CSV en una base de datos **SQL Server**. También puedes generar scripts SQL exportables para ejecutar las inserciones manualmente.

## 🚀 Características

- Soporte para múltiples archivos CSV.
- Inserción directa en SQL Server mediante ODBC.
- Exportación opcional de scripts SQL.
- Registro de errores en logs.
- Configuración por archivo `.env`.

## 📦 Requisitos

- Python 3.7+
- SQL Server (ODBC Driver 17)
- Dependencias Python:

```bash
pip install -r requirements.txt
```

Contenido de `requirements.txt` (sugerido):

```
pypyodbc
python-dotenv
```

## ⚙️ Configuración

Crea un archivo `.env` en el directorio raíz con las siguientes variables:

```env
DB_HOST=localhost
DB_USER=usuario
DB_PASS=contraseña
DB_NAME=nombre_de_base_de_datos
CSV_PATH=csvs
FILE_PATTERN=^.*\.csv$
FILE_SPLITTER=_
```

- `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`: Datos de conexión a la base de datos.
- `CSV_PATH`: Carpeta donde se encuentran los archivos `.csv`.
- `FILE_PATTERN`: Expresión regular para filtrar archivos CSV válidos.
- `FILE_SPLITTER`: Caracter utilizado para extraer el nombre de la tabla desde el nombre del archivo.

### Ejemplo de nombre de archivo

Si el archivo es `clientes_data.csv` y `FILE_SPLITTER` es `_`, el script insertará los datos en la tabla `clientes`.

## 📥 Uso

### Inserción directa a la base de datos

```bash
python main.py
```

### Exportar scripts SQL sin insertar en la base de datos

```bash
python main.py --export true
```

Los scripts se guardarán en la carpeta `scripts/` y los errores en `logs/`.

## 📝 Estructura del proyecto

```
.
├── main.py
├── .env
├── scripts/         # SQLs generados (solo si se usa --export)
├── logs/            # Logs de errores
├── csvs/            # Archivos CSV
└── requirements.txt
```

## 📚 Notas

- Asegúrate de que los nombres de las columnas en los CSV coincidan con los nombres de columnas en la base de datos.
- Este script **no valida tipos de datos** ni estructuras; se recomienda asegurar la calidad de los CSV antes de su ejecución.

## 🛠️ Mejoras futuras

- Validación de tipos de datos.
- Soporte para múltiples delimitadores.
- Modo interactivo o GUI.
