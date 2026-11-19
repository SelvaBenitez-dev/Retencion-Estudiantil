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
    # TODO 5: convertir fecha_matricula a fecha con los dos formatos.
    return df


def eliminar_duplicados(df):
    """Paso 6 del Word: filas repetidas.

    Pregunta: ¿podrían existir dos estudiantes distintos con todos los datos iguales?
    Pista: duplicated() y drop_duplicates(), con reset_index(drop=True).
    """
    # TODO 6: eliminar duplicados, registrar la decisión y devolver el dataframe.
    return df


def tratar_faltantes(df):
    """Paso 7 del Word: decidir qué hacer con los nulos reales.

    Preguntas:
    - ¿Puedes inventar una nota? ¿Qué pasa si imputas el promedio?
    - Para ciudad o tipo de colegio, ¿conviene eliminar la fila o marcar el dato como 'Sin dato'?
    - motivo_retiro tiene muchos nulos. ¿Son errores? (Pista: ¿para quiénes aplica esa columna?)
    """
    # TODO 7: tratar los nulos de promedio_acumulado, ciudad_procedencia y tipo_colegio.
    return df


def tratar_imposibles(df):
    """Paso 8 del Word: valores que no pueden existir.

    Preguntas:
    - La escala del promedio es de 0 a 5. ¿Qué harías con un 45?
    - Una edad de 150 años es un error. ¿Qué valor pondrías en su lugar?
    - Si el estudiante no trabaja, ¿cuántas horas de trabajo tiene? ¿Cómo lo aplicas en código?
    """
    # TODO 8: tratar edad, promedio_acumulado y horas_trabajo_semana, con sus justificaciones.
    return df


def crear_variables(df):
    """Paso 9 del Word: variables nuevas para el análisis.

    Crea:
    - desertor: True si estado es 'desertor', False si no.
    - cuartil_asistencia: divide asistencia_pct en cuatro grupos iguales con pd.qcut.
    Pregunta: ¿por qué conviene usar cuartiles y no valores exactos de asistencia?
    """
    # TODO 9: crear las columnas desertor y cuartil_asistencia.
    return df


def grafico_faltantes(df):
    """Gráfico 1: mapa de faltantes del dataset original.

    Pista: sns.heatmap(df.isnull(), cbar=False)
    """
    # TODO 10: dibujar, guardar en GRAFICOS / "mapa_faltantes.png" y mostrar.
    pass


def grafico_distribuciones(antes, despues):
    """Gráfico 2: boxplots de promedio_acumulado y edad, antes y después de limpiar.

    Pregunta: ¿qué cambió en cada distribución? ¿Por qué?
    """
    # TODO 11: dibujar los cuatro boxplots, guardar en GRAFICOS / "distribuciones_antes_despues.png" y mostrar.
    pass


def grafico_tasa_programa(df):
    """Gráfico 3: tasa de deserción por programa.

    Pista: df.groupby("programa")["desertor"].mean()
    """
    # TODO 12: dibujar la tasa por programa, guardar en GRAFICOS / "tasa_desercion_por_programa.png" y mostrar.
    pass


def grafico_tasa_asistencia(df):
    """Gráfico 4: tasa de deserción por cuartil de asistencia.

    Pista: df.groupby("cuartil_asistencia", observed=True)["desertor"].mean()
    """
    # TODO 13: dibujar la tasa por cuartil, guardar en GRAFICOS / "tasa_desercion_por_asistencia.png" y mostrar.
    pass


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
    pass


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
