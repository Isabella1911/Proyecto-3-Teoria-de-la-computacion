# gui.py
"""
GUI para el Proyecto 3 - Teoría de la Computación
Simulador de Máquinas de Turing para Cifrado César
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pathlib import Path
from maquina.encoder_mt import encrypt
from maquina.decoder_mt import decrypt


class CaesarCipherGUI:
    """Interfaz gráfica para el cifrado César con Máquinas de Turing"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cifrado César - Máquinas de Turing")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear interfaz
        self.create_widgets()
        
        # Cargar ejemplos por defecto
        self.load_default_examples()
    
    def setup_styles(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores personalizados
        bg_color = "#f0f0f0"
        fg_color = "#333333"
        accent_color = "#2196F3"
        
        self.root.configure(bg=bg_color)
        
        # Estilo para pestañas
        style.configure('TNotebook', background=bg_color)
        style.configure('TNotebook.Tab', padding=[20, 10], font=('Arial', 10, 'bold'))
        
        # Estilo para frames
        style.configure('TFrame', background=bg_color)
        style.configure('Card.TFrame', background='white', relief='raised')
        
        # Estilo para labels
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), 
                       background=bg_color, foreground=accent_color)
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), 
                       background='white', foreground=fg_color)
        style.configure('TLabel', background='white', foreground=fg_color)
        
        # Estilo para botones
        style.configure('TButton', font=('Arial', 10, 'bold'), 
                       padding=[10, 5])
        style.map('TButton', background=[('active', accent_color)])
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Título principal
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=20)
        
        title_label = ttk.Label(
            title_frame,
            text="Cifrado César con Máquinas de Turing",
            style='Title.TLabel'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Proyecto 3 - Teoría de la Computación",
            font=('Arial', 10, 'italic')
        )
        subtitle_label.pack()
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Crear pestañas
        self.create_encoder_tab()
        self.create_decoder_tab()
        self.create_examples_tab()
        self.create_info_tab()
        
        # Footer
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(pady=10)
        
        footer_label = ttk.Label(
            footer_frame,
            text="Universidad • 2025",
            font=('Arial', 8)
        )
        footer_label.pack()
    
    def create_encoder_tab(self):
        """Crea la pestaña de encriptación"""
        encoder_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(encoder_frame, text="Encriptar")
        
        # Card container
        card = ttk.Frame(encoder_frame, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(
            card,
            text="Encriptar Mensaje",
            style='Header.TLabel'
        ).pack(anchor='w', pady=(0, 15))
        
        # Instrucciones
        instructions = ttk.Label(
            card,
            text="Formato: LLAVE#MENSAJE\nEjemplo: 3#ROMA NO FUE CONSTRUIDA EN UN DIA.",
            font=('Arial', 9),
            foreground='#666'
        )
        instructions.pack(anchor='w', pady=(0, 10))
        
        # Input
        ttk.Label(card, text="Texto a encriptar:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.encoder_input = scrolledtext.ScrolledText(
            card,
            height=4,
            font=('Consolas', 11),
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1
        )
        self.encoder_input.pack(fill='x', pady=(5, 15))
        
        # Botón de encriptar
        btn_frame = ttk.Frame(card)
        btn_frame.pack(pady=10)
        
        encrypt_btn = ttk.Button(
            btn_frame,
            text="Encriptar",
            command=self.encrypt_message,
            style='TButton'
        )
        encrypt_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(
            btn_frame,
            text="Limpiar",
            command=lambda: self.clear_fields('encoder')
        )
        clear_btn.pack(side='left', padx=5)
        
        # Output
        ttk.Label(card, text="Mensaje encriptado:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.encoder_output = scrolledtext.ScrolledText(
            card,
            height=4,
            font=('Consolas', 11, 'bold'),
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1,
            background='#e8f5e9'
        )
        self.encoder_output.pack(fill='x', pady=(5, 10))
        self.encoder_output.config(state='disabled')
        
        # Botón copiar
        copy_btn = ttk.Button(
            card,
            text="Copiar resultado",
            command=lambda: self.copy_to_clipboard(self.encoder_output)
        )
        copy_btn.pack(pady=5)

        # Botón ver trazado
        self.encoder_trace = []
        self.trace_btn_enc = ttk.Button(
            card,
            text="Ver trazado MT",
            command=lambda: self.show_trace(self.encoder_trace, title="Trazado Encriptación")
        )
        self.trace_btn_enc.pack(pady=5)
        self.trace_btn_enc.config(state='disabled')
    
    def create_decoder_tab(self):
        """Crea la pestaña de decriptación"""
        decoder_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(decoder_frame, text="Decriptar")
        
        # Card container
        card = ttk.Frame(decoder_frame, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(
            card,
            text="Decriptar Mensaje",
            style='Header.TLabel'
        ).pack(anchor='w', pady=(0, 15))
        
        # Instrucciones
        instructions = ttk.Label(
            card,
            text="Formato: LLAVE#MENSAJE_ENCRIPTADO\nEjemplo: 3#URPD QR IXH FRQVWUXLGD HQ XQ GLD.",
            font=('Arial', 9),
            foreground='#666'
        )
        instructions.pack(anchor='w', pady=(0, 10))
        
        # Input
        ttk.Label(card, text="Texto a decriptar:", font=('Arial', 10, 'bold')).pack(anchor='w')
        self.decoder_input = scrolledtext.ScrolledText(
            card,
            height=4,
            font=('Consolas', 11),
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1
        )
        self.decoder_input.pack(fill='x', pady=(5, 15))
        
        # Botones
        btn_frame = ttk.Frame(card)
        btn_frame.pack(pady=10)
        
        decrypt_btn = ttk.Button(
            btn_frame,
            text="Decriptar",
            command=self.decrypt_message,
            style='TButton'
        )
        decrypt_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(
            btn_frame,
            text="Limpiar",
            command=lambda: self.clear_fields('decoder')
        )
        clear_btn.pack(side='left', padx=5)
        
        # Output
        ttk.Label(card, text="Mensaje decriptado:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(10, 0))
        self.decoder_output = scrolledtext.ScrolledText(
            card,
            height=4,
            font=('Consolas', 11, 'bold'),
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1,
            background='#fff3e0'
        )
        self.decoder_output.pack(fill='x', pady=(5, 10))
        self.decoder_output.config(state='disabled')
        
        # Botón copiar
        copy_btn = ttk.Button(
            card,
            text="Copiar resultado",
            command=lambda: self.copy_to_clipboard(self.decoder_output)
        )
        copy_btn.pack(pady=5)

        # Botón ver trazado
        self.decoder_trace = []
        self.trace_btn_dec = ttk.Button(
            card,
            text="Ver trazado MT",
            command=lambda: self.show_trace(self.decoder_trace, title="Trazado Decriptación")
        )
        self.trace_btn_dec.pack(pady=5)
        self.trace_btn_dec.config(state='disabled')
    
    def create_examples_tab(self):
        """Crea la pestaña de ejemplos"""
        examples_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(examples_frame, text="Ejemplos")
        
        # Card container
        card = ttk.Frame(examples_frame, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(
            card,
            text="Ejemplos de Cifrado César",
            style='Header.TLabel'
        ).pack(anchor='w', pady=(0, 15))
        
        # Ejemplos
        examples_text = scrolledtext.ScrolledText(
            card,
            height=20,
            font=('Consolas', 10),
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1
        )
        examples_text.pack(fill='both', expand=True)
        
        examples_content = """
============================================================
EJEMPLOS DE CIFRADO CÉSAR
============================================================

EJEMPLO 1: Llave k=3
------------------------------------------------------------
    Entrada (encriptar):  3#ROMA NO FUE CONSTRUIDA EN UN DIA.
    Salida (encriptado):  URPD QR IXH FRQVWUXLGD HQ XQ GLD.
    Entrada (decriptar):  3#URPD QR IXH FRQVWUXLGD HQ XQ GLD.
    Salida (decriptado):  ROMA NO FUE CONSTRUIDA EN UN DIA.

EJEMPLO 2: Llave k=5
------------------------------------------------------------
    Entrada (encriptar):  5#HOLA MUNDO.
    Salida (encriptado):  MTQF RZSIТ.
    Entrada (decriptar):  5#MTQF RZSIТ.
    Salida (decriptado):  HOLA MUNDO.

EJEMPLO 3: Llave k=1
------------------------------------------------------------
    Entrada (encriptar):  1#CAESAR CIPHER.
    Salida (encriptado):  DBFTBS DJQIFS.
    Entrada (decriptar):  1#DBFTBS DJQIFS.
    Salida (decriptado):  CAESAR CIPHER.

EJEMPLO 4: Llave k=13 (ROT13)
------------------------------------------------------------
    Entrada (encriptar):  13#TURING MACHINE.
    Salida (encriptado):  GHEVAT ZNPUVAR.
    Entrada (decriptar):  13#GHEVAT ZNPUVAR.
    Salida (decriptado):  TURING MACHINE.

EJEMPLO 5: Llave k=7
------------------------------------------------------------
    Entrada (encriptar):  7#LA TEORIA DE LA COMPUTACION.
    Salida (encriptado):  SH ALVYPH KL SH JVTWBAHJPVU.
    Entrada (decriptar):  7#SH ALVYPH KL SH JVTWBAHJPVU.
    Salida (decriptado):  LA TEORIA DE LA COMPUTACION.

NOTAS:
    • La llave puede ser un número (0-26) o una letra (A-Z)
    • El alfabeto incluye: A-Z, espacio y punto (26 letras)
    • Solo se cifran las letras mayúsculas
    • Los espacios y puntos se mantienen
============================================================
"""
        
        examples_text.insert('1.0', examples_content)
        examples_text.config(state='disabled')
        
        # Botones de ejemplos rápidos
        btn_frame = ttk.Frame(card)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Probar Ejemplo 1",
            command=lambda: self.load_example("3#ROMA NO FUE CONSTRUIDA EN UN DIA.")
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="Probar Ejemplo 2",
            command=lambda: self.load_example("5#HOLA MUNDO.")
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="Probar Ejemplo 4",
            command=lambda: self.load_example("13#TURING MACHINE.")
        ).pack(side='left', padx=5)
    
    def create_info_tab(self):
        """Crea la pestaña de información"""
        info_frame = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(info_frame, text="Información")
        
        # Card container
        card = ttk.Frame(info_frame, style='Card.TFrame', padding=20)
        card.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(
            card,
            text="Acerca del Proyecto",
            style='Header.TLabel'
        ).pack(anchor='w', pady=(0, 15))
        
        # Información
        info_text = scrolledtext.ScrolledText(
            card,
            height=20,
            font=('Arial', 10),
            wrap=tk.WORD,
            relief='solid',
            borderwidth=1
        )
        info_text.pack(fill='both', expand=True)
        
        info_content = """
============================================================
INFORMACIÓN DEL PROYECTO
============================================================

CIFRADO CÉSAR
El cifrado César es una técnica de sustitución donde cada letra se reemplaza
por otra desplazada k posiciones en el alfabeto.

FÓRMULA
    Encriptación: E(x) = (x + k) mod n
    Decriptación: D(x) = (x - k) mod n
    x: posición de la letra, k: llave, n: tamaño del alfabeto.

MÁQUINAS DE TURING
Se implementan dos máquinas: una para encriptar y otra para decriptar.
Operaciones permitidas: cambiar de estado, escribir símbolo y mover la cabeza.

CARACTERÍSTICAS
    • Una cinta
    • Configuración en JSON
    • Alfabeto: A-Z (26 letras), espacio y punto
    • Sin operaciones externas dentro de la MT

FORMATO DE ENTRADA
    LLAVE#MENSAJE (ejemplo: 3#HOLA MUNDO.)
    El símbolo '#' separa la llave del mensaje.

OBJETIVOS
    • Investigar MTs
    • Simular cifrado y descifrado
    • Respetar restricciones del modelo
    • Comprender el mecanismo del cifrado

Desarrollado con Python y Tkinter • 2025
============================================================
"""
        
        info_text.insert('1.0', info_content)
        info_text.config(state='disabled')
    
    def encrypt_message(self):
        """Encripta el mensaje usando la MT"""
        input_text = self.encoder_input.get('1.0', 'end-1c').strip()
        
        if not input_text:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un texto a encriptar.")
            return
        
        try:
            # Mostrar mensaje de procesamiento
            self.root.config(cursor="wait")
            self.root.update()
            
            # Encriptar usando la MT
            from maquina.encoder_mt import encrypt_with_trace
            result, trace = encrypt_with_trace(input_text)
            
            # Mostrar resultado
            self.encoder_output.config(state='normal')
            self.encoder_output.delete('1.0', 'end')
            self.encoder_output.insert('1.0', result)
            self.encoder_output.config(state='disabled')
            self.encoder_trace = trace
            self.trace_btn_enc.config(state='normal')
            
            # Guardar en archivo
            self.save_output(result, 'encoder_output.txt')
            
            messagebox.showinfo(
                "Éxito",
                "Mensaje encriptado correctamente.\n"
                f"Resultado guardado en: output/encoder_output.txt"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al encriptar:\n{str(e)}")
        
        finally:
            self.root.config(cursor="")
    
    def decrypt_message(self):
        """Decripta el mensaje usando la MT"""
        input_text = self.decoder_input.get('1.0', 'end-1c').strip()
        
        if not input_text:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un texto a decriptar.")
            return
        
        try:
            # Mostrar mensaje de procesamiento
            self.root.config(cursor="wait")
            self.root.update()
            
            # Decriptar usando la MT
            from maquina.decoder_mt import decrypt_with_trace
            result, trace = decrypt_with_trace(input_text)
            
            # Mostrar resultado
            self.decoder_output.config(state='normal')
            self.decoder_output.delete('1.0', 'end')
            self.decoder_output.insert('1.0', result)
            self.decoder_output.config(state='disabled')
            self.decoder_trace = trace
            self.trace_btn_dec.config(state='normal')
            
            # Guardar en archivo
            self.save_output(result, 'decoder_output.txt')
            
            messagebox.showinfo(
                "Éxito",
                "Mensaje decriptado correctamente.\n"
                f"Resultado guardado en: output/decoder_output.txt"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al decriptar:\n{str(e)}")
        
        finally:
            self.root.config(cursor="")
    
    def save_output(self, text, filename):
        """Guarda el resultado en un archivo"""
        try:
            output_dir = Path(__file__).parent / "output"
            output_dir.mkdir(exist_ok=True)
            output_file = output_dir / filename
            output_file.write_text(text, encoding='utf-8')
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
    
    def clear_fields(self, mode):
        """Limpia los campos de entrada y salida"""
        if mode == 'encoder':
            self.encoder_input.delete('1.0', 'end')
            self.encoder_output.config(state='normal')
            self.encoder_output.delete('1.0', 'end')
            self.encoder_output.config(state='disabled')
            self.encoder_trace = []
            self.trace_btn_enc.config(state='disabled')
        elif mode == 'decoder':
            self.decoder_input.delete('1.0', 'end')
            self.decoder_output.config(state='normal')
            self.decoder_output.delete('1.0', 'end')
            self.decoder_output.config(state='disabled')
            self.decoder_trace = []
            self.trace_btn_dec.config(state='disabled')
    
    def copy_to_clipboard(self, text_widget):
        """Copia el contenido del widget al portapapeles"""
        text = text_widget.get('1.0', 'end-1c').strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copiado", "Texto copiado al portapapeles.")
        else:
            messagebox.showwarning("Advertencia", "No hay texto para copiar.")
    
    def load_example(self, example_text):
        """Carga un ejemplo en el campo de encriptación"""
        self.notebook.select(0)  # Cambiar a pestaña de encriptar
        self.encoder_input.delete('1.0', 'end')
        self.encoder_input.insert('1.0', example_text)
        messagebox.showinfo("Ejemplo cargado", "Ejemplo cargado en la pestaña de Encriptar.")

    def show_trace(self, trace, title="Trazado MT"):
        """Muestra una ventana emergente con el trazado de la MT."""
        if not trace:
            messagebox.showwarning("Sin trazado", "No hay trazado disponible.")
            return
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("700x500")
        text = scrolledtext.ScrolledText(top, wrap=tk.NONE, font=('Consolas', 10))
        text.pack(fill='both', expand=True)
        lines = []
        for entry in trace:
            lines.append(f"Paso {entry['step']:>4} | Estado: {entry['state']:<10} | Cabeza: {entry['head']:>3}\n  Cinta: {entry['tape']}\n")
        text.insert('1.0', "".join(lines))
        text.config(state='disabled')
    
    def load_default_examples(self):
        """Carga los ejemplos por defecto desde los archivos"""
        try:
            base = Path(__file__).parent
            
            # Cargar ejemplo de encoder
            encoder_file = base / "ejemplos" / "input_encoder.txt"
            if encoder_file.exists():
                example = encoder_file.read_text(encoding='utf-8').strip()
                self.encoder_input.insert('1.0', example)
            
        except Exception as e:
            print(f"Error al cargar ejemplos: {e}")


def main():
    """Función principal para ejecutar la GUI"""
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
