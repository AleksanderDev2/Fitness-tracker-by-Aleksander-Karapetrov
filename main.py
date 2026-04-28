import tkinter as tk
from tkinter import ttk, messagebox
from models import FitnessTracker

# ══════════════════════════════════════════════
#  ЦВЕТОВА СХЕМА
# ══════════════════════════════════════════════
BG        = "#1a1a2e"
PANEL     = "#16213e"
CARD      = "#0f3460"
ACCENT    = "#e94560"
ACCENT2   = "#f5a623"
TEXT      = "#eaeaea"
SUBTEXT   = "#a0a0c0"
BTN_HV    = "#c73652"

FONT_H1   = ("Segoe UI", 18, "bold")
FONT_H2   = ("Segoe UI", 13, "bold")
FONT_BODY = ("Segoe UI", 10)
FONT_SM   = ("Segoe UI", 9)


class FlatButton(tk.Button):
    def __init__(self, master, **kw):
        kw.setdefault("relief", "flat")
        kw.setdefault("bg", ACCENT)
        kw.setdefault("fg", TEXT)
        kw.setdefault("font", ("Segoe UI", 10, "bold"))
        kw.setdefault("cursor", "hand2")
        kw.setdefault("padx", 14)
        kw.setdefault("pady", 7)
        kw.setdefault("activebackground", BTN_HV)
        kw.setdefault("activeforeground", TEXT)
        kw.setdefault("bd", 0)
        _bg = kw["bg"]
        super().__init__(master, **kw)
        self.bind("<Enter>", lambda e: self.config(bg=BTN_HV))
        self.bind("<Leave>", lambda e: self.config(bg=_bg))


class FitnessApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Фитнес Тракер")
        self.geometry("1000x680")
        self.minsize(900, 620)
        self.configure(bg=BG)
        self.state("zoomed")
        self.tracker = FitnessTracker("Потребител")
        self._build_ui()
        self._load_demo_data()

    def _build_ui(self):
        # Хедър
        header = tk.Frame(self, bg=CARD, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="  ФИТНЕС ТРАКЕР",
                 font=FONT_H1, bg=CARD, fg=ACCENT).pack(side="left", padx=20, pady=12)
        self.lbl_summary = tk.Label(header, text="", font=FONT_SM, bg=CARD, fg=SUBTEXT)
        self.lbl_summary.pack(side="right", padx=20)

        # Основна зона
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=14, pady=12)

        left = tk.Frame(main, bg=PANEL, width=310)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        self._build_form(left)

        right = tk.Frame(main, bg=BG)
        right.pack(side="left", fill="both", expand=True)
        self._build_table(right)
        self._build_stats(right)

    def _build_form(self, parent):
        tk.Label(parent, text="  ДОБАВИ ТРЕНИРОВКА",
                 font=FONT_H2, bg=PANEL, fg=ACCENT).pack(pady=(18, 10), padx=16, anchor="w")

        fields = [("Упражнение", "упр"), ("Серии", "серии"),
                  ("Повторения", "повт"), ("Калории", "кал")]
        self.vars = {}
        for label, key in fields:
            tk.Label(parent, text=label, font=FONT_SM,
                     bg=PANEL, fg=SUBTEXT).pack(anchor="w", padx=16, pady=(8, 0))
            var = tk.StringVar()
            tk.Entry(parent, textvariable=var, font=FONT_BODY,
                     bg=CARD, fg=TEXT, insertbackground=TEXT,
                     relief="flat", highlightthickness=1,
                     highlightcolor=ACCENT, highlightbackground=PANEL
                     ).pack(fill="x", padx=16, ipady=6)
            self.vars[key] = var

        tk.Label(parent, text="Мускулна група", font=FONT_SM,
                 bg=PANEL, fg=SUBTEXT).pack(anchor="w", padx=16, pady=(8, 0))
        self.var_група = tk.StringVar(value="Гърди")
        групи = ["Гърди", "Гръб", "Крака", "Рамене", "Ръце", "Корем", "Кардио"]

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=CARD, background=CARD,
                        foreground=TEXT, selectbackground=ACCENT, arrowcolor=TEXT)

        ttk.Combobox(parent, textvariable=self.var_група, values=групи,
                     state="readonly", font=FONT_BODY
                     ).pack(fill="x", padx=16, ipady=4)

        FlatButton(parent, text="  ДОБАВИ", command=self._добави
                   ).pack(fill="x", padx=16, pady=(16, 8), ipady=4)

        tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x", padx=16, pady=8)

        tk.Label(parent, text="  ФИЛТРИРАЙ ПО ГРУПА",
                 font=("Segoe UI", 10, "bold"), bg=PANEL, fg=ACCENT2
                 ).pack(anchor="w", padx=16, pady=(6, 0))
        self.var_филтър = tk.StringVar(value="Всички")
        ttk.Combobox(parent, textvariable=self.var_филтър,
                     values=["Всички"] + групи, state="readonly", font=FONT_BODY
                     ).pack(fill="x", padx=16, ipady=4, pady=(4, 0))

        FlatButton(parent, text="  ФИЛТРИРАЙ", bg="#1565c0",
                   command=self._филтрирай
                   ).pack(fill="x", padx=16, pady=(8, 4), ipady=4)
        FlatButton(parent, text="  СОРТИРАЙ ПО КАЛОРИИ", bg="#2e7d32",
                   command=self._сортирай
                   ).pack(fill="x", padx=16, pady=(4, 4), ipady=4)
        FlatButton(parent, text="  ИЗЧИСТИ ВСИЧКО", bg="#555",
                   command=self._изчисти
                   ).pack(fill="x", padx=16, pady=(4, 16), ipady=4)

    def _build_table(self, parent):
        tk.Label(parent, text="  ТРЕНИРОВКИ",
                 font=FONT_H2, bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 6))
        frame = tk.Frame(parent, bg=BG)
        frame.pack(fill="both", expand=True)

        cols = ("Дата", "Упражнение", "Серии", "Повт.", "Калории", "Група")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings",
                                 height=14, selectmode="browse")
        for col, w in zip(cols, [90, 220, 60, 60, 80, 100]):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=w, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", background=PANEL, foreground=TEXT,
                        fieldbackground=PANEL, rowheight=28, font=FONT_BODY)
        style.configure("Treeview.Heading", background=CARD, foreground=ACCENT,
                        font=("Segoe UI", 10, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT)])

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="left", fill="y")
        self.tree.tag_configure("odd",  background=PANEL)
        self.tree.tag_configure("even", background="#1c2a50")

    def _build_stats(self, parent):
        bar = tk.Frame(parent, bg=CARD, height=52)
        bar.pack(fill="x", pady=(10, 0))
        bar.pack_propagate(False)
        self.stat_labels = {}
        for key, text in [("stat_total", "Общо тренировки: 0"),
                           ("stat_cal",  "Калории: 0"),
                           ("stat_max",  "Топ упражнение: —"),
                           ("stat_group","Топ група: —")]:
            lbl = tk.Label(bar, text=text, font=FONT_SM, bg=CARD, fg=TEXT)
            lbl.pack(side="left", padx=20, pady=10)
            self.stat_labels[key] = lbl

    # ── Логика ──────────────────────────────────
    def _добави(self):
        упр = self.vars["упр"].get().strip()
        if not упр:
            messagebox.showwarning("Грешка", "Въведи названието на упражнението!")
            return
        try:
            серии = int(self.vars["серии"].get())
            повт  = int(self.vars["повт"].get())
            кал   = float(self.vars["кал"].get())
        except ValueError:
            messagebox.showwarning("Грешка", "Серии, повторения и калории трябва да са числа!")
            return
        if серии <= 0 or повт <= 0 or кал <= 0:
            messagebox.showwarning("Грешка", "Стойностите трябва да са положителни!")
            return
        self.tracker.добави_тренировка(упр, серии, повт, кал, self.var_група.get())
        for v in self.vars.values():
            v.set("")
        self._обнови_таблица(self.tracker.тренировки)
        self._обнови_статистики()

    def _обнови_таблица(self, тренировки):
        self.tree.delete(*self.tree.get_children())
        for i, т in enumerate(тренировки):
            self.tree.insert("", "end", tags=("odd" if i % 2 == 0 else "even",),
                             values=(т["дата"], т["упражнение"], т["серии"],
                                     т["повторения"], f"{т['калории']:.0f} кал",
                                     т["мускулна_група"]))

    def _обнови_статистики(self):
        тр = self.tracker.тренировки
        общо = self.tracker.общо_калории()
        най  = max(тр, key=lambda х: х["калории"]) if тр else None
        обобщ = self.tracker.обобщение_по_групи()
        топ_гр = max(обобщ, key=обобщ.get) if обобщ else "—"
        self.stat_labels["stat_total"].config(text=f"Тренировки: {len(тр)}")
        self.stat_labels["stat_cal"].config(text=f"Калории: {общо:.0f} кал", fg=ACCENT2)
        self.stat_labels["stat_max"].config(text=f"Топ: {най['упражнение'] if най else '—'}")
        self.stat_labels["stat_group"].config(text=f"Топ група: {топ_гр}")
        self.lbl_summary.config(
            text=f"{self.tracker.потребител}  |  {len(тр)} тренировки  |  {общо:.0f} кал")

    def _филтрирай(self):
        г = self.var_филтър.get()
        self._обнови_таблица(
            self.tracker.тренировки if г == "Всички"
            else self.tracker.филтрирай_по_група(г))

    def _сортирай(self):
        self._обнови_таблица(self.tracker.сортирай_по_калории())

    def _изчисти(self):
        if self.tracker.тренировки and messagebox.askyesno(
                "Потвърди", "Изтриване на всички тренировки?"):
            self.tracker.тренировки.clear()
            self._обнови_таблица([])
            self._обнови_статистики()

    def _load_demo_data(self):
        for упр, с, п, к, гр in [
            ("Лег преса",         4, 10, 180, "Гърди"),
            ("Клек",              5,  8, 220, "Крака"),
            ("Мъртва тяга",       4,  6, 260, "Гръб"),
            ("Бицепс кърл",       3, 12,  90, "Ръце"),
            ("Трицепс разгъване", 3, 12,  85, "Ръце"),
            ("Лег флай",          3, 15, 130, "Гърди"),
            ("Лат машина",        4, 10, 150, "Гръб"),
            ("Напади",            3, 12, 170, "Крака"),
            ("Рамо преса",        4, 10, 140, "Рамене"),
            ("Кардио — 20 мин",   1,  1, 200, "Кардио"),
        ]:
            self.tracker.добави_тренировка(упр, с, п, к, гр)
        self._обнови_таблица(self.tracker.тренировки)
        self._обнови_статистики()


if __name__ == "__main__":
    app = FitnessApp()
    app.mainloop()