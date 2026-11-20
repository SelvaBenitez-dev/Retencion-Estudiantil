from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)

RAW = Path(__file__).parent / "Data" / "raw" / "datos_estudiantes.csv"
PROCESSED = Path(__file__).parent / "Data" / "processed"
GRAFICOS = PROCESSED / "graficos"

# Valores válidos de cada columna categórica (la forma correcta de escribirlos).
VALIDOS = {
    "programa": ["Administración de Empresas", "Contaduría Pública", "Derecho", "Psicología",
                 "Ingeniería de Sistemas", "Ingeniería Industrial", "Enfermería", "Diseño Gráfico"],
    "jornada": ["Diurna", "Nocturna", "Fin de semana"],
    "genero": ["Femenino", "Masculino"],
    "ciudad_procedencia": ["Bogotá", "Medellín", "Cali", "Bucaramanga", "Rionegro",
                           "Barranquilla", "Otra ciudad"],
}

DECISIONES = []


def registrar(paso, columna, accion, filas, justificacion):
    """Guarda una decisión para la tabla de decisiones. Ya está escrita: solo úsala."""
    DECISIONES.append({
        "paso": paso, "columna": columna, "accion": accion,
        "filas_afectadas": int(filas), "justificacion": justificacion,
    })


def explorar(df):
    """Paso 1 del Word: primera mirada al dataset.

    Muestra la forma, los tipos y los nulos de cada columna, las estadísticas
    numéricas, y los valores de las columnas programa, jornada, genero y estado.
    Pregunta: ¿alguna columna numérica aparece como texto? ¿Por qué crees que pasa?

    Respuesta: sí. asistencia_pct y horas_trabajo_semana aparecen como texto (str) porque tienen símbolos (%) o guiones (-) dentro.Además, solo con un valor no numérico es suficiente para que Pandas lea toda la columna como texto.
    """
    print("1. Exploración inicial del dataset:")
    # TODO 1: imprimir shape, info(), describe() y value_counts() de las columnas indicadas.
    
    print("\nForma (filas, columnas):", df.shape)
    print("\nTipos de datos y nulos:")
    df.info()
    print("\nEstadísticas de las columnas numéricas:")
    print(df.describe())
    print("\nEstadísticas de promedio_acumulado:")
    print(df["promedio_acumulado"].describe())
    print("\nEstadísticas de edad:")
    print(df["edad"].describe())
    for col in ["programa", "jornada", "genero", "estado"]:
        print(f"Valores de {col}:")
        print(df[col].value_counts(dropna=False))


def auditar(df):
    """Paso 2 del Word: buscar problemas sin corregirlos todavía.

    Revisa: nulos reales, faltantes disfrazados ('-', 999), valores imposibles
    (edad, promedio, horas), duplicados y formatos de fecha.
    Pregunta: ¿cuál de estos problemas afecta más el análisis? ¿Por qué?

    Respuesta: los nulos reales y los faltantes disfrazados afectan más el análisis porque el que la respuesta devuelva un str en lugar de un número, o que haya valores imposibles, puede afectar la interpretación de los datos y la toma de decisiones basada en ellos.
    """
    print("2. Auditoría de problemas en el dataset:")
    # TODO 2: imprimir cada uno de los conteos de problemas.
    # 1. Nulos reales (celdas vacías)
    print("\nNulos reales por columna:")
    print(df.isnull().sum())

    # 2. Faltantes disfrazados (parecen dato, pero significan 'sin dato')
    print("\nGuiones en asistencia_pct:", (df["asistencia_pct"] == "-").sum())
    print("Guiones en horas_trabajo_semana:", (df["horas_trabajo_semana"] == "-").sum())
    print("Valores 999 en distancia_km:", (df["distancia_km"] == 999).sum())

    # 3. Formato inconsistente: números con símbolo
    print("Celdas con % en asistencia_pct:",
          df["asistencia_pct"].str.contains("%", regex=False).sum())

    # 4. Valores imposibles (cada condición entre paréntesis, con | para 'o')
    print("Edades fuera de 15 a 60:", ((df["edad"] < 15) | (df["edad"] > 60)).sum())
    print("Promedios mayores a 5:", (df["promedio_acumulado"] > 5).sum())
    horas = pd.to_numeric(df["horas_trabajo_semana"], errors="coerce")
    print("Horas de trabajo mayores a 100:", (horas > 100).sum())

    # 5. Duplicados (filas idénticas en todas las columnas)
    print("Filas duplicadas:", df.duplicated().sum())

    # 6. Fechas en dos formatos
    print("Fechas en formato DD/MM/AAAA:",
          df["fecha_matricula"].str.contains("/", regex=False).sum())


def convertir_numericos(df):
    """Paso 3 del Word: columnas que deberían ser numéricas, pero llegan como texto.
    
    Pistas: quitar el símbolo % con str.replace; reemplazar '-' por nulo;
    convertir con pd.to_numeric(..., errors="coerce"); reemplazar 999 por nulo en distancia_km.
    Registra cada conversión con registrar().
    """
    print("3. Convertir columnas a numéricas:")
    # TODO 3: convertir asistencia_pct, horas_trabajo_semana y distancia_km a número.
    # asistencia_pct 
    # Parte 1: quitar el símbolo %
    n_pct = df["asistencia_pct"].str.contains("%", regex=False).sum()      # 1. contar
    df["asistencia_pct"] = df["asistencia_pct"].str.replace("%", "", regex=False)  # 2. corregir
    registrar("3. numericos", "asistencia_pct", "quitar el símbolo %", n_pct,     # 3. registrar
              "El % es formato, no dato; mientras exista, la columna no se puede tratar como número.")

    # Parte 2: el guion pasa a nulo y la columna se convierte a número
    n_guion = (df["asistencia_pct"] == "-").sum()
    df["asistencia_pct"] = df["asistencia_pct"].replace("-", np.nan)
    df["asistencia_pct"] = pd.to_numeric(df["asistencia_pct"], errors="coerce")
    registrar("3. numericos", "asistencia_pct", "'-' a nulo y convertir a número", n_guion,
              "El guion es un faltante disfrazado: significa 'sin dato', así que debe ser un nulo real.")

    # horas_trabajo_semana
    n_guion = (df["horas_trabajo_semana"] == "-").sum()
    df["horas_trabajo_semana"] = df["horas_trabajo_semana"].replace("-", np.nan)
    df["horas_trabajo_semana"] = pd.to_numeric(df["horas_trabajo_semana"], errors="coerce")
    registrar("3. numericos", "horas_trabajo_semana", "'-' a nulo y convertir a número", n_guion,
              "El guion impide calcular con la columna; se vuelve nulo y en el paso 8 se pone 0 "
              "a quienes no trabajan (todos los guiones son de estudiantes con trabaja = 'no').")

    # distancia_km 
    # Ya es numérica, pero usa 999 como código de 'sin dato'
    n_999 = (df["distancia_km"] == 999).sum()
    df.loc[df["distancia_km"] == 999, "distancia_km"] = np.nan
    registrar("3. numericos", "distancia_km", "999 a nulo", n_999,
              "999 km es un código de relleno, no una distancia real; si se deja, infla la distancia promedio.")

    # Verificación
    print("Tipos después de convertir:")
    print(df[["asistencia_pct", "horas_trabajo_semana", "distancia_km"]].dtypes)
    print("\nNulos después de convertir:")
    print(df[["asistencia_pct", "horas_trabajo_semana", "distancia_km"]].isnull().sum())

    return df


def unificar_categorias(df):
    """Paso 4 del Word: errores tipográficos en columnas categóricas.

    Pistas: primero df[col].str.strip().str.lower(); después .replace(diccionario)
    con las variantes que encontraste con value_counts(). Los valores correctos están en VALIDOS.
    Pregunta: ¿qué variantes son el mismo valor? ¿Hay alguna que no debas unificar?
    """
    print("\n4. Unificar categorías:")
    # TODO 4: unificar las escrituras de programa, jornada, genero y ciudad_procedencia.
    diccionarios = {
        "programa": {
            "administración de empresas": "Administración de Empresas",
            "contaduría pública": "Contaduría Pública",
            "derecho": "Derecho",
            "psicología": "Psicología",
            "psicologia": "Psicología",                  # variante sin tilde
            "ingeniería de sistemas": "Ingeniería de Sistemas",
            "ingenieria de sistemas": "Ingeniería de Sistemas",  # variante sin tilde
            "ingeniería industrial": "Ingeniería Industrial",
            "enfermería": "Enfermería",
            "diseño gráfico": "Diseño Gráfico",
        },
        "jornada": {
            "diurna": "Diurna",
            "nocturna": "Nocturna",                      # cubre 'nocturna' y 'NOCTURNA '
            "fin de semana": "Fin de semana",
        },
        "genero": {
            "femenino": "Femenino",
            "f": "Femenino",                             # abreviatura
            "masculino": "Masculino",
            "m": "Masculino",                            # abreviatura
        },
        "ciudad_procedencia": {
            "bogotá": "Bogotá",                          # cubre 'BOGOTÁ'
            "bogota": "Bogotá",                          # cubre 'Bogota' y 'bogota '
            "medellín": "Medellín",
            "medellin": "Medellín",                      # cubre 'medellin' y 'Medellin '
            "cali": "Cali",
            "bucaramanga": "Bucaramanga",
            "rionegro": "Rionegro",
            "barranquilla": "Barranquilla",
            "otra ciudad": "Otra ciudad",                # NO se unifica con ninguna ciudad
        },
    }

    for col, diccionario in diccionarios.items():
        antes = df[col].copy()
        df[col] = df[col].str.strip().str.lower()        # 1. normalizar
        df[col] = df[col].replace(diccionario)           # 2. unificar con el diccionario

        cambiadas = (antes.notna() & (antes != df[col])).sum()
        fuera = (df[col].notna() & ~df[col].isin(VALIDOS[col])).sum()

        print(f"\n{col}: {cambiadas} filas corregidas | valores fuera de VALIDOS: {fuera}")
        print(df[col].value_counts(dropna=False))

        registrar("4. categorias", col, "strip + lower + replace con diccionario", cambiadas,
                  "Mayúsculas, espacios y tildes faltantes crean grupos falsos que dividen el mismo valor.")

    return df


def convertir_fechas(df):
    """Paso 5 del Word: fechas escritas en dos formatos.

    Pista: intenta el formato AAAA-MM-DD y luego DD/MM/AAAA, cada uno con errors="coerce",
    y junta los resultados con fillna(). Registra cuántas fechas tenían el segundo formato.
    """
    print("\n5. Convertir fechas:")
    # TODO 5: convertir fecha_matricula a tipo fecha, registrar cuántas
    # 1. Contar ANTES de convertir cuántas fechas vienen en DD/MM/AAAA
    n_latinas = df["fecha_matricula"].str.contains("/", regex=False).sum()

    # 2. Intentar cada formato por separado (lo que no coincide queda como NaT)
    fechas_iso = pd.to_datetime(df["fecha_matricula"], format="%Y-%m-%d", errors="coerce")
    fechas_latinas = pd.to_datetime(df["fecha_matricula"], format="%d/%m/%Y", errors="coerce")

    # 3. Juntar: donde la primera quedó vacía, usar la segunda
    df["fecha_matricula"] = fechas_iso.fillna(fechas_latinas)

    # 4. Verificar
    sin_convertir = df["fecha_matricula"].isnull().sum()
    print("Fechas en formato DD/MM/AAAA convertidas:", n_latinas)
    print("Fechas que quedaron sin convertir:", sin_convertir)
    print("Tipo de la columna:", df["fecha_matricula"].dtype)
    print("Fecha más antigua:", df["fecha_matricula"].min())
    print("Fecha más reciente:", df["fecha_matricula"].max())

    registrar("5. fechas", "fecha_matricula", "convertir DD/MM/AAAA y AAAA-MM-DD a fecha", n_latinas,
              "Con formatos mezclados Pandas no puede leer la columna como fecha; con formato "
              "explícito no se confunden día y mes (03/04 podría ser 3 de abril o 4 de marzo).")

    return df


def eliminar_duplicados(df):
    """Paso 6 del Word: filas repetidas.

    Pregunta: ¿podrían existir dos estudiantes distintos con todos los datos iguales?
    Pista: duplicated() y drop_duplicates(), con reset_index(drop=True).

    Respuesta: no podrían existir dos estudiantes distintos con todos los datos
    iguales, porque id_estudiante los diferenciaría, es el mismo registro cargado dos veces.
    """
    # TODO 6: eliminar duplicados, registrar la decisión y devolver el dataframe.
    
    print("\n6. Eliminar duplicados:")

    filas_antes = len(df)
    n_duplicados = df.duplicated().sum()                 # 1. contar
    df = df.drop_duplicates().reset_index(drop=True)     # 2. eliminar y renumerar

    print("Filas antes:", filas_antes)
    print("Filas duplicadas eliminadas:", n_duplicados)
    print("Filas después:", len(df))
    print("Ids repetidos que quedan:", df["id_estudiante"].duplicated().sum())

    registrar("6. duplicados", "todas", "eliminar filas idénticas", n_duplicados,   # 3. registrar
              "Son filas idénticas incluido el id_estudiante (150 ids repetidos); contarlas "
              "dos veces duplicaría a esos estudiantes en las tasas.")

    return df


def tratar_faltantes(df):
    """Paso 7 del Word: decidir qué hacer con los nulos reales.

    Preguntas:
    - ¿Puedes inventar una nota? ¿Qué pasa si imputas el promedio?
    - Para ciudad o tipo de colegio, ¿conviene eliminar la fila o marcar el dato como 'Sin dato'?
    - motivo_retiro tiene muchos nulos. ¿Son errores? (Pista: ¿para quiénes aplica esa columna?)

     Respuestas:
    - No se puede inventar una nota. Si se imputa el promedio, todos los grupos se
    acercan artificialmente a la media general y se esconden las diferencias.
    - Para ciudad y tipo de colegio conviene marcar 'Sin dato': así no se pierde al
    estudiante en las preguntas que no usan esas columnas.
    - Los nulos de motivo_retiro no son errores: la columna solo aplica a desertores.
    """
    # TODO 7: tratar los nulos de promedio_acumulado, ciudad_procedencia y tipo_colegio.
   
    print("\npaso 7. Tratar faltantes:")

    #  promedio_acumulado: eliminar filas
    n = df["promedio_acumulado"].isnull().sum()
    df = df.dropna(subset=["promedio_acumulado"]).reset_index(drop=True)
    registrar("7. faltantes", "promedio_acumulado", "eliminar filas", n,
              "Una nota no se puede inventar; imputar la media acercaría todos los grupos "
              "al promedio general y escondería las diferencias que se quieren medir.")

    # ── ciudad_procedencia y tipo_colegio: rellenar con 'Sin dato' ─
    for col in ["ciudad_procedencia", "tipo_colegio"]:
        n = df[col].isnull().sum()
        df[col] = df[col].fillna("Sin dato")
        registrar("7. faltantes", col, "rellenar con 'Sin dato'", n,
                  "Es un dato descriptivo; eliminar la fila haría perder al estudiante "
                  "en las demás preguntas, y 'Sin dato' deja claro que la información falta.")

    # motivo_retiro: dejar los nulos (son esperados)
    n = df["motivo_retiro"].isnull().sum()
    desertores_sin_motivo = (df["estado"].eq("desertor") & df["motivo_retiro"].isnull()).sum()
    registrar("7. faltantes", "motivo_retiro", "dejar los nulos", n,
              f"Nulo esperado: la columna solo aplica a desertores, y {desertores_sin_motivo} "
              "desertores la tienen vacía. Activos y graduados no tienen motivo de retiro.")

    # asistencia_pct: dejar los nulos
    n = df["asistencia_pct"].isnull().sum()
    registrar("7. faltantes", "asistencia_pct", "dejar los nulos", n,
              "Es la variable de la pregunta 5; imputarla inventaría la relación que se "
              "quiere medir. Estas filas quedan fuera de los cuartiles.")

    # distancia_km: dejar los nulos
    n = df["distancia_km"].isnull().sum()
    registrar("7. faltantes", "distancia_km", "dejar los nulos", n,
              "No se usa en las cinco preguntas; imputarla no aporta y ocultaría que el dato falta.")

    # Verificación
    print("Filas después de eliminar promedios faltantes:", len(df))
    print("Desertores sin motivo_retiro:", desertores_sin_motivo)
    print("\nNulos que quedan:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    return df


def tratar_imposibles(df):
    """Paso 8 del Word: valores que no pueden existir.

    Preguntas:
    - La escala del promedio es de 0 a 5. ¿Qué harías con un 45?
    - Una edad de 150 años es un error. ¿Qué valor pondrías en su lugar?
    - Si el estudiante no trabaja, ¿cuántas horas de trabajo tiene? ¿Cómo lo aplicas en código?

    Respuestas:
    - Un promedio de 45 en escala 0-5 se convierte en nulo y se elimina la fila, igual que los promedios faltantes: no se puede confirmar en qué escala se registró.
    - Una edad imposible se reemplaza por la mediana de las edades válidas.
    - Si el estudiante no trabaja, sus horas son 0; se aplica con loc y una condición que combina trabaja == 'no' y horas nulas.

    """
    # TODO 8: tratar edad, promedio_acumulado y horas_trabajo_semana, con sus justificaciones.
 
    print("\npaso 8. Tratar imposibles:")

    # edad 
    imposible = (df["edad"] < 15) | (df["edad"] > 60)
    n = imposible.sum()
    df["edad"] = df["edad"].astype("float64")            # para poder guardar nulos
    df.loc[imposible, "edad"] = np.nan                   # 1. marcar como nulo
    mediana_edad = df["edad"].median()                   # 2. mediana SOLO con edades válidas
    df["edad"] = df["edad"].fillna(mediana_edad)         # 3. rellenar
    registrar("8. imposibles", "edad", f"fuera de 15-60 a la mediana ({mediana_edad:.0f})", n,
              "Edades de 12 y 150 años son errores de registro; la mediana de las edades "
              "válidas no se ve afectada por esos extremos.")

    #  promedio_acumulado 
    imposible = df["promedio_acumulado"] > 5
    n = imposible.sum()
    df.loc[imposible, "promedio_acumulado"] = np.nan
    df = df.dropna(subset=["promedio_acumulado"]).reset_index(drop=True)
    registrar("8. imposibles", "promedio_acumulado", "mayores a 5 a nulo y eliminar fila", n,
              "Valores de 45 a 78 son imposibles en la escala 0-5. No se puede confirmar la "
              "escala original, así que se tratan igual que un faltante: una nota no se inventa.")

    # horas_trabajo_semana: regla que depende de otra columna 
    sin_trabajo = (df["trabaja"] == "no") & (df["horas_trabajo_semana"].isnull())
    n = sin_trabajo.sum()
    df.loc[sin_trabajo, "horas_trabajo_semana"] = 0
    registrar("8. imposibles", "horas_trabajo_semana", "nulo con trabaja='no' a 0", n,
              "Quien no trabaja tiene 0 horas de trabajo; todos los guiones originales eran "
              "de estudiantes con trabaja = 'no', así que el guion significaba cero.")

    # horas_trabajo_semana: valores mayores a 100 
    imposible = df["horas_trabajo_semana"] > 100
    n = imposible.sum()
    df.loc[imposible, "horas_trabajo_semana"] = np.nan
    mediana_horas = df.loc[df["trabaja"] == "sí", "horas_trabajo_semana"].median()
    df["horas_trabajo_semana"] = df["horas_trabajo_semana"].fillna(mediana_horas)
    registrar("8. imposibles", "horas_trabajo_semana",
              f"mayores a 100 a la mediana de quienes trabajan ({mediana_horas:.0f})", n,
              "Más de 100 horas semanales no deja tiempo para estudiar ni dormir; la mediana "
              "de quienes trabajan representa el valor típico sin contar los ceros.")

    # Verificación
    print("Filas después del paso 8:", len(df))
    print(df[["edad", "promedio_acumulado", "horas_trabajo_semana"]].describe())
    print("\nNulos que quedan en horas_trabajo_semana:", df["horas_trabajo_semana"].isnull().sum())

    return df


def crear_variables(df):
    """Paso 9 del Word: variables nuevas para el análisis.

    Crea:
    - desertor: True si estado es 'desertor', False si no.
    - cuartil_asistencia: divide asistencia_pct en cuatro grupos iguales con pd.qcut.
    Pregunta: ¿por qué conviene usar cuartiles y no valores exactos de asistencia?

    Respuesta: con valores exactos habría cientos de grupos de pocos estudiantes y sus
    tasas serían inestables. Con cuartiles cada grupo tiene cerca de una cuarta parte
    de los estudiantes, así que la comparación es confiable.
    """
    # TODO 9: crear las columnas desertor y cuartil_asistencia.
    
    print("\npaso 9. Crear variables nuevas:")

    #desertor: True / False 
    df["desertor"] = df["estado"].eq("desertor")
    n_desertores = df["desertor"].sum()
    print(f"Desertores: {n_desertores} de {len(df)} estudiantes "
          f"({df['desertor'].mean():.1%})")
    registrar("9. variables", "desertor", "crear columna True/False", n_desertores,
              "Una columna True/False permite calcular la tasa de deserción con mean(), "
              "porque el promedio de True y False es la proporción de True.")

    #cuartil_asistencia: 4 grupos de tamaño parecido 
    df["cuartil_asistencia"] = pd.qcut(df["asistencia_pct"], 4,
                                       labels=["Q1 (más baja)", "Q2", "Q3", "Q4 (más alta)"])
    n_con_cuartil = df["cuartil_asistencia"].notna().sum()
    print("\nEstudiantes por cuartil:")
    print(df["cuartil_asistencia"].value_counts(dropna=False).sort_index())
    print("\nRango de asistencia de cada cuartil:")
    print(df.groupby("cuartil_asistencia", observed=True)["asistencia_pct"].agg(["min", "max"]))
    registrar("9. variables", "cuartil_asistencia", "crear cuartiles con qcut", n_con_cuartil,
              "Cuatro grupos de tamaño parecido permiten comparar tasas de forma estable; "
              "los estudiantes sin asistencia quedan fuera de los cuartiles.")

    return df


def grafico_faltantes(df):
    """Gráfico 1: mapa de faltantes del dataset original.

    Pista: sns.heatmap(df.isnull(), cbar=False)
    """
    # TODO 10: dibujar, guardar en GRAFICOS / "mapa_faltantes.png" y mostrar.
    plt.figure(figsize=(12, 6))
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="viridis")
    plt.title("Mapa de faltantes del dataset original")
    plt.xlabel("Columna")
    plt.ylabel("Estudiantes (filas)")
    plt.tight_layout()

    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.savefig(GRAFICOS / "mapa_faltantes.png", dpi=120)
    plt.show()


def grafico_distribuciones(antes, despues):
    """Gráfico 2: boxplots de promedio_acumulado y edad, antes y después de limpiar.

    Pregunta: ¿qué cambió en cada distribución? ¿Por qué?
    """
    # TODO 11: dibujar los cuatro boxplots, guardar en GRAFICOS / "distribuciones_antes_despues.png" y mostrar.
    fig, ejes = plt.subplots(2, 2, figsize=(12, 7))

    sns.boxplot(x=antes["promedio_acumulado"], ax=ejes[0, 0], color="salmon")
    ejes[0, 0].set_title("Promedio acumulado: antes")

    sns.boxplot(x=despues["promedio_acumulado"], ax=ejes[0, 1], color="mediumseagreen")
    ejes[0, 1].set_title("Promedio acumulado: después")

    sns.boxplot(x=antes["edad"], ax=ejes[1, 0], color="salmon")
    ejes[1, 0].set_title("Edad: antes")

    sns.boxplot(x=despues["edad"], ax=ejes[1, 1], color="mediumseagreen")
    ejes[1, 1].set_title("Edad: después")

    plt.tight_layout()
    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.savefig(GRAFICOS / "distribuciones_antes_despues.png", dpi=120)
    plt.show()


def grafico_tasa_programa(df):
    """Gráfico 3: tasa de deserción por programa.

    Pista: df.groupby("programa")["desertor"].mean()
    """
    # TODO 12: dibujar la tasa por programa, guardar en GRAFICOS / "tasa_desercion_por_programa.png" y mostrar.
    tasa = df.groupby("programa")["desertor"].mean().sort_values()

    plt.figure(figsize=(10, 6))
    tasa.plot(kind="barh", color="steelblue")
    plt.title("Tasa de deserción por programa")
    plt.xlabel("Proporción de desertores")
    plt.ylabel("")
    plt.tight_layout()

    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.savefig(GRAFICOS / "tasa_desercion_por_programa.png", dpi=120)
    plt.show()


def grafico_tasa_asistencia(df):
    """Gráfico 4: tasa de deserción por cuartil de asistencia.

    Pista: df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()
    """
    # TODO 13: dibujar la tasa por cuartil, guardar en GRAFICOS / "tasa_desercion_por_asistencia.png" y mostrar.
    tasa = df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()

    plt.figure(figsize=(8, 5))
    tasa.plot(kind="bar", color="steelblue", rot=0)
    plt.title("Tasa de deserción por cuartil de asistencia")
    plt.xlabel("Cuartil de asistencia")
    plt.ylabel("Proporción de desertores")
    plt.tight_layout()

    GRAFICOS.mkdir(parents=True, exist_ok=True)
    plt.savefig(GRAFICOS / "tasa_desercion_por_asistencia.png", dpi=120)
    plt.show()


def responder_preguntas(df):
    """Paso 10 del Word: las cinco preguntas de la institución.

    Cada pregunta debe imprimir el resultado con el número de estudiantes por grupo.
    Pregunta 1: ¿Qué programa presenta la tasa de deserción más alta?
    Pregunta 2: ¿Hay diferencia en la deserción entre becados y no becados?
    Pregunta 3: ¿Qué jornada tiene el menor promedio acumulado?
    Pregunta 4: ¿Cuántas materias reprobadas tienen en promedio los desertores frente a los activos?
                (Excluye a los graduados.)
    Pregunta 5: ¿La deserción aumenta conforme baja la asistencia?
                (Usa cuartil_asistencia.)
    """
    # TODO 14: responder las cinco preguntas con groupby() y agg().
     #Pregunta 1: programa con mayor tasa de deserción 
    p1 = (df.groupby("programa")
            .agg(tasa=("desertor", "mean"), estudiantes=("desertor", "size"))
            .sort_values("tasa", ascending=False))
    print("\nPregunta 1: tasa de deserción por programa")
    print(p1.round(3))
    print(f"-> Mayor tasa: {p1.index[0]} ({p1['tasa'].iloc[0]:.1%}, "
          f"{p1['estudiantes'].iloc[0]} estudiantes)")

    # Pregunta 2: becados frente a no becados
    p2 = df.groupby("beca").agg(tasa=("desertor", "mean"), estudiantes=("desertor", "size"))
    print("\nPregunta 2: tasa de deserción según beca")
    print(p2.round(3))
    diferencia = p2.loc["no", "tasa"] - p2.loc["sí", "tasa"]
    print(f"-> Diferencia: {diferencia * 100:.1f} puntos porcentuales")

    # Pregunta 3: jornada con menor promedio acumulado
    p3 = (df.groupby("jornada")
            .agg(promedio=("promedio_acumulado", "mean"),
                 estudiantes=("promedio_acumulado", "size"))
            .sort_values("promedio"))
    print("\nPregunta 3: promedio acumulado por jornada")
    print(p3.round(3))
    print(f"-> Menor promedio: {p3.index[0]} ({p3['promedio'].iloc[0]:.2f})")

    # Pregunta 4: materias reprobadas, desertores frente a activos 
    # Se excluye a los graduados porque no pertenecen a ninguno de los dos grupos.
    sin_graduados = df[df["estado"] != "graduado"]
    p4 = (sin_graduados.groupby("estado")
            .agg(reprobadas=("materias_reprobadas", "mean"),
                 estudiantes=("materias_reprobadas", "size")))
    print("\nPregunta 4: materias reprobadas en promedio (sin graduados)")
    print(p4.round(2))
    print("Graduados excluidos:", (df["estado"] == "graduado").sum())

    #Pregunta 5: deserción por cuartil de asistencia 
    p5 = (df.groupby("cuartil_asistencia", observed=True)
            .agg(tasa=("desertor", "mean"),
                 asistencia_media=("asistencia_pct", "mean"),
                 estudiantes=("desertor", "size")))
    print("\nPregunta 5: tasa de deserción por cuartil de asistencia")
    print(p5.round(3))


def guardar(df):
    """Paso 11 del Word: guardar el dataset limpio y la tabla de decisiones. Ya está escrito."""
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED / "dataset_limpio.csv", index=False)
    pd.DataFrame(DECISIONES).to_csv(PROCESSED / "decisiones.csv", index=False)
    print(f"\nDataset limpio guardado: {df.shape[0]} filas, {df.shape[1]} columnas.")


def main():
    original = pd.read_csv(RAW)
    df = original.copy()

    explorar(df)
    auditar(df)
    grafico_faltantes(df)

    df = convertir_numericos(df)
    df = unificar_categorias(df)
    df = convertir_fechas(df)
    df = eliminar_duplicados(df)
    df = tratar_faltantes(df)
    df = tratar_imposibles(df)
    df = crear_variables(df)

    grafico_distribuciones(original, df)
    grafico_tasa_programa(df)
    grafico_tasa_asistencia(df)

    responder_preguntas(df)
    print("\nTabla de decisiones:")
    print(pd.DataFrame(DECISIONES))
    guardar(df)


if __name__ == "__main__":
    main()
