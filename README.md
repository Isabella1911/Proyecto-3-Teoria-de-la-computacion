# Proyecto 3 – Simulador de Máquina de Turing para Cifrado César

**Curso:** Teoría de la Computación 2025

Este proyecto implementa un **simulador de Máquinas de Turing deterministas** y define **dos máquinas específicas** para:

1. **Encriptar** mensajes usando el **Cifrado César con desplazamiento general k (0 ≤ k ≤ 26)**.
2. **Decriptar** mensajes cifrados con la misma llave.

La especificación del proyecto indica que el cifrado debe realizarse **solo con las operaciones permitidas por una Máquina de Turing**: cambiar de estado, sustituir símbolos de cinta y mover la cabeza a la izquierda o a la derecha, sin usar funciones externas de “suma” o “módulo” dentro de la lógica de la MT.

---

## Tabla de Contenidos

1. [Inicio Rápido](#-inicio-rápido)
2. [Modelo de Máquina de Turing](#-modelo-de-máquina-de-turing)
3. [Interfaz Gráfica (GUI)](#-interfaz-gráfica-gui)
4. [Uso por Línea de Comandos](#-uso-por-línea-de-comandos)
5. [Ejemplos](#-ejemplos)
6. [Estructura del Proyecto](#-estructura-del-proyecto)

---

## Inicio Rápido

### Opción 1: Interfaz Gráfica

```bash
python run_gui.py
```

### Opción 2: Línea de Comandos

```bash
# Encriptar
python main_encoder.py "3#HOLA MUNDO."

# Decriptar
python main_decoder.py "3#MTQF RZSIT."
```

---

## Modelo de Máquina de Turing

### Tipo de Máquina

**Máquinas de Turing deterministas de 1 sola cinta (encoder y decoder):**

- La única cinta contiene la llave, el separador `#` y el mensaje. Tras el procesamiento la misma cinta queda transformada.

### Definición Formal

\[
M = (Q, \Sigma, \Gamma, \_, q_0, F, \delta)
\]

Donde:
- **Q**: Conjunto de estados
- **Σ**: Alfabeto de entrada (A-Z, espacio, punto, #, 0-9)
- **Γ**: Alfabeto de cinta
- **\_**: Símbolo en blanco
- **q₀**: Estado inicial
- **F**: Estados de aceptación
- **δ**: Función de transición: Q × Γ → Q × Γ × {L, R, S}

### Alfabeto y Formato

**Alfabeto de entrada:**
- Letras mayúsculas: A-Z (26 símbolos totales)
- Símbolos: espacio, punto (.)
- Separador: `#`
- Dígitos: 0–9 (para definir la llave numérica) y letras para definir llave alfabética.

**Formato de entrada:**
```
LLAVE#MENSAJE
```

**Ejemplos:**
```
3#ROMA NO FUE CONSTRUIDA EN UN DIA.
13#TURING MACHINE.
26#HOLA MUNDO.
D#ROMA NO FUE CONSTRUIDA EN UN DIA.   (D equivale a k=3)
```


### Cifrado César

**Fórmula de encriptación (alfabeto de tamaño n = 26):**
\[
E(x) = (x + k) \mod n
\]

**Fórmula de decriptación:**
\[
D(x) = (x - k) \mod n
\]

Donde:
- **x**: Posición de la letra en el alfabeto
- **k**: Llave (desplazamiento). Puede darse como número (0–26) o letra (A=0, B=1, ..., Z=25).
- **n**: Tamaño del alfabeto (26 caracteres, A-Z estándar).

> Nota: Con k=3 sobre `ROMA` produce `URPD` (R→U, O→R, M→P, A→D) según el cifrado César clásico.

---

## Interfaz Gráfica (GUI)

### Ejecutar

```bash
python run_gui.py
```

### Características

La GUI incluye **4 pestañas**:

#### 1. Encriptar
- Campo de entrada para mensaje
- Botón "Encriptar"
- Resultado con fondo verde
- Copiar al portapapeles
- Guardado automático en `output/encoder_output.txt`
 - Botón "Ver trazado MT" para inspeccionar la evolución de la cinta paso a paso

#### 2. Decriptar
- Campo de entrada para mensaje cifrado
- Botón "Decriptar"
- Resultado con fondo naranja
- Copiar al portapapeles
- Guardado automático en `output/decoder_output.txt`
 - Botón "Ver trazado MT" para inspeccionar la evolución de la cinta

#### 3. Ejemplos
- 8 ejemplos predefinidos (k=1, 3, 5, 7, 10, 13, 20)
- Botones de carga rápida
- Explicación de cada caso

#### 4. Información
- Explicación del cifrado César
- Fórmulas matemáticas
- Descripción de las MTs
- Objetivos del proyecto

### Uso Rápido

1. Ejecuta `python run_gui.py`
2. Ve a pestaña "Encriptar"
3. Ingresa: `3#HOLA MUNDO.`
4. Presiona "Encriptar"
5. Resultado: `MTQF RZSIT.`

---

## Uso por Línea de Comandos

### Encriptar

```bash
# Usando argumento
python main_encoder.py "3#ROMA NO FUE CONSTRUIDA EN UN DIA."

# Usando archivo de entrada
python main_encoder.py
# Lee de: ejemplos/input_encoder.txt
# Guarda en: output/encoder_output.txt
```

### Decriptar

```bash
# Usando argumento
python main_decoder.py "3#URPD QR IXH FRQVWUXLGD HQ XQ GLD."

# Usando archivo de entrada
python main_decoder.py
# Lee de: ejemplos/input_decoder.txt
# Guarda en: output/decoder_output.txt
```

### Como Módulo Python

```python
from maquina.encoder_mt import encrypt
from maquina.decoder_mt import decrypt

# Encriptar
cifrado = encrypt("3#HOLA MUNDO.")
print(cifrado)  # MTQF RZSIT.

# Decriptar
original = decrypt("3#MTQF RZSIT.")
print(original)  # HOLA MUNDO.
```

---

## Ejemplos

### Ejemplo 1: Clásico (k=3)
```
Entrada (encriptar):  3#ROMA NO FUE CONSTRUIDA EN UN DIA.
Salida:               URPD QR IXH FRQVWUXLGD HQ XQ GLD.

Entrada (decriptar):  3#URPD QR IXH FRQVWUXLGD HQ XQ GLD.
Salida:               ROMA NO FUE CONSTRUIDA EN UN DIA.
```

### Ejemplo 2: Simple (k=5)
```
Entrada:  5#HOLA MUNDO.
Salida:   MTQF RZSIT.
```

### Ejemplo 3: ROT13 (k=13)
```
Entrada:  13#TURING MACHINE.
Salida:   GHEVAT ZNPUVAR.
```

### Ejemplo 4: Mínimo (k=1)
```
Entrada:  1#CAESAR CIPHER.
Salida:   DBFTBS DJQIFS.
```

### Más Ejemplos

Usa la pestaña "Ejemplos" en la GUI para casos predefinidos.

---

## Generación de Máquinas

Las definiciones de transición se generan mediante el script:

```bash
python generate_machines.py
```

Esto regenera:
- `ejemplos/mt_encoder.json`
- `ejemplos/mt_decoder.json`

Cada archivo incluye estados `qKey_k` y `qProc_k` para k = 0..26, soportando llaves numéricas de uno o dos dígitos y llaves dadas como letra. La transformación se hace exclusivamente dentro de la MT (sin cálculos aritméticos externos).

### Visualización de Cinta / Trazado

Al ejecutar una operación de encriptación o decriptación en la GUI se habilita el botón **"Ver trazado MT"** que muestra:

- Número de paso
- Estado actual
- Posición de la cabeza
- Contenido de la cinta con el símbolo bajo la cabeza entre corchetes

Esto permite verificar que la máquina solo usa movimientos, escrituras y cambios de estado para realizar el cifrado César.

---

## Estructura del Proyecto

```
Proyecto-3-Teoria-de-la-computacion/
├── gui.py                 # Interfaz gráfica
├── run_gui.py             # Lanzador de la GUI
├── main_encoder.py        # Encriptar por CLI
├── main_decoder.py        # Decriptar por CLI
├── generate_machines.py   # Generador de MTs (JSON)
├── maquina/
│   ├── turing.py          # Simulador de MT (genérico)
│   ├── parser.py          # Carga JSON → MT
│   ├── encoder_mt.py      # Capa de ejecución (encoder)
│   └── decoder_mt.py      # Capa de ejecución (decoder)
├── ejemplos/
│   ├── mt_encoder.json    # MT de encriptación
│   ├── mt_decoder.json    # MT de decriptación
│   ├── input_encoder.txt  # Ejemplo de entrada
│   └── input_decoder.txt  # Ejemplo de entrada
├── output/
│   ├── encoder_output.txt # Último resultado encoder
│   └── decoder_output.txt # Último resultado decoder
└── README.md
```

---

## Requisitos

- **Python 3.x**
- **Tkinter** (incluido con Python)
- Sin dependencias externas

---

## Solución de Problemas

### Error: "No module named 'tkinter'"
Tkinter viene con Python. Reinstala Python asegurándote de incluir Tkinter.

### Error: "No module named 'maquina'"
Ejecuta desde la carpeta del proyecto:
```bash
cd ruta/al/Proyecto-3-Teoria-de-la-computacion
python run_gui.py
```

### La ventana no se abre
1. Verifica Python: `python --version`
2. Verifica Tkinter: `python -c "import tkinter; print('OK')"`
3. Ejecuta: `python run_gui.py`

---

## Información Técnica

### Complejidad
- **Temporal:** O(n) donde n = longitud del mensaje
- **Espacial:** O(n) para las cintas

### Configuración de MTs
Las tablas de transiciones (una cinta) están en:
- `ejemplos/mt_encoder.json` – MT de encriptación (desplaza +k)
- `ejemplos/mt_decoder.json` – MT de decriptación (desplaza −k)
- `generate_machines.py` – Generador de ambos JSON.

---
