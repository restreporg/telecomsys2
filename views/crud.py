"""
TelecomSys
Cumple: tkcalendar, validaciones, 2 temas, Treeview, confirmaciones, Pillow, iconografía ttk
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re, os
from datetime import date, datetime

# tkcalendar
try:
    from tkcalendar import DateEntry
    HAVE_CALENDAR = True
except ImportError:
    HAVE_CALENDAR = False

# Pillow
try:
    from PIL import Image, ImageTk
    HAVE_PIL = True
except ImportError:
    HAVE_PIL = False

from controllers.cliente_controller import ClienteController
from controllers.controllers import PlanController, ContratoController, FacturaController

# ── Paletas de colores ─────────────────────────────────────────────────────────
THEMES = {
    "Claro": {
        "bg":          "#F4F6FB",
        "sidebar":     "#1A237E",
        "sidebar_fg":  "#FFFFFF",
        "accent":      "#1976D2",
        "accent2":     "#00ACC1",
        "card":        "#FFFFFF",
        "text":        "#1A1A2E",
        "text2":       "#546E7A",
        "entry_bg":    "#FFFFFF",
        "entry_fg":    "#1A1A2E",
        "border":      "#CFD8DC",
        "success":     "#388E3C",
        "danger":      "#D32F2F",
        "warning":     "#F57C00",
        "info":        "#0288D1",
        "tree_head":   "#E3F2FD",
        "tree_row1":   "#FFFFFF",
        "tree_row2":   "#F0F4FF",
        "btn_save":    "#1976D2",
        "btn_update":  "#00897B",
        "btn_delete":  "#D32F2F",
        "btn_clear":   "#7B1FA2",
        "btn_export":  "#E65100",
        "tab_sel":     "#1976D2",
        "tab_bg":      "#E8EAF6",
    },
    "Oscuro": {
        "bg":          "#0D1117",
        "sidebar":     "#161B22",
        "sidebar_fg":  "#E6EDF3",
        "accent":      "#58A6FF",
        "accent2":     "#3FB950",
        "card":        "#1C2128",
        "text":        "#E6EDF3",
        "text2":       "#8B949E",
        "entry_bg":    "#21262D",
        "entry_fg":    "#E6EDF3",
        "border":      "#30363D",
        "success":     "#3FB950",
        "danger":      "#F85149",
        "warning":     "#D29922",
        "info":        "#58A6FF",
        "tree_head":   "#161B22",
        "tree_row1":   "#1C2128",
        "tree_row2":   "#21262D",
        "btn_save":    "#238636",
        "btn_update":  "#1F6FEB",
        "btn_delete":  "#DA3633",
        "btn_clear":   "#6E40C9",
        "btn_export":  "#C9510C",
        "tab_sel":     "#58A6FF",
        "tab_bg":      "#161B22",
    },
}

EMAIL_RE = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")

#  VENTANA PRINCIPAL
class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TelecomSys – Conexión Total S.A.")
        self.geometry("1280x800")
        self.minsize(1100, 700)
        self.theme_name = tk.StringVar(value="Claro")
        self.T = THEMES["Claro"]
        self._set_favicon()
        self._build_ui()
        self._apply_theme()

    # ── Favicon ──
    def _set_favicon(self):
        ico_path = os.path.join(os.path.dirname(__file__),
                                "..", "assets", "favicons", "favicon.ico")
        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except Exception:
                pass

    # ── Layout raíz ──
    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Contenido
        self.content = tk.Frame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content.rowconfigure(0, weight=1)
        self.content.columnconfigure(0, weight=1)

        self._build_sidebar()
        self._build_notebook()

    # ── Sidebar ──
    def _build_sidebar(self):
        T = self.T
        for w in self.sidebar.winfo_children():
            w.destroy()
        self.sidebar.configure(bg=T["sidebar"])

        # Logo / título
        lf = tk.Frame(self.sidebar, bg=T["sidebar"])
        lf.pack(fill="x", pady=(20, 5), padx=10)
        tk.Label(lf, text="📡", font=("Segoe UI Emoji", 26),
                 bg=T["sidebar"], fg=T["accent2"]).pack()
        tk.Label(lf, text="TelecomSys", font=("Segoe UI", 13, "bold"),
                 bg=T["sidebar"], fg=T["sidebar_fg"]).pack()
        tk.Label(lf, text="Conexión Total S.A.", font=("Segoe UI", 8),
                 bg=T["sidebar"], fg=T["text2"]).pack()

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)

        # Navegación
        nav_items = [
            ("👤  Clientes",    0),
            ("📋  Planes",      1),
            ("📄  Contratos",   2),
            ("🧾  Facturación", 3),
        ]
        self._nav_btns = []
        for label, idx in nav_items:
            btn = tk.Button(
                self.sidebar, text=label,
                font=("Segoe UI", 10, "bold"),
                bg=T["sidebar"], fg=T["sidebar_fg"],
                activebackground=T["accent"], activeforeground="#FFFFFF",
                relief="flat", anchor="w", padx=18, pady=8, cursor="hand2",
                command=lambda i=idx: self.notebook.select(i),
            )
            btn.pack(fill="x", pady=1)
            self._nav_btns.append(btn)

        ttk.Separator(self.sidebar, orient="horizontal").pack(fill="x", padx=10, pady=10)

        # Selector de tema
        tk.Label(self.sidebar, text="🎨  Tema", font=("Segoe UI", 9),
                 bg=T["sidebar"], fg=T["text2"]).pack(anchor="w", padx=18)
        for tname in THEMES:
            rb = tk.Radiobutton(
                self.sidebar, text=tname, variable=self.theme_name, value=tname,
                font=("Segoe UI", 9), bg=T["sidebar"], fg=T["sidebar_fg"],
                activebackground=T["sidebar"], selectcolor=T["accent"],
                command=self._apply_theme, relief="flat",
            )
            rb.pack(anchor="w", padx=28)

        # Versión
        tk.Label(self.sidebar, text="v1.0.0", font=("Segoe UI", 8),
                 bg=T["sidebar"], fg=T["text2"]).pack(side="bottom", pady=10)

    # ── Notebook ──
    def _build_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        self.notebook = ttk.Notebook(self.content)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Tabs
        self.tab_clientes   = ttk.Frame(self.notebook)
        self.tab_planes     = ttk.Frame(self.notebook)
        self.tab_contratos  = ttk.Frame(self.notebook)
        self.tab_facturas   = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_clientes,  text="  👤 Clientes  ")
        self.notebook.add(self.tab_planes,    text="  📋 Planes  ")
        self.notebook.add(self.tab_contratos, text="  📄 Contratos  ")
        self.notebook.add(self.tab_facturas,  text="  🧾 Facturación  ")

        # Construir cada tab
        self._build_tab_clientes()
        self._build_tab_planes()
        self._build_tab_contratos()
        self._build_tab_facturas()

    #  HELPERS REUTILIZABLES
    def _card(self, parent, title=""):
        T = self.T
        outer = tk.Frame(parent, bg=T["bg"])
        outer.pack(fill="both", expand=True, padx=12, pady=8)
        if title:
            tk.Label(outer, text=title, font=("Segoe UI", 13, "bold"),
                     bg=T["bg"], fg=T["accent"]).pack(anchor="w", pady=(0, 6))
        card = tk.Frame(outer, bg=T["card"],
                        highlightbackground=T["border"],
                        highlightthickness=1)
        card.pack(fill="both", expand=True)
        return card

    def _lbl_entry(self, parent, label, row, col=0, width=22, readonly=False):
        """Label + Entry con grid. Retorna el Entry."""
        T = self.T
        tk.Label(parent, text=label, font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=row, column=col*2, sticky="w", padx=(12, 4), pady=4)
        state = "readonly" if readonly else "normal"
        e = tk.Entry(parent, width=width, font=("Segoe UI", 10),
                     bg=T["entry_bg"], fg=T["entry_fg"],
                     insertbackground=T["text"],
                     relief="flat", bd=0,
                     highlightbackground=T["border"],
                     highlightthickness=1,
                     state=state)
        e.grid(row=row, column=col*2+1, sticky="ew", padx=(0, 12), pady=4)
        return e

    def _lbl_combo(self, parent, label, row, values, col=0, width=20):
        T = self.T
        tk.Label(parent, text=label, font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=row, column=col*2, sticky="w", padx=(12, 4), pady=4)
        cb = ttk.Combobox(parent, values=values, width=width,
                          font=("Segoe UI", 10), state="readonly")
        cb.grid(row=row, column=col*2+1, sticky="ew", padx=(0, 12), pady=4)
        return cb

    def _lbl_date(self, parent, label, row, col=0, width=14):
        T = self.T
        tk.Label(parent, text=label, font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=row, column=col*2, sticky="w", padx=(12, 4), pady=4)
        if HAVE_CALENDAR:
            de = DateEntry(parent, width=width, font=("Segoe UI", 10),
                           date_pattern="yyyy-mm-dd",
                           background=T["accent"], foreground="#ffffff",
                           borderwidth=1)
        else:
            de = tk.Entry(parent, width=width, font=("Segoe UI", 10),
                          bg=T["entry_bg"], fg=T["entry_fg"],
                          relief="flat", bd=0,
                          highlightbackground=T["border"],
                          highlightthickness=1)
        de.grid(row=row, column=col*2+1, sticky="w", padx=(0, 12), pady=4)
        return de

    def _btn(self, parent, text, color, command, icon=""):
        T = self.T
        b = tk.Button(parent,
                      text=f"{icon}  {text}" if icon else text,
                      font=("Segoe UI", 9, "bold"),
                      bg=color, fg="#FFFFFF",
                      activebackground=color,
                      relief="flat", cursor="hand2",
                      padx=12, pady=6,
                      command=command)
        b.pack(side="left", padx=4, pady=6)
        return b

    def _treeview(self, parent, columns):
        T = self.T
        frame = tk.Frame(parent, bg=T["card"])
        frame.pack(fill="both", expand=True, padx=8, pady=6)

        vsb = ttk.Scrollbar(frame, orient="vertical")
        hsb = ttk.Scrollbar(frame, orient="horizontal")

        style = ttk.Style()
        style.configure("Custom.Treeview",
                         font=("Segoe UI", 9),
                         rowheight=24,
                         background=T["tree_row1"],
                         fieldbackground=T["tree_row1"],
                         foreground=T["text"])
        style.configure("Custom.Treeview.Heading",
                         font=("Segoe UI", 9, "bold"),
                         background=T["tree_head"],
                         foreground=T["accent"])
        style.map("Custom.Treeview",
                  background=[("selected", T["accent"])],
                  foreground=[("selected", "#FFFFFF")])

        tv = ttk.Treeview(frame, columns=columns, show="headings",
                          yscrollcommand=vsb.set, xscrollcommand=hsb.set,
                          style="Custom.Treeview")
        vsb.configure(command=tv.yview)
        hsb.configure(command=tv.xview)

        vsb.pack(side="right",  fill="y")
        hsb.pack(side="bottom", fill="x")
        tv.pack(fill="both", expand=True)

        tv.tag_configure("odd",  background=T["tree_row1"])
        tv.tag_configure("even", background=T["tree_row2"])
        return tv

    def _get_date_value(self, widget):
        """Obtiene la fecha de DateEntry o Entry como string YYYY-MM-DD."""
        if HAVE_CALENDAR and isinstance(widget, DateEntry):
            return widget.get_date().isoformat()
        else:
            return widget.get().strip()

    def _set_date_value(self, widget, val):
        """Pone un valor de fecha en DateEntry o Entry."""
        if not val:
            return
        if HAVE_CALENDAR and isinstance(widget, DateEntry):
            try:
                if isinstance(val, str):
                    val = datetime.strptime(val[:10], "%Y-%m-%d").date()
                widget.set_date(val)
            except Exception:
                pass
        else:
            widget.delete(0, "end")
            widget.insert(0, str(val)[:10] if val else "")

    def _clear_entry(self, widget):
        if HAVE_CALENDAR and isinstance(widget, DateEntry):
            widget.set_date(date.today())
        else:
            widget.configure(state="normal")
            widget.delete(0, "end")

    def _get_entry(self, widget):
        return widget.get().strip()

    def _set_entry(self, widget, val):
        widget.configure(state="normal")
        widget.delete(0, "end")
        widget.insert(0, str(val) if val else "")

    def _show_error(self, msg):
        messagebox.showerror("Error de validación", msg)

    def _show_success(self, msg):
        messagebox.showinfo("Operación exitosa", msg)

    def _confirm(self, msg):
        return messagebox.askyesno("Confirmar operación", msg)

    def _image_picker(self, preview_label, var_path: list):
        """Abre diálogo para seleccionar imagen y muestra preview."""
        path = filedialog.askopenfilename(
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif"),
                       ("Todos", "*.*")])
        if not path:
            return
        var_path[0] = os.path.basename(path)
        if HAVE_PIL and preview_label:
            try:
                img = Image.open(path)
                img.thumbnail((80, 80))
                photo = ImageTk.PhotoImage(img)
                preview_label.configure(image=photo, text="")
                preview_label._photo = photo
            except Exception:
                preview_label.configure(text="[img]")


    #  TAB CLIENTES
    def _build_tab_clientes(self):
        T = self.T
        tab = self.tab_clientes
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # ── Barra superior ──
        bar = tk.Frame(tab, bg=T["bg"])
        bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))
        tk.Label(bar, text="👤  Gestión de Clientes",
                 font=("Segoe UI", 14, "bold"),
                 bg=T["bg"], fg=T["text"]).pack(side="left")

        # Búsqueda
        srch_frame = tk.Frame(bar, bg=T["bg"])
        srch_frame.pack(side="right")
        self.cli_search = tk.Entry(srch_frame, width=22, font=("Segoe UI", 10),
                                   bg=T["entry_bg"], fg=T["entry_fg"],
                                   relief="flat", highlightbackground=T["border"],
                                   highlightthickness=1)
        self.cli_search.pack(side="left", padx=4)
        tk.Button(srch_frame, text="🔍 Buscar",
                  font=("Segoe UI", 9), bg=T["info"], fg="#fff",
                  relief="flat", cursor="hand2", padx=8,
                  command=self._cli_search).pack(side="left", padx=2)
        tk.Button(srch_frame, text="↺ Todos",
                  font=("Segoe UI", 9), bg=T["text2"], fg="#fff",
                  relief="flat", cursor="hand2", padx=8,
                  command=self._cli_load_all).pack(side="left", padx=2)

        # ── PanedWindow ──
        paned = ttk.PanedWindow(tab, orient="horizontal")
        paned.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        # ─ Formulario izquierdo ─
        form_outer = tk.Frame(paned, bg=T["card"],
                              highlightbackground=T["border"],
                              highlightthickness=1)
        paned.add(form_outer, weight=40)
        form_outer.columnconfigure(1, weight=1)
        form_outer.columnconfigure(3, weight=1)

        tk.Label(form_outer, text="Datos del Cliente",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).grid(
            row=0, column=0, columnspan=4, sticky="w", padx=12, pady=(10, 4))

        self.cli_id_var = tk.StringVar()
        self.cli_id_entry = self._lbl_entry(form_outer, "ClienteID *", 1, readonly=True)

        self.cli_tipo = self._lbl_combo(form_outer, "Tipo *", 2,
                                        ["Personal", "Empresarial"])
        self.cli_nombre = self._lbl_entry(form_outer, "Nombre / Razón Social *", 3, width=28)
        self.cli_doc    = self._lbl_entry(form_outer, "Documento / RUC *", 4, width=22)
        self.cli_fecha  = self._lbl_date(form_outer,  "Fecha Nac./Constitución", 5)
        self.cli_dir    = self._lbl_entry(form_outer, "Dirección", 6, width=28)
        self.cli_tel    = self._lbl_entry(form_outer, "Teléfono", 7, width=20)
        self.cli_email  = self._lbl_entry(form_outer, "Correo Electrónico", 8, width=26)
        self.cli_clasif = self._lbl_combo(form_outer, "Clasificación Crediticia *", 9,
                                          ["A", "B", "C", "D"])
        self.cli_estado = self._lbl_combo(form_outer, "Estado", 10,
                                          ["Activo", "Inactivo"])
        self.cli_estado.set("Activo")

        # Imagen
        img_frame = tk.Frame(form_outer, bg=T["card"])
        img_frame.grid(row=11, column=0, columnspan=4, padx=12, pady=4, sticky="w")
        tk.Label(img_frame, text="Foto:", font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).pack(side="left")
        self.cli_foto_path = [""]
        self.cli_foto_preview = tk.Label(img_frame, text="[sin imagen]",
                                         width=10, height=4,
                                         bg=T["entry_bg"], fg=T["text2"],
                                         relief="flat")
        self.cli_foto_preview.pack(side="left", padx=8)
        tk.Button(img_frame, text="📁 Seleccionar",
                  font=("Segoe UI", 9), bg=T["accent"], fg="#fff",
                  relief="flat", cursor="hand2",
                  command=lambda: self._image_picker(
                      self.cli_foto_preview, self.cli_foto_path)
                  ).pack(side="left")

        # Botones
        btn_bar = tk.Frame(form_outer, bg=T["card"])
        btn_bar.grid(row=12, column=0, columnspan=4, pady=8, sticky="ew")
        self._btn(btn_bar, "Guardar",    T["btn_save"],   self._cli_insert, "💾")
        self._btn(btn_bar, "Actualizar", T["btn_update"], self._cli_update, "✏️")
        self._btn(btn_bar, "Eliminar",   T["btn_delete"], self._cli_delete, "🗑️")
        self._btn(btn_bar, "Limpiar",    T["btn_clear"],  self._cli_clear,  "✕")

        # ─ Treeview derecho ─
        tree_outer = tk.Frame(paned, bg=T["card"],
                              highlightbackground=T["border"],
                              highlightthickness=1)
        paned.add(tree_outer, weight=60)
        tree_outer.rowconfigure(1, weight=1)
        tree_outer.columnconfigure(0, weight=1)

        tk.Label(tree_outer, text="Lista de Clientes",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).pack(anchor="w", padx=12, pady=(10, 4))

        cols = ("ID", "Tipo", "Nombre/Razón", "Documento",
                "Teléfono", "Email", "Clasif.", "Estado")
        self.cli_tree = self._treeview(tree_outer, cols)
        for c, w in zip(cols, [50, 90, 180, 110, 110, 160, 55, 70]):
            self.cli_tree.heading(c, text=c)
            self.cli_tree.column(c, width=w, minwidth=40)
        self.cli_tree.bind("<<TreeviewSelect>>", self._cli_on_select)

        # Export bar
        exp_bar = tk.Frame(tree_outer, bg=T["card"])
        exp_bar.pack(fill="x", padx=8, pady=4)
        self._btn(exp_bar, "Excel", T["btn_export"], self._cli_export_excel, "📊")
        self._btn(exp_bar, "PDF",   T["btn_export"], self._cli_export_pdf,   "📄")

        self._cli_load_all()

    def _cli_get_fields(self):
        return dict(
            tipo     = self.cli_tipo.get(),
            nombre   = self._get_entry(self.cli_nombre),
            documento= self._get_entry(self.cli_doc),
            fecha_nac= self._get_date_value(self.cli_fecha),
            direccion= self._get_entry(self.cli_dir),
            telefono = self._get_entry(self.cli_tel),
            email    = self._get_entry(self.cli_email),
            clasif   = self.cli_clasif.get(),
            estado   = self.cli_estado.get(),
            foto     = self.cli_foto_path[0],
        )

    def _cli_load_all(self):
        self.cli_search.delete(0, "end")
        self._cli_fill_tree(ClienteController.get_all())

    def _cli_search(self):
        term = self.cli_search.get().strip()
        if not term:
            self._cli_load_all(); return
        self._cli_fill_tree(ClienteController.search(term))

    def _cli_fill_tree(self, rows):
        self.cli_tree.delete(*self.cli_tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.cli_tree.insert("", "end", tags=(tag,), values=(
                r["ClienteID"], r["Tipo"], r["NombreRazon"],
                r["Documento"], r["Telefono"] or "", r["Email"] or "",
                r["ClasifCrediticia"], r["Estado"]))

    def _cli_on_select(self, _=None):
        sel = self.cli_tree.selection()
        if not sel: return
        vals = self.cli_tree.item(sel[0], "values")
        row = ClienteController.get_by_id(vals[0])
        if not row: return
        self._cli_clear()
        self._set_entry(self.cli_id_entry, row["ClienteID"])
        self.cli_tipo.set(row["Tipo"])
        self._set_entry(self.cli_nombre, row["NombreRazon"])
        self._set_entry(self.cli_doc,    row["Documento"])
        self._set_date_value(self.cli_fecha, row["FechaNacConst"])
        self._set_entry(self.cli_dir,    row["Direccion"] or "")
        self._set_entry(self.cli_tel,    row["Telefono"] or "")
        self._set_entry(self.cli_email,  row["Email"] or "")
        self.cli_clasif.set(row["ClasifCrediticia"])
        self.cli_estado.set(row["Estado"])
        self.cli_foto_path[0] = row["Foto"] or ""

    def _cli_insert(self):
        f = self._cli_get_fields()
        try:
            ClienteController.insert(**{k: v for k, v in f.items()
                                        if k != "estado"})
            self._show_success("Cliente guardado correctamente.")
            self._cli_clear(); self._cli_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _cli_update(self):
        cid = self._get_entry(self.cli_id_entry)
        if not cid:
            self._show_error("Seleccione un cliente de la lista."); return
        if not self._confirm("¿Confirma la actualización de este cliente?"):
            return
        f = self._cli_get_fields()
        try:
            ClienteController.update(cid, f["tipo"], f["nombre"], f["documento"],
                                     f["fecha_nac"], f["direccion"], f["telefono"],
                                     f["email"], f["clasif"], f["estado"], f["foto"])
            self._show_success("Cliente actualizado correctamente.")
            self._cli_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _cli_delete(self):
        cid = self._get_entry(self.cli_id_entry)
        if not cid:
            self._show_error("Seleccione un cliente de la lista."); return
        if not self._confirm("¿Confirma la ELIMINACIÓN de este cliente?\nEsta acción no se puede deshacer."):
            return
        try:
            ClienteController.delete(cid)
            self._show_success("Cliente eliminado correctamente.")
            self._cli_clear(); self._cli_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _cli_clear(self):
        for w in [self.cli_id_entry, self.cli_nombre, self.cli_doc,
                  self.cli_dir, self.cli_tel, self.cli_email]:
            self._clear_entry(w)
        self._clear_entry(self.cli_fecha)
        self.cli_tipo.set("")
        self.cli_clasif.set("")
        self.cli_estado.set("Activo")
        self.cli_foto_path[0] = ""
        self.cli_foto_preview.configure(text="[sin imagen]", image="")

    def _cli_export_excel(self):
        from views.export_view import ExportView
        rows = ClienteController.get_all()
        cols = ["ClienteID","Tipo","NombreRazon","Documento",
                "Telefono","Email","ClasifCrediticia","Estado"]
        ExportView.to_excel(rows, cols, "clientes")

    def _cli_export_pdf(self):
        from views.export_view import ExportView
        rows = ClienteController.get_all()
        cols = ["ClienteID","Tipo","NombreRazon","Documento",
                "Telefono","Email","ClasifCrediticia","Estado"]
        ExportView.to_pdf(rows, cols, "Reporte de Clientes")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB PLANES
    # ══════════════════════════════════════════════════════════════════════════
    def _build_tab_planes(self):
        T = self.T
        tab = self.tab_planes
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        bar = tk.Frame(tab, bg=T["bg"])
        bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))
        tk.Label(bar, text="📋  Gestión de Planes",
                 font=("Segoe UI", 14, "bold"),
                 bg=T["bg"], fg=T["text"]).pack(side="left")

        srch = tk.Frame(bar, bg=T["bg"])
        srch.pack(side="right")
        self.pln_search = tk.Entry(srch, width=22, font=("Segoe UI", 10),
                                   bg=T["entry_bg"], fg=T["entry_fg"],
                                   relief="flat", highlightbackground=T["border"],
                                   highlightthickness=1)
        self.pln_search.pack(side="left", padx=4)
        tk.Button(srch, text="🔍 Buscar", font=("Segoe UI", 9),
                  bg=T["info"], fg="#fff", relief="flat", cursor="hand2", padx=8,
                  command=self._pln_search).pack(side="left", padx=2)
        tk.Button(srch, text="↺ Todos", font=("Segoe UI", 9),
                  bg=T["text2"], fg="#fff", relief="flat", cursor="hand2", padx=8,
                  command=self._pln_load_all).pack(side="left", padx=2)

        paned = ttk.PanedWindow(tab, orient="horizontal")
        paned.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        # ─ Formulario ─
        form = tk.Frame(paned, bg=T["card"],
                        highlightbackground=T["border"], highlightthickness=1)
        paned.add(form, weight=40)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="Datos del Plan",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 4))

        self.pln_id    = self._lbl_entry(form, "PlanID *", 1, readonly=True)
        self.pln_cod   = self._lbl_entry(form, "Código *", 2)
        self.pln_nom   = self._lbl_entry(form, "Nombre Comercial *", 3, width=26)
        self.pln_tipo  = self._lbl_combo(form, "Tipo Servicio *", 4,
                                         ["Telefonía Móvil", "Internet Fijo",
                                          "Televisión", "Paquete"])
        self.pln_desc  = self._lbl_entry(form, "Descripción", 5, width=28)
        self.pln_tar   = self._lbl_entry(form, "Tarifa Mensual *", 6)
        self.pln_perm  = self._lbl_entry(form, "Permanencia (meses) *", 7)
        self.pln_promo = self._lbl_entry(form, "Promoción", 8, width=26)
        self.pln_est   = self._lbl_combo(form, "Estado", 9,
                                         ["Vigente", "Descontinuado"])
        self.pln_est.set("Vigente")

        # Imagen plan
        img_f = tk.Frame(form, bg=T["card"])
        img_f.grid(row=10, column=0, columnspan=2, padx=12, pady=4, sticky="w")
        tk.Label(img_f, text="Imagen:", font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).pack(side="left")
        self.pln_img_path = [""]
        self.pln_img_prev = tk.Label(img_f, text="[sin imagen]",
                                     width=10, height=4,
                                     bg=T["entry_bg"], fg=T["text2"])
        self.pln_img_prev.pack(side="left", padx=8)
        tk.Button(img_f, text="📁 Seleccionar",
                  font=("Segoe UI", 9), bg=T["accent"], fg="#fff",
                  relief="flat", cursor="hand2",
                  command=lambda: self._image_picker(
                      self.pln_img_prev, self.pln_img_path)
                  ).pack(side="left")

        btn_bar = tk.Frame(form, bg=T["card"])
        btn_bar.grid(row=11, column=0, columnspan=2, pady=8)
        self._btn(btn_bar, "Guardar",    T["btn_save"],   self._pln_insert, "💾")
        self._btn(btn_bar, "Actualizar", T["btn_update"], self._pln_update, "✏️")
        self._btn(btn_bar, "Eliminar",   T["btn_delete"], self._pln_delete, "🗑️")
        self._btn(btn_bar, "Limpiar",    T["btn_clear"],  self._pln_clear,  "✕")

        # ─ Treeview ─
        tree_outer = tk.Frame(paned, bg=T["card"],
                              highlightbackground=T["border"], highlightthickness=1)
        paned.add(tree_outer, weight=60)
        tk.Label(tree_outer, text="Lista de Planes",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).pack(anchor="w", padx=12, pady=(10, 4))

        cols = ("ID", "Código", "Nombre Comercial", "Tipo",
                "Tarifa", "Permanencia", "Estado")
        self.pln_tree = self._treeview(tree_outer, cols)
        for c, w in zip(cols, [50, 100, 180, 120, 90, 100, 90]):
            self.pln_tree.heading(c, text=c)
            self.pln_tree.column(c, width=w, minwidth=40)
        self.pln_tree.bind("<<TreeviewSelect>>", self._pln_on_select)

        exp_bar = tk.Frame(tree_outer, bg=T["card"])
        exp_bar.pack(fill="x", padx=8, pady=4)
        self._btn(exp_bar, "Excel", T["btn_export"], self._pln_export_excel, "📊")
        self._btn(exp_bar, "PDF",   T["btn_export"], self._pln_export_pdf,   "📄")

        self._pln_load_all()

    def _pln_load_all(self):
        self.pln_search.delete(0, "end")
        self._pln_fill_tree(PlanController.get_all())

    def _pln_search(self):
        term = self.pln_search.get().strip()
        if not term: self._pln_load_all(); return
        self._pln_fill_tree(PlanController.search(term))

    def _pln_fill_tree(self, rows):
        self.pln_tree.delete(*self.pln_tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.pln_tree.insert("", "end", tags=(tag,), values=(
                r["PlanID"], r["Codigo"], r["NombreComercial"],
                r["Tipo"], f"${r['TarifaMensual']:,.0f}",
                f"{r['Permanencia']} meses", r["Estado"]))

    def _pln_on_select(self, _=None):
        sel = self.pln_tree.selection()
        if not sel: return
        vals = self.pln_tree.item(sel[0], "values")
        row = PlanController.get_by_id(vals[0])
        if not row: return
        self._pln_clear()
        self._set_entry(self.pln_id,   row["PlanID"])
        self._set_entry(self.pln_cod,  row["Codigo"])
        self._set_entry(self.pln_nom,  row["NombreComercial"])
        self.pln_tipo.set(row["Tipo"])
        self._set_entry(self.pln_desc, row["Descripcion"] or "")
        self._set_entry(self.pln_tar,  row["TarifaMensual"])
        self._set_entry(self.pln_perm, row["Permanencia"])
        self._set_entry(self.pln_promo,row["Promocion"] or "")
        self.pln_est.set(row["Estado"])
        self.pln_img_path[0] = row["Imagen"] or ""

    def _pln_insert(self):
        try:
            PlanController.insert(
                self._get_entry(self.pln_cod),
                self._get_entry(self.pln_nom),
                self.pln_tipo.get(),
                self._get_entry(self.pln_desc),
                self._get_entry(self.pln_tar),
                self._get_entry(self.pln_perm),
                self._get_entry(self.pln_promo),
                self.pln_img_path[0])
            self._show_success("Plan guardado correctamente.")
            self._pln_clear(); self._pln_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _pln_update(self):
        pid = self._get_entry(self.pln_id)
        if not pid: self._show_error("Seleccione un plan."); return
        if not self._confirm("¿Confirma la actualización del plan?"): return
        try:
            PlanController.update(
                pid,
                self._get_entry(self.pln_cod),
                self._get_entry(self.pln_nom),
                self.pln_tipo.get(),
                self._get_entry(self.pln_desc),
                self._get_entry(self.pln_tar),
                self._get_entry(self.pln_perm),
                self._get_entry(self.pln_promo),
                self.pln_est.get(),
                self.pln_img_path[0])
            self._show_success("Plan actualizado correctamente.")
            self._pln_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _pln_delete(self):
        pid = self._get_entry(self.pln_id)
        if not pid: self._show_error("Seleccione un plan."); return
        if not self._confirm("¿Confirma la ELIMINACIÓN del plan?"): return
        try:
            PlanController.delete(pid)
            self._show_success("Plan eliminado.")
            self._pln_clear(); self._pln_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _pln_clear(self):
        for w in [self.pln_id, self.pln_cod, self.pln_nom,
                  self.pln_desc, self.pln_tar, self.pln_perm, self.pln_promo]:
            self._clear_entry(w)
        self.pln_tipo.set("")
        self.pln_est.set("Vigente")
        self.pln_img_path[0] = ""
        self.pln_img_prev.configure(text="[sin imagen]", image="")

    def _pln_export_excel(self):
        from views.export_view import ExportView
        rows = PlanController.get_all()
        cols = ["PlanID","Codigo","NombreComercial","Tipo",
                "TarifaMensual","Permanencia","Promocion","Estado"]
        ExportView.to_excel(rows, cols, "planes")

    def _pln_export_pdf(self):
        from views.export_view import ExportView
        rows = PlanController.get_all()
        cols = ["PlanID","Codigo","NombreComercial","Tipo",
                "TarifaMensual","Permanencia","Estado"]
        ExportView.to_pdf(rows, cols, "Reporte de Planes")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB CONTRATOS
    # ══════════════════════════════════════════════════════════════════════════
    def _build_tab_contratos(self):
        T = self.T
        tab = self.tab_contratos
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        bar = tk.Frame(tab, bg=T["bg"])
        bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))
        tk.Label(bar, text="📄  Gestión de Contratos",
                 font=("Segoe UI", 14, "bold"),
                 bg=T["bg"], fg=T["text"]).pack(side="left")

        paned = ttk.PanedWindow(tab, orient="horizontal")
        paned.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        # ─ Formulario ─
        form = tk.Frame(paned, bg=T["card"],
                        highlightbackground=T["border"], highlightthickness=1)
        paned.add(form, weight=40)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="Datos del Contrato",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 4))

        self.ctr_id     = self._lbl_entry(form, "ContratoID", 1, readonly=True)
        self.ctr_num    = self._lbl_entry(form, "Número Contrato *", 2)
        self.ctr_firma  = self._lbl_date(form,  "Fecha Firma *", 3)
        self.ctr_inicio = self._lbl_date(form,  "Fecha Inicio *", 4)

        # Combos cliente / plan (con datos de DB)
        tk.Label(form, text="Cliente *", font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=5, column=0, sticky="w", padx=(12, 4), pady=4)
        self.ctr_cli_combo = ttk.Combobox(form, width=26,
                                           font=("Segoe UI", 10), state="readonly")
        self.ctr_cli_combo.grid(row=5, column=1, sticky="ew", padx=(0, 12), pady=4)
        self._ctr_load_combos()

        tk.Label(form, text="Plan *", font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=6, column=0, sticky="w", padx=(12, 4), pady=4)
        self.ctr_pln_combo = ttk.Combobox(form, width=26,
                                           font=("Segoe UI", 10), state="readonly")
        self.ctr_pln_combo.grid(row=6, column=1, sticky="ew", padx=(0, 12), pady=4)
        self._ctr_load_plan_combo()

        self.ctr_dir     = self._lbl_entry(form, "Dir. Instalación", 7, width=26)
        self.ctr_equip   = self._lbl_entry(form, "Equipos Incluidos", 8, width=26)
        self.ctr_cond    = self._lbl_entry(form, "Condiciones Esp.", 9, width=26)
        self.ctr_dur     = self._lbl_entry(form, "Duración (meses) *", 10)
        self.ctr_monto   = self._lbl_entry(form, "Monto Mensual *", 11)
        self.ctr_est     = self._lbl_combo(form, "Estado", 12,
                                           ["Activo", "Suspendido",
                                            "Cancelado", "Vencido"])
        self.ctr_est.set("Activo")

        btn_bar = tk.Frame(form, bg=T["card"])
        btn_bar.grid(row=13, column=0, columnspan=2, pady=8)
        self._btn(btn_bar, "Guardar",    T["btn_save"],   self._ctr_insert, "💾")
        self._btn(btn_bar, "Actualizar", T["btn_update"], self._ctr_update, "✏️")
        self._btn(btn_bar, "Eliminar",   T["btn_delete"], self._ctr_delete, "🗑️")
        self._btn(btn_bar, "Limpiar",    T["btn_clear"],  self._ctr_clear,  "✕")

        # ─ Treeview ─
        tree_outer = tk.Frame(paned, bg=T["card"],
                              highlightbackground=T["border"], highlightthickness=1)
        paned.add(tree_outer, weight=60)
        tk.Label(tree_outer, text="Lista de Contratos",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).pack(anchor="w", padx=12, pady=(10, 4))

        cols = ("ID", "Número", "Fecha Firma", "Cliente",
                "Plan", "F.Inicio", "Duración", "Monto", "Estado")
        self.ctr_tree = self._treeview(tree_outer, cols)
        for c, w in zip(cols, [50, 110, 90, 150, 150, 90, 70, 90, 80]):
            self.ctr_tree.heading(c, text=c)
            self.ctr_tree.column(c, width=w, minwidth=40)
        self.ctr_tree.bind("<<TreeviewSelect>>", self._ctr_on_select)

        exp_bar = tk.Frame(tree_outer, bg=T["card"])
        exp_bar.pack(fill="x", padx=8, pady=4)
        self._btn(exp_bar, "Excel", T["btn_export"], self._ctr_export_excel, "📊")
        self._btn(exp_bar, "PDF",   T["btn_export"], self._ctr_export_pdf,   "📄")

        self._ctr_load_all()

    def _ctr_load_combos(self):
        self._ctr_clientes = ClienteController.get_combo()
        opts = [f"{r['ClienteID']} – {r['NombreRazon']}"
                for r in self._ctr_clientes]
        self.ctr_cli_combo["values"] = opts

    def _ctr_load_plan_combo(self):
        self._ctr_planes = PlanController.get_combo()
        opts = [f"{r['PlanID']} – {r['NombreComercial']}"
                for r in self._ctr_planes]
        self.ctr_pln_combo["values"] = opts

    def _ctr_get_cliente_id(self):
        sel = self.ctr_cli_combo.get()
        if sel:
            return int(sel.split("–")[0].strip())
        return None

    def _ctr_get_plan_id(self):
        sel = self.ctr_pln_combo.get()
        if sel:
            return int(sel.split("–")[0].strip())
        return None

    def _ctr_load_all(self):
        self._ctr_fill_tree(ContratoController.get_all())

    def _ctr_fill_tree(self, rows):
        self.ctr_tree.delete(*self.ctr_tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.ctr_tree.insert("", "end", tags=(tag,), values=(
                r["ContratoID"], r["NumeroContrato"],
                str(r["FechaFirma"])[:10] if r["FechaFirma"] else "",
                r["ClienteNombre"], r["PlanNombre"],
                str(r["FechaInicio"])[:10] if r["FechaInicio"] else "",
                f"{r['DuracionMeses']} m",
                f"${r['MontoMensual']:,.0f}",
                r["Estado"]))

    def _ctr_on_select(self, _=None):
        sel = self.ctr_tree.selection()
        if not sel: return
        vals = self.ctr_tree.item(sel[0], "values")
        row = ContratoController.get_by_id(vals[0])
        if not row: return
        self._ctr_clear()
        self._set_entry(self.ctr_id,  row["ContratoID"])
        self._set_entry(self.ctr_num, row["NumeroContrato"])
        self._set_date_value(self.ctr_firma,  row["FechaFirma"])
        self._set_date_value(self.ctr_inicio, row["FechaInicio"])
        # set combos
        for i, r in enumerate(self._ctr_clientes):
            if r["ClienteID"] == row["ClienteID"]:
                self.ctr_cli_combo.current(i); break
        for i, r in enumerate(self._ctr_planes):
            if r["PlanID"] == row["PlanID"]:
                self.ctr_pln_combo.current(i); break
        self._set_entry(self.ctr_dir,   row["DirInstalacion"] or "")
        self._set_entry(self.ctr_equip, row["EquiposIncluidos"] or "")
        self._set_entry(self.ctr_cond,  row["CondicionesEsp"] or "")
        self._set_entry(self.ctr_dur,   row["DuracionMeses"])
        self._set_entry(self.ctr_monto, row["MontoMensual"])
        self.ctr_est.set(row["Estado"])

    def _ctr_insert(self):
        try:
            ContratoController.insert(
                self._get_entry(self.ctr_num),
                self._get_date_value(self.ctr_firma),
                self._ctr_get_cliente_id(),
                self._ctr_get_plan_id(),
                self._get_entry(self.ctr_dir),
                self._get_entry(self.ctr_equip),
                self._get_entry(self.ctr_cond),
                self._get_date_value(self.ctr_inicio),
                self._get_entry(self.ctr_dur),
                self._get_entry(self.ctr_monto))
            self._show_success("Contrato guardado correctamente.")
            self._ctr_clear(); self._ctr_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _ctr_update(self):
        cid = self._get_entry(self.ctr_id)
        if not cid: self._show_error("Seleccione un contrato."); return
        if not self._confirm("¿Confirma la actualización del contrato?"): return
        try:
            ContratoController.update(
                cid,
                self._get_entry(self.ctr_num),
                self._get_date_value(self.ctr_firma),
                self._ctr_get_cliente_id(),
                self._ctr_get_plan_id(),
                self._get_entry(self.ctr_dir),
                self._get_entry(self.ctr_equip),
                self._get_entry(self.ctr_cond),
                self._get_date_value(self.ctr_inicio),
                self._get_entry(self.ctr_dur),
                self._get_entry(self.ctr_monto),
                self.ctr_est.get())
            self._show_success("Contrato actualizado.")
            self._ctr_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _ctr_delete(self):
        cid = self._get_entry(self.ctr_id)
        if not cid: self._show_error("Seleccione un contrato."); return
        if not self._confirm("¿Confirma la ELIMINACIÓN del contrato?"): return
        try:
            ContratoController.delete(cid)
            self._show_success("Contrato eliminado.")
            self._ctr_clear(); self._ctr_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _ctr_clear(self):
        for w in [self.ctr_id, self.ctr_num, self.ctr_dir,
                  self.ctr_equip, self.ctr_cond, self.ctr_dur, self.ctr_monto]:
            self._clear_entry(w)
        self._clear_entry(self.ctr_firma)
        self._clear_entry(self.ctr_inicio)
        self.ctr_cli_combo.set("")
        self.ctr_pln_combo.set("")
        self.ctr_est.set("Activo")

    def _ctr_export_excel(self):
        from views.export_view import ExportView
        rows = ContratoController.get_all()
        cols = ["ContratoID","NumeroContrato","FechaFirma","ClienteNombre",
                "PlanNombre","FechaInicio","DuracionMeses","MontoMensual","Estado"]
        ExportView.to_excel(rows, cols, "contratos")

    def _ctr_export_pdf(self):
        from views.export_view import ExportView
        rows = ContratoController.get_all()
        cols = ["ContratoID","NumeroContrato","FechaFirma","ClienteNombre",
                "PlanNombre","FechaInicio","DuracionMeses","MontoMensual","Estado"]
        ExportView.to_pdf(rows, cols, "Reporte de Contratos")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB FACTURAS
    # ══════════════════════════════════════════════════════════════════════════
    def _build_tab_facturas(self):
        T = self.T
        tab = self.tab_facturas
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        bar = tk.Frame(tab, bg=T["bg"])
        bar.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 0))
        tk.Label(bar, text="🧾  Gestión de Facturación",
                 font=("Segoe UI", 14, "bold"),
                 bg=T["bg"], fg=T["text"]).pack(side="left")

        # Filtro por rango de fechas
        rng = tk.Frame(bar, bg=T["bg"])
        rng.pack(side="right")
        tk.Label(rng, text="Desde:", font=("Segoe UI", 9),
                 bg=T["bg"], fg=T["text2"]).pack(side="left")
        self.fac_desde = self._date_mini(rng)
        tk.Label(rng, text="Hasta:", font=("Segoe UI", 9),
                 bg=T["bg"], fg=T["text2"]).pack(side="left", padx=(8, 0))
        self.fac_hasta = self._date_mini(rng)
        tk.Button(rng, text="🔍 Filtrar", font=("Segoe UI", 9),
                  bg=T["info"], fg="#fff", relief="flat", cursor="hand2", padx=8,
                  command=self._fac_filter).pack(side="left", padx=4)
        tk.Button(rng, text="↺ Todos", font=("Segoe UI", 9),
                  bg=T["text2"], fg="#fff", relief="flat", cursor="hand2", padx=8,
                  command=self._fac_load_all).pack(side="left", padx=2)

        paned = ttk.PanedWindow(tab, orient="horizontal")
        paned.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        tab.rowconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)

        # ─ Formulario ─
        form = tk.Frame(paned, bg=T["card"],
                        highlightbackground=T["border"], highlightthickness=1)
        paned.add(form, weight=40)
        form.columnconfigure(1, weight=1)

        tk.Label(form, text="Datos de la Factura",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 4))

        self.fac_id      = self._lbl_entry(form, "FacturaID", 1, readonly=True)
        self.fac_num     = self._lbl_entry(form, "Número Factura *", 2)
        self.fac_periodo = self._lbl_entry(form, "Período (YYYY-MM) *", 3)
        self.fac_emision = self._lbl_date(form,  "Fecha Emisión *", 4)
        self.fac_venc    = self._lbl_date(form,  "Fecha Vencimiento *", 5)

        # Combos cliente / contrato
        tk.Label(form, text="Cliente *", font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=6, column=0, sticky="w", padx=(12, 4), pady=4)
        self.fac_cli_combo = ttk.Combobox(form, width=26,
                                           font=("Segoe UI", 10), state="readonly")
        self.fac_cli_combo.grid(row=6, column=1, sticky="ew", padx=(0, 12), pady=4)

        tk.Label(form, text="Contrato *", font=("Segoe UI", 9, "bold"),
                 bg=T["card"], fg=T["text2"]).grid(
            row=7, column=0, sticky="w", padx=(12, 4), pady=4)
        self.fac_ctr_combo = ttk.Combobox(form, width=26,
                                           font=("Segoe UI", 10), state="readonly")
        self.fac_ctr_combo.grid(row=7, column=1, sticky="ew", padx=(0, 12), pady=4)
        self._fac_load_combos()

        self.fac_fijos    = self._lbl_entry(form, "Cargos Fijos *", 8)
        self.fac_var      = self._lbl_entry(form, "Cargos Variables *", 9)
        self.fac_desc     = self._lbl_entry(form, "Descuentos *", 10)
        self.fac_imp      = self._lbl_entry(form, "Impuestos *", 11)
        self.fac_total    = self._lbl_entry(form, "Total a Pagar", 12, readonly=True)
        self.fac_est_pago = self._lbl_combo(form, "Estado Pago", 13,
                                            ["Pendiente", "Pagada",
                                             "Vencida", "Anulada"])
        self.fac_est_pago.set("Pendiente")
        self.fac_forma    = self._lbl_combo(form, "Forma de Pago", 14,
                                            ["Efectivo", "Transferencia",
                                             "Tarjeta", "Débito Automático"])
        self.fac_fecha_pago = self._lbl_date(form, "Fecha Pago", 15)

        # Auto-calcular total
        for w in [self.fac_fijos, self.fac_var, self.fac_desc, self.fac_imp]:
            w.bind("<FocusOut>", lambda e: self._fac_calc_total())

        btn_bar = tk.Frame(form, bg=T["card"])
        btn_bar.grid(row=16, column=0, columnspan=2, pady=6)
        self._btn(btn_bar, "Guardar",    T["btn_save"],   self._fac_insert, "💾")
        self._btn(btn_bar, "Actualizar", T["btn_update"], self._fac_update, "✏️")
        self._btn(btn_bar, "Eliminar",   T["btn_delete"], self._fac_delete, "🗑️")
        self._btn(btn_bar, "Limpiar",    T["btn_clear"],  self._fac_clear,  "✕")
        self._btn(btn_bar, "Registrar Pago", T["btn_save"],
                  self._fac_pagar, "💳")

        # ─ Treeview ─
        tree_outer = tk.Frame(paned, bg=T["card"],
                              highlightbackground=T["border"], highlightthickness=1)
        paned.add(tree_outer, weight=60)
        tk.Label(tree_outer, text="Lista de Facturas",
                 font=("Segoe UI", 11, "bold"),
                 bg=T["card"], fg=T["accent"]).pack(anchor="w", padx=12, pady=(10, 4))

        cols = ("ID", "Número", "Período", "F.Emisión",
                "Cliente", "Total", "Estado", "Forma Pago")
        self.fac_tree = self._treeview(tree_outer, cols)
        for c, w in zip(cols, [50, 120, 80, 90, 150, 90, 80, 120]):
            self.fac_tree.heading(c, text=c)
            self.fac_tree.column(c, width=w, minwidth=40)
        self.fac_tree.bind("<<TreeviewSelect>>", self._fac_on_select)

        exp_bar = tk.Frame(tree_outer, bg=T["card"])
        exp_bar.pack(fill="x", padx=8, pady=4)
        self._btn(exp_bar, "Excel", T["btn_export"], self._fac_export_excel, "📊")
        self._btn(exp_bar, "PDF",   T["btn_export"], self._fac_export_pdf,   "📄")

        self._fac_load_all()

    def _date_mini(self, parent):
        T = self.T
        if HAVE_CALENDAR:
            w = DateEntry(parent, width=11, font=("Segoe UI", 9),
                          date_pattern="yyyy-mm-dd",
                          background=T["accent"], foreground="#fff", borderwidth=1)
        else:
            w = tk.Entry(parent, width=11, font=("Segoe UI", 9),
                         bg=T["entry_bg"], fg=T["entry_fg"],
                         relief="flat", highlightbackground=T["border"],
                         highlightthickness=1)
        w.pack(side="left", padx=2)
        return w

    def _fac_load_combos(self):
        self._fac_clientes = ClienteController.get_combo()
        self.fac_cli_combo["values"] = [
            f"{r['ClienteID']} – {r['NombreRazon']}"
            for r in self._fac_clientes]
        self._fac_contratos = ContratoController.get_combo()
        self.fac_ctr_combo["values"] = [
            f"{r['ContratoID']} – {r['NumeroContrato']} ({r['ClienteNombre']})"
            for r in self._fac_contratos]

    def _fac_get_cli_id(self):
        sel = self.fac_cli_combo.get()
        return int(sel.split("–")[0].strip()) if sel else None

    def _fac_get_ctr_id(self):
        sel = self.fac_ctr_combo.get()
        return int(sel.split("–")[0].strip()) if sel else None

    def _fac_calc_total(self):
        try:
            f = float(self._get_entry(self.fac_fijos) or 0)
            v = float(self._get_entry(self.fac_var)   or 0)
            d = float(self._get_entry(self.fac_desc)  or 0)
            i = float(self._get_entry(self.fac_imp)   or 0)
            total = f + v - d + i
            self._set_entry(self.fac_total, f"{total:,.2f}")
        except Exception:
            pass

    def _fac_load_all(self):
        self._fac_fill_tree(FacturaController.get_all())

    def _fac_filter(self):
        d = self._get_date_value(self.fac_desde)
        h = self._get_date_value(self.fac_hasta)
        if not d or not h:
            self._show_error("Ingrese ambas fechas para filtrar.")
            return
        self._fac_fill_tree(FacturaController.get_by_rango(d, h))

    def _fac_fill_tree(self, rows):
        self.fac_tree.delete(*self.fac_tree.get_children())
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.fac_tree.insert("", "end", tags=(tag,), values=(
                r["FacturaID"], r["NumeroFactura"],
                r["PeriodoFacturado"],
                str(r["FechaEmision"])[:10] if r["FechaEmision"] else "",
                r["ClienteNombre"],
                f"${r['TotalPagar']:,.0f}",
                r["EstadoPago"],
                r["FormaPago"] or ""))

    def _fac_on_select(self, _=None):
        sel = self.fac_tree.selection()
        if not sel: return
        vals = self.fac_tree.item(sel[0], "values")
        row = FacturaController.get_by_id(vals[0])
        if not row: return
        self._fac_clear()
        self._set_entry(self.fac_id,      row["FacturaID"])
        self._set_entry(self.fac_num,     row["NumeroFactura"])
        self._set_entry(self.fac_periodo, row["PeriodoFacturado"])
        self._set_date_value(self.fac_emision,    row["FechaEmision"])
        self._set_date_value(self.fac_venc,       row["FechaVencimiento"])
        for i, r in enumerate(self._fac_clientes):
            if r["ClienteID"] == row["ClienteID"]:
                self.fac_cli_combo.current(i); break
        for i, r in enumerate(self._fac_contratos):
            if r["ContratoID"] == row["ContratoID"]:
                self.fac_ctr_combo.current(i); break
        self._set_entry(self.fac_fijos, row["CargosFijos"])
        self._set_entry(self.fac_var,   row["CargosVariables"])
        self._set_entry(self.fac_desc,  row["Descuentos"])
        self._set_entry(self.fac_imp,   row["Impuestos"])
        self._set_entry(self.fac_total, row["TotalPagar"])
        self.fac_est_pago.set(row["EstadoPago"])
        if row["FormaPago"]:
            self.fac_forma.set(row["FormaPago"])
        self._set_date_value(self.fac_fecha_pago, row["FechaPago"])

    def _fac_insert(self):
        try:
            FacturaController.insert(
                self._get_entry(self.fac_num),
                self._get_entry(self.fac_periodo),
                self._get_date_value(self.fac_emision),
                self._get_date_value(self.fac_venc),
                self._fac_get_cli_id(),
                self._fac_get_ctr_id(),
                self._get_entry(self.fac_fijos)  or 0,
                self._get_entry(self.fac_var)    or 0,
                self._get_entry(self.fac_desc)   or 0,
                self._get_entry(self.fac_imp)    or 0)
            self._show_success("Factura guardada correctamente.")
            self._fac_clear(); self._fac_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _fac_update(self):
        fid = self._get_entry(self.fac_id)
        if not fid: self._show_error("Seleccione una factura."); return
        if not self._confirm("¿Confirma la actualización de la factura?"): return
        try:
            FacturaController.update(
                fid,
                self._get_entry(self.fac_num),
                self._get_entry(self.fac_periodo),
                self._get_date_value(self.fac_emision),
                self._get_date_value(self.fac_venc),
                self._fac_get_cli_id(),
                self._fac_get_ctr_id(),
                self._get_entry(self.fac_fijos) or 0,
                self._get_entry(self.fac_var)   or 0,
                self._get_entry(self.fac_desc)  or 0,
                self._get_entry(self.fac_imp)   or 0,
                self.fac_est_pago.get(),
                self.fac_forma.get() or None,
                self._get_date_value(self.fac_fecha_pago) or None)
            self._show_success("Factura actualizada.")
            self._fac_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _fac_delete(self):
        fid = self._get_entry(self.fac_id)
        if not fid: self._show_error("Seleccione una factura."); return
        if not self._confirm("¿Confirma la ELIMINACIÓN de la factura?"): return
        try:
            FacturaController.delete(fid)
            self._show_success("Factura eliminada.")
            self._fac_clear(); self._fac_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _fac_pagar(self):
        fid = self._get_entry(self.fac_id)
        if not fid: self._show_error("Seleccione una factura."); return
        forma = self.fac_forma.get()
        fpago = self._get_date_value(self.fac_fecha_pago)
        if not self._confirm(f"¿Registrar pago con {forma} al {fpago}?"): return
        try:
            FacturaController.pagar(fid, forma, fpago)
            self._show_success("Pago registrado correctamente.")
            self._fac_load_all()
        except Exception as e:
            self._show_error(str(e))

    def _fac_clear(self):
        for w in [self.fac_id, self.fac_num, self.fac_periodo,
                  self.fac_fijos, self.fac_var, self.fac_desc,
                  self.fac_imp, self.fac_total]:
            self._clear_entry(w)
        for w in [self.fac_emision, self.fac_venc, self.fac_fecha_pago]:
            self._clear_entry(w)
        self.fac_cli_combo.set("")
        self.fac_ctr_combo.set("")
        self.fac_est_pago.set("Pendiente")
        self.fac_forma.set("")

    def _fac_export_excel(self):
        from views.export_view import ExportView
        rows = FacturaController.get_all()
        cols = ["FacturaID","NumeroFactura","PeriodoFacturado","FechaEmision",
                "ClienteNombre","TotalPagar","EstadoPago","FormaPago"]
        ExportView.to_excel(rows, cols, "facturas")

    def _fac_export_pdf(self):
        from views.export_view import ExportView
        rows = FacturaController.get_all()
        cols = ["FacturaID","NumeroFactura","PeriodoFacturado","FechaEmision",
                "ClienteNombre","TotalPagar","EstadoPago","FormaPago"]
        ExportView.to_pdf(rows, cols, "Reporte de Facturación")

    # ══════════════════════════════════════════════════════════════════════════
    #  TEMA
    # ══════════════════════════════════════════════════════════════════════════
    def _apply_theme(self):
        self.T = THEMES[self.theme_name.get()]
        T = self.T
        self.configure(bg=T["bg"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook",
                         background=T["bg"], borderwidth=0)
        style.configure("TNotebook.Tab",
                         font=("Segoe UI", 10, "bold"),
                         padding=[12, 6],
                         background=T["tab_bg"],
                         foreground=T["text"])
        style.map("TNotebook.Tab",
                  background=[("selected", T["tab_sel"])],
                  foreground=[("selected", "#FFFFFF")])
        style.configure("TFrame", background=T["bg"])
        style.configure("TPanedwindow", background=T["bg"])
        style.configure("Custom.Treeview",
                         background=T["tree_row1"],
                         fieldbackground=T["tree_row1"],
                         foreground=T["text"])
        style.configure("Custom.Treeview.Heading",
                         background=T["tree_head"],
                         foreground=T["accent"])
        style.map("Custom.Treeview",
                  background=[("selected", T["accent"])],
                  foreground=[("selected", "#FFFFFF")])

        # Reconstruir sidebar con nuevo tema
        self._build_sidebar()

        # Reconstruir tabs
        for tab in [self.tab_clientes, self.tab_planes,
                    self.tab_contratos, self.tab_facturas]:
            for w in tab.winfo_children():
                w.destroy()
        self._build_tab_clientes()
        self._build_tab_planes()
        self._build_tab_contratos()
        self._build_tab_facturas()
