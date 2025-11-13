# Proyecto 3 – Simulador de Máquina de Turing para Cifrado César

Curso: **Teoría de la Computación 2025**  
Estudiante:   

Este proyecto implementa un **simulador de Máquinas de Turing de múltiples cintas en Python** y define **dos máquinas específicas** para:

1. **Encriptar** mensajes usando el **Cifrado César con desplazamiento k = 3**.  
2. **Decriptar** mensajes cifrados con el mismo mecanismo (desplazamiento −3).

La especificación del proyecto indica que el cifrado debe realizarse **solo con las operaciones permitidas por una Máquina de Turing**: cambiar de estado, sustituir símbolos de cinta y mover la cabeza a la izquierda o a la derecha, sin usar funciones externas de “suma” o “módulo” dentro de la lógica de la MT. :contentReference[oaicite:0]{index=0}  

---

## 1. Modelo de Máquina de Turing Usado

### 1.1. Tipo de máquina

Se utiliza una **Máquina de Turing determinista de 2 cintas** (multicinta):

- **Cinta 1**: contiene la **entrada** y también la **salida** (mensaje final encriptado/decriptado).
- **Cinta 2**: se deja disponible para extensiones (por ejemplo, podría contener el alfabeto como “diccionario”).  
  En la versión actual se usa como cinta auxiliar, pero la lógica principal se implementa como **sustitución símbolo a símbolo** a través de la función de transición.

Formalmente, una MT de 2 cintas se define como:

\[
M = (Q, \Sigma, \Gamma, \_, q_0, F, \delta)
\]

donde:

- \( Q \): conjunto finito de estados.
- \( \Sigma \): alfabeto de entrada (símbolos válidos en el input).
- \( \Gamma \): alfabeto de cinta, con \( \Sigma \subseteq \Gamma \) y el símbolo en blanco `"_“`.
- `"_“`: símbolo en blanco de la cinta.
- \( q_0 \in Q \): estado inicial.
- \( F \subseteq Q \): conjunto de estados de aceptación.
- \( \delta \): función de transición de la forma:

\[
\delta: Q \times \Gamma^2 \to Q \times \Gamma^2 \times \{L, R, S\}^2
\]

En otras palabras, la transición depende del **estado actual** y de los símbolos leídos en **las dos cintas**, y a cambio entrega:

- un nuevo estado,
- los símbolos a escribir en cada cinta,
- y el movimiento (L, R o S) de cada cabeza.

---

### 1.2. Alfabeto y formato de entrada

Para ambas máquinas (encriptación y decriptación):

- Alfabeto de entrada \(\Sigma\) incluye:
  - Letras mayúsculas `A`–`Z`
  - Espacio `" "`
  - Punto `"."`
  - Símbolo `"#"` como separador entre llave y mensaje
  - Dígitos `0`–`9` (para representar la llave numérica, por ejemplo `3`)

La **entrada** tiene el formato:

```text
k#MENSAJE EN MAYÚSCULAS.

python -m venv venv
.\venv\Scripts\Activate
python main_decoder.py
python main_encoder.py