# Taller práctico proyecto integrador: calidad de datos para la retención estudiantil

Una institución de educación superior quiere entender qué factores están asociados a la deserción, para diseñar estrategias de retención tempranas. Antes de responder preguntas de análisis, el equipo de datos debe garantizar que la información sea confiable. Este taller trabaja justo ese paso: auditar, limpiar y documentar los datos, y después responder cinco preguntas con esos datos limpios.

Los datos son sintéticos. Fueron generados para el taller y no corresponden a estudiantes reales.

## Requisitos

- Python 3.10 o superior
- Git
- Lo visto en los talleres de Pandas y de limpieza de datos

## Cómo empezar

1. Clona el repositorio y entra a la carpeta del proyecto:

   ```
   git clone <URL-DEL-REPOSITORIO>
   cd <NOMBRE-DE-LA-CARPETA>
   ```

2. Crea y activa un ambiente virtual. Las instrucciones para Windows y Mac/Linux están en `LEEME_ambiente.txt`.

3. Instala las librerías:

   ```
   pip install -r requirements.txt
   ```

4. Ejecuta el script:

   ```
   python analisis_desercion.py
   ```

Ejecuta el comando desde la carpeta del proyecto.

## Estructura del proyecto

```
proyecto/
├── analisis_desercion.py   Script principal. Tiene un TODO por cada paso.
├── requirements.txt        Versiones de las librerías.
├── LEEME_ambiente.txt      Pasos para crear el ambiente virtual.
├── README.md               Este archivo.
├── .gitignore              Archivos que Git no debe subir.
└── Data/
    ├── raw/
    │   └── datos_estudiantes.csv   Dataset original. No lo modifiques.
    └── processed/
        ├── .gitkeep                Mantiene la carpeta en el repositorio.
        ├── dataset_limpio.csv      Lo genera el script. No se sube (está en .gitignore).
        ├── decisiones.csv          Lo genera el script. Sí se sube.
        └── graficos/               Lo genera el script. Sí se sube.
```

Lo que genera el script (`dataset_limpio.csv`, `decisiones.csv` y `graficos/`) aparece en `Data/processed/` al ejecutarlo. Los dos últimos se suben al repositorio, porque son parte de la entrega.

## Qué debes hacer

Completa los TODO de `analisis_desercion.py` en orden. Cada función tiene un docstring con preguntas: respóndelas antes de escribir el código. Cada decisión que tomes debe quedar registrada con `registrar()`.

Cuando termines, el script debe producir:

- `Data/processed/dataset_limpio.csv`: el dataset limpio.
- `Data/processed/decisiones.csv`: la tabla de decisiones.
- `Data/processed/graficos/`: los cuatro gráficos.

La guía del taller (`Taller_Retencion_Estudiantil.docx`) explica cada método antes de usarlo, con ejemplos y errores frecuentes.

## Entrega

Sube tu código completo al repositorio y envía el enlace por el formulario de entrega. La entrega es individual.

El repositorio debe incluir:

- `analisis_desercion.py` con todos los TODO completados.
- `Data/processed/decisiones.csv` y la carpeta `Data/processed/graficos/`.
- Un `README.md` al final de este archivo, con una sección titulada **Mis decisiones y respuestas**. Debe incluir:
  0. El diccionario de datos: la tabla de las 23 columnas con tipo, descripción y rol, completada según el paso 1 de la guía.
  1. Tu diagnóstico de calidad: qué problemas encontraste y en qué columnas.
  2. Tus decisiones de limpieza, con su justificación.
  3. Las respuestas a las cinco preguntas, cada una con el número de estudiantes por grupo.
  4. Tu respuesta a la reflexión sobre asociación y causalidad.
  5. Tu respuesta a la reflexión sobre `motivo_retiro` y la predicción.
  6. Tu respuesta a la reflexión sobre el uso de variables sensibles.

El script debe ejecutarse sin errores desde cero. Cada decisión necesita una justificación, y cada conclusión debe apoyarse en un número del análisis.


**Mis decisiones y respuestas**

0. 

| Columna | Tipo | Descripción | Rol |
|---|---|---|---|
| id_estudiante | Texto | Código que identifica a cada estudiante. | Identificación |
| programa | Categórica | Carrera la cual cursa el estudiante. | Explicativa |
| facultad | Categórica | Facultad a la que pertenece el programa que cursa el estudiante. | Explicativa |
| jornada | Categórica | Horario de estudio; si es jornada diurna, nocturna o fin de semana. | Explicativa |
| semestre | Numérica | Semestre en el que se encuentra cursando el estudiante. | Explicativa |
| promedio_acumulado | Numérica | Nota del promedio de la carrera (0 <= x <= 5)| Explicativa |
| creditos_aprobados | Numérica | Créditos aprobados hasta la fecha. | Explicativa |
| materias_reprobadas | Numérica | Número de materias perdidas. | Explicativa |
| asistencia_pct | Numérica (entra en str)| Porcentaje de asistencia a clases. Trae % y guiones. | Explicativa |
| sesiones_tutoria | Numérica | Sesiones de tutoría a las que asistió el estudiante. | Explicativa |
| cambios_programa | Numérica | Veces que el estudiante se ha cambiado de carrera. | Explicativa |
| estrato | Categórica | Estrato socioeconómico de la vivienda (1 a 6). | Explicativa |
| beca | Categórica | Indica si el estudiante recibe una beca (sí o no). | Explicativa |
| trabaja | Categórica | Indica si el estudiante trabaja (sí o no). | Explicativa |
| horas_trabajo_semana | Numérica (llega como str) | Horas de trabajo por semana. Trae guiones. | Explicativa |
| distancia_km | Numérica | Distancia de la vivienda al lugar de estudio en km. | Explicativa |
| edad | Numérica | Edad del estudiante (años). | Explicativa |
| genero | Categórica | Género registrado: femenino o masculino. | Explicativa |
| ciudad_procedencia | Categórica | Ciudad de origen del estudiante. | Explicativa |
| tipo_colegio | Categórica | Tipo de colegio donde egresó el estudiante: público o privado. | Explicativa |
| fecha_matricula | Fecha (llega como str) | Fecha de matrícula. Mezcla los formatos AAAA-MM-DD y DD/MM/AAAA. | Explicativa |
| estado | Categórica | Situación del estudiante: activo, graduado o desertor. | Resultado |
| motivo_retiro | Categórica | Razón del retiro; solo existe para los desertores. | Resultado |

Análisis:
a. Las columnas identificadas que deberían ser numéricas en lugar de str son: `asistencia_pct`, `horas_trabajo_semana` y `fecha_matricula`.
b. El promedio excede el límite de 0 <= x <= 5, siendo el promedio máximo `78.00`
c. Edad: Se registró una edad máxima de `150.00` (dato que no debe pertenecer en un registro estudiantil en este caso.)
d. Variantes en la escritura: Leyendo directamente datos_estudiantes.csv, hay instancias donde las palabras tienen o no tílde, en el caso de "psicología" también hay "psicologia". Por otro lado, en género, hay casos "Femenino" y "femenino".

1. 

Conteos hechos sobre el dataset original, antes de corregir nada (10.150 filas).

| Tipo de problema | Columna | Filas |
|---|---|---|
| Nulo real | promedio_acumulado | 304 |
| Nulo real | distancia_km | 199 |
| Nulo real | ciudad_procedencia | 103 |
| Nulo real | tipo_colegio | 152 |
| Nulo esperado (no es error) | motivo_retiro | 6.877 |
| Faltante disfrazado (`-`) | asistencia_pct | 202 |
| Faltante disfrazado (`-`) | horas_trabajo_semana | 2.822 |
| Faltante disfrazado (999) | distancia_km | 152 |
| Formato inconsistente (símbolo %) | asistencia_pct | 300 |
| Formato inconsistente (fechas DD/MM/AAAA) | fecha_matricula | 3.052 |
| Duplicado | todas las columnas | 150 |
| Valor imposible (fuera de 15 a 60) | edad | 12 |
| Valor imposible (mayor a 5) | promedio_acumulado | 17 |
| Valor imposible (más de 100 horas) | horas_trabajo_semana | 30 |

**Errores tipográficos:**
- `programa`: Ingenieria de Sistemas, Psicologia (sin tilde).
- `jornada`: diurna, nocturna, NOCTURNA (minúsculas, mayúsculas y espacio al final).
- `genero`: M, F, femenino.
- `ciudad_procedencia`: BOGOTÁ, Bogota, bogota, medellin, Medellin.

**Lectura del diagnóstico:**
- El problema que más afecta el análisis es que `asistencia_pct` y `horas_trabajo_semana` estén guardadas como texto, mientras sigan así no se puede calcular ninguna tasa ni promedio con ellas.
- Los 17 promedios entre 45 y 78 están en otra escala e inflarían la media de su grupo.
- Los 6.877 nulos de `motivo_retiro` no son errores: la columna solo aplica a los desertores, y ningún desertor la tiene vacía.
- Los 2.822 guiones de `horas_trabajo_semana` son todos de estudiantes que no trabajan, así que en realidad significan 0 horas.
- Las 150 filas duplicadas también repiten el `id_estudiante`, así que son el mismo registro cargado dos veces.

2. 

Todas las decisiones están registradas en `Data/processed/decisiones.csv`, con el número de filas afectadas y su justificación.

| Columna | Acción | Filas | Justificación |
|---|---|---|---|
| asistencia_pct | Quitar el símbolo % | 300 | El % es formato, no dato; impide tratar la columna como número. |
| asistencia_pct | `-` a nulo y convertir a número | 202 | El guion es un faltante disfrazado; debe ser un nulo real. |
| horas_trabajo_semana | `-` a nulo y convertir a número | 2.822 | Todos los guiones son de estudiantes que no trabajan; en el paso 8 se les pone 0. |
| distancia_km | 999 a nulo | 152 | 999 es un código de relleno; si se deja, infla la distancia promedio. |

Después de convertir, las tres columnas quedan como `float64`.

3. 

Se normalizó cada columna con `str.strip()` y `str.lower()`, y después se tradujo cada variante a su forma correcta con un diccionario basado en `VALIDOS`.

| Columna | Variantes corregidas | Filas |
|---|---|---|
| programa | Ingenieria de Sistemas, Psicologia | 260 |
| jornada | diurna, nocturna, NOCTURNA (con espacio) | 485 |
| genero | M, F, femenino | 559 |
| ciudad_procedencia | BOGOTÁ, Bogota, bogota, medellin, Medellin | 542 |

Justificación: las variantes de escritura crean grupos falsos que dividen el mismo valor; por ejemplo, Psicología aparecía partida en 1.065 + 116 estudiantes. Después de unificar, todos los valores coinciden con la lista de válidos. No se unificó "Otra ciudad" con ninguna ciudad, y los 103 nulos de ciudad se tratan en el paso 7. 

4. 

**Paso 5: fechas**

| Columna | Acción | Filas | Justificación |
|---|---|---|---|
| fecha_matricula | Convertir los dos formatos a fecha | 3.052 en DD/MM/AAAA | Con formatos mezclados la columna no se puede usar como fecha. Se convirtió cada formato por separado con `pd.to_datetime(format=..., errors="coerce")` y se juntaron con `fillna()`. El formato explícito evita confundir día y mes. |

Después de la conversión, la columna queda como `datetime64` y ninguna fecha quedó sin convertir.

5. 
**Paso 6: duplicados**

| Columna | Acción | Filas | Justificación |
|---|---|---|---|
| todas | Eliminar filas idénticas con `drop_duplicates()` y renumerar con `reset_index(drop=True)` | 150 | Las 150 filas duplicadas repiten también el `id_estudiante`, así que son el mismo registro cargado dos veces y no dos estudiantes distintos. Si se dejaran, esos estudiantes contarían doble en las tasas. |

El dataset pasa de 10.150 a 10.000 filas, y ya no queda ningún `id_estudiante` repetido.

6. 
**Paso 7: faltantes**

| Columna | Acción | Filas | Justificación |
|---|---|---|---|
| promedio_acumulado | Eliminar filas | 298 | Una nota no se puede inventar. Imputar la media acercaría todos los grupos al promedio general y escondería las diferencias. Se pierde el 3 % de las filas. |
| ciudad_procedencia | Rellenar con "Sin dato" | 96 | Es un dato descriptivo. Eliminar la fila haría perder al estudiante en las demás preguntas. |
| tipo_colegio | Rellenar con "Sin dato" | 145 | Igual que la ciudad. |
| motivo_retiro | Dejar los nulos | 6.562 | Nulo esperado: solo aplica a desertores, y ningún desertor lo tiene vacío. |
| asistencia_pct | Dejar los nulos | 197 | Es la variable de la pregunta 5; imputarla inventaría la relación que se quiere medir. Quedan fuera de los cuartiles. |
| distancia_km | Dejar los nulos | 334 | No se usa en las cinco preguntas. |

Los nulos de `horas_trabajo_semana` se tratan en el paso 8. Después de este paso quedan 9.702 filas.

7. **Paso 8: valores imposibles**

Primero se marcó cada valor imposible como nulo con `loc`, y después se trató como cualquier otro nulo.

| Columna | Acción | Filas | Justificación |
|---|---|---|---|
| edad | Fuera de 15 a 60 → mediana de las edades válidas (22) | 12 | Edades de 12 y 150 años son errores de registro. La mediana no se ve afectada por los extremos y así no se pierde la fila. |
| promedio_acumulado | Mayores a 5 → nulo → eliminar fila | 15 | Valores de 45, 62 y 78 son imposibles en la escala 0 a 5. No se puede confirmar la escala original, así que se tratan como un faltante: una nota no se inventa. |
| horas_trabajo_semana | Nulos con `trabaja = "no"` → 0 | 2.703 | Todos los guiones originales eran de estudiantes que no trabajan, así que significaban 0 horas. |
| horas_trabajo_semana | Mayores a 100 → mediana de quienes trabajan (24) | 29 | Más de 100 horas por semana no deja tiempo para estudiar ni dormir. Se usa la mediana de quienes trabajan para no contar los ceros. |

Después de este paso quedan 9.687 filas. La edad queda entre 17 y 29 años, el promedio entre 1,17 y 5,00, y las horas entre 0 y 40, sin nulos.


8. **Paso 9: variables nuevas**

| Columna nueva | Cómo se creó | Filas | Justificación |
|---|---|---|---|
| desertor | `df["estado"].eq("desertor")` | 3.136 desertores de 9.687 (32,4 %) | Una columna True/False permite calcular la tasa de deserción con `mean()`, porque el promedio de True y False es la proporción de True. |
| cuartil_asistencia | `pd.qcut(asistencia_pct, 4)` con etiquetas Q1 a Q4 | 9.490 (197 sin asistencia quedan fuera) | Con valores exactos habría cientos de grupos pequeños con tasas inestables. Los cuartiles crean 4 grupos de tamaño parecido (unos 2.350 a 2.390 estudiantes cada uno), así que la comparación es confiable. |

El dataset limpio queda con 9.687 filas y 25 columnas.

9.

