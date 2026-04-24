import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from datetime import datetime
import threading

from sentimiento.analizador import analizar_por_nivel
from almacenamiento.guardar import guardar_resultado
from almacenamiento.leer import leer_json, listar_archivos


class AplicacionSentimiento:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Sentimiento - Local")
        self.root.geometry("940x700")
        self._construir_ui()

    def _construir_ui(self):
        # ── Título
        tk.Label(self.root, text="🧠 ANÁLISIS DE SENTIMIENTO - LOCAL",
                 font=("Arial", 14, "bold")).pack(pady=8)

        # ── Área de texto
        frame_texto = tk.LabelFrame(self.root, text="Texto a analizar", padx=5, pady=5)
        frame_texto.pack(fill="x", padx=10)
        self.texto_entrada = scrolledtext.ScrolledText(frame_texto, height=5, wrap="word")
        self.texto_entrada.pack(fill="x")

        # ── Botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=6)
        tk.Button(frame_botones, text="🔍 ANALIZAR SENTIMIENTO",
                  command=self._analizar, bg="#d0e8ff").pack(side="left", padx=5)
        tk.Button(frame_botones, text="🧹 LIMPIAR",
                  command=self._limpiar).pack(side="left", padx=5)
        tk.Button(frame_botones, text="💾 GUARDAR",
                  command=self._guardar_manual).pack(side="left", padx=5)

        # ── Pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=4)

        self.tab_niveles     = ttk.Frame(self.notebook)
        self.tab_detallado   = ttk.Frame(self.notebook)
        self.tab_justif      = ttk.Frame(self.notebook)
        self.tab_historial   = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_niveles,   text="📊 Resultados por Nivel")
        self.notebook.add(self.tab_detallado, text="🔬 Análisis Detallado")
        self.notebook.add(self.tab_justif,    text="💡 Justificación & Recomendación")
        self.notebook.add(self.tab_historial, text="📋 Historial")

        self._construir_tab_niveles()
        self._construir_tab_detallado()
        self._construir_tab_justificacion()
        self._construir_tab_historial()

        # ── Leyenda polaridad
        frame_leyenda = tk.LabelFrame(self.root, text="¿Qué significa la polaridad?", padx=8, pady=4)
        frame_leyenda.pack(fill="x", padx=10, pady=2)
        tk.Label(frame_leyenda, text="🟢 POSITIVA (+0.00 a +1.00): El texto expresa emociones positivas",
                 fg="green").pack(anchor="w")
        tk.Label(frame_leyenda, text="🔴 NEGATIVA (-1.00 a -0.00): El texto expresa emociones negativas",
                 fg="red").pack(anchor="w")
        tk.Label(frame_leyenda, text="⚪ NEUTRAL (0.00): El texto no muestra emociones fuertes",
                 fg="gray").pack(anchor="w")

        # ── Barra de estado
        self.barra_estado = tk.StringVar(value="Listo")
        tk.Label(self.root, textvariable=self.barra_estado,
                 relief="sunken", anchor="w").pack(fill="x", side="bottom")

        self.ultimo_resultado = None

    # ── Construcción de pestañas ──────────────────────────────────

    def _construir_tab_niveles(self):
        cols = ("Nivel", "Sentimiento", "Polaridad", "Intensidad")
        self.tabla = ttk.Treeview(self.tab_niveles, columns=cols, show="headings", height=6)
        for col in cols:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=180)
        self.tabla.pack(fill="both", expand=True, padx=8, pady=8)

    def _construir_tab_detallado(self):
        self.texto_detallado = scrolledtext.ScrolledText(self.tab_detallado, wrap="word")
        self.texto_detallado.pack(fill="both", expand=True, padx=8, pady=8)

    def _construir_tab_justificacion(self):
        self.texto_justif = scrolledtext.ScrolledText(self.tab_justif, wrap="word")
        self.texto_justif.pack(fill="both", expand=True, padx=8, pady=8)

    def _construir_tab_historial(self):
        frame = tk.Frame(self.tab_historial)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        tk.Button(frame, text="🔄 Actualizar historial",
                  command=self._cargar_historial).pack(anchor="w", pady=4)
        self.lista_historial = tk.Listbox(frame, font=("Courier", 10))
        self.lista_historial.pack(fill="both", expand=True)

    # ── Acciones ──────────────────────────────────────────────────

    def _analizar(self):
        texto = self.texto_entrada.get("1.0", "end").strip()
        if not texto:
            messagebox.showwarning("Aviso", "Introduce un texto para analizar.")
            return
        self.barra_estado.set("⏳ Analizando...")
        threading.Thread(target=self._ejecutar_analisis, args=(texto,), daemon=True).start()

    def _ejecutar_analisis(self, texto):
        try:
            basico      = analizar_por_nivel(texto, "basico")
            intermedio  = analizar_por_nivel(texto, "intermedio")
            avanzado    = analizar_por_nivel(texto, "avanzado")

            self.ultimo_resultado = {
                "timestamp": datetime.now().isoformat(),
                "texto": texto,
                "basico": basico,
                "intermedio": intermedio,
                "avanzado": avanzado
            }

            self.root.after(0, self._actualizar_ui, basico, intermedio, avanzado, texto)
            guardar_resultado(self.ultimo_resultado)
            self.root.after(0, self.barra_estado.set,
                            "✅ Análisis completado y guardado automáticamente")
            self.root.after(0, self._cargar_historial)
        except Exception as e:
            self.root.after(0, self.barra_estado.set, f"❌ Error: {e}")

    def _actualizar_ui(self, basico, intermedio, avanzado, texto):
        # Tabla niveles
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        def polaridad(score):
            return f"{round(score * 100, 2)}%" if score else "-"

        def intensidad(score):
            if score is None: return "-"
            return "ALTA" if score >= 0.9 else "MEDIA" if score >= 0.7 else "BAJA"

        self.tabla.insert("", "end", values=(
            "Básico", basico["sentimiento"],
            polaridad(basico.get("confianza")), "-"),
            tags=("pos",) if basico["sentimiento"] == "POSITIVE" else ("neg",))
        self.tabla.insert("", "end", values=(
            "Intermedio", intermedio["sentimiento"],
            round(intermedio.get("confianza", 0), 2),
            intensidad(intermedio.get("confianza"))),
            tags=("pos",) if intermedio["sentimiento"] == "POSITIVE" else ("neg",))
        self.tabla.insert("", "end", values=(
            "Avanzado", avanzado["sentimiento"],
            round(avanzado.get("confianza", 0), 2), "-"),
            tags=("pos",) if avanzado["sentimiento"] == "POSITIVE" else ("neg",))

        self.tabla.tag_configure("pos", background="#e8f5e9")
        self.tabla.tag_configure("neg", background="#ffebee")

        # Análisis detallado
        self.texto_detallado.delete("1.0", "end")
        self.texto_detallado.insert("end",
            f"Texto analizado:\n{texto}\n\n"
            f"Sentimiento detectado : {avanzado['sentimiento']}\n"
            f"Confianza del modelo  : {round(avanzado.get('confianza', 0) * 100, 2)}%\n"
            f"Polaridad             : {'POSITIVA' if avanzado['sentimiento'] == 'POSITIVE' else 'NEGATIVA'}\n"
            f"Intensidad            : {intensidad(avanzado.get('confianza'))}\n"
        )

        # Justificación
        sent = avanzado["sentimiento"]
        confianza = avanzado.get("confianza", 0)
        self.texto_justif.delete("1.0", "end")
        self.texto_justif.insert("end",
            f"📌 Justificación del análisis\n"
            f"{'─' * 50}\n"
            f"El modelo ha clasificado el texto como {sent} "
            f"con una confianza del {round(confianza * 100, 2)}%.\n\n"
            f"💡 Recomendación\n"
            f"{'─' * 50}\n"
        )
        if sent == "POSITIVE":
            self.texto_justif.insert("end",
                "El texto transmite una valoración favorable. "
                "Adecuado para contextos de feedback positivo o recomendaciones.")
        else:
            self.texto_justif.insert("end",
                "El texto transmite una valoración desfavorable. "
                "Considera revisar el contenido si el objetivo es comunicar de forma positiva.")

    def _limpiar(self):
        self.texto_entrada.delete("1.0", "end")
        for row in self.tabla.get_children():
            self.tabla.delete(row)
        self.texto_detallado.delete("1.0", "end")
        self.texto_justif.delete("1.0", "end")
        self.barra_estado.set("Listo")
        self.ultimo_resultado = None

    def _guardar_manual(self):
        if not self.ultimo_resultado:
            messagebox.showwarning("Aviso", "No hay ningún análisis para guardar.")
            return
        guardar_resultado(self.ultimo_resultado)
        self.barra_estado.set("💾 Guardado manualmente con éxito")

    def _cargar_historial(self):
        self.lista_historial.delete(0, "end")
        try:
            archivos = listar_archivos("json")
            for archivo in sorted(archivos, reverse=True)[:20]:
                self.lista_historial.insert("end", archivo)
        except Exception:
            self.lista_historial.insert("end", "No hay resultados guardados aún.")


def iniciar_interfaz():
    root = tk.Tk()
    AplicacionSentimiento(root)
    root.mainloop()