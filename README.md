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