import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import datetime
import os
import pyautogui 
import time
import platform

class AppGeradorNumeros:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        # Configurações Iniciais e Auditoria
        self.is_fullscreen = False
        self.numero_gerado = False
        self.idioma = "PT"
        self.segundos = 30
        self.digitos = 6
        self.tempo_restante = 0
        self.inicio_sessao = time.time()
        self.inicio_programa = datetime.datetime.now()
        self.modo_escuro = True
        self.piscando = True 
        self.visivel = True
        self.timer_hide = None
        
        self.cores = {
            "escuro": {
                "bg": "#1e1e1e", "text": "#4d4d4d", "border": "#313131", 
                "num": "#00ff9c", "trough": "#2a2a2a", "title_bg": "#252525", "err": "#4e1d1d"
            },
            "claro": {
                "bg": "#ffffff", "text": "#b3b3b3", "border": "#e1e1e1", 
                "num": "#232923", "trough": "#f0f0f0", "title_bg": "#f8f8f8", "err": "#ffe6e6"
            }
        }
        
        self.t = {
            "PT": {
                "title": "Gerador de Números ESP",
                "timer_q": "Segundos para o temporizador (1 a 36000)?",
                "btn_conf": "Confirmar",
                "digitos_q": "Quantidade de algarismos (1 a 9)?",
                "gen_in": "O número será gerado em {} segundos",
                "gen_done": "Número gerado!",
                "prog_start": "Programa iniciado em: {}",
                "gen_time": "Número gerado em: {}",
                "history": "Histórico / Auditoria",
                "invert": "Inverter Cores (i)",
                "fullscreen": "Ecrã Completo (Esc)"
            },
            "EN": {
                "title": "ESP Number Generator",
                "timer_q": "Seconds for timer (1-3600)?",
                "btn_conf": "Confirm",
                "digitos_q": "Number of digits (1-9)?",
                "gen_in": "Generating in {} seconds",
                "gen_done": "Generated!",
                "prog_start": "Started: {}",
                "gen_time": "Generated: {}",
                "history": "History / Audit Log",
                "invert": "Invert Colors (i)",
                "fullscreen": "Full Screen (Esc)"
            }
        }
        
        self.sw = self.root.winfo_screenwidth()
        self.sh = self.root.winfo_screenheight()
        self.base_w = int(self.sw * 0.6)
        self.base_h = int(self.sh * 0.6)
        
        # Atalhos de Teclado
        self.root.bind("<Escape>", self.sair_fullscreen_esc)
        self.root.bind("<Key-i>", lambda e: self.inverter_cores())
        self.root.bind("<Key-I>", lambda e: self.inverter_cores())
        
        self.root.after(100, self.mostrar_janela_idioma)
        self.impedir_descanso_ecra()

    def validar_estilo_entrada(self, var, entry, min_val, max_val):
        try:
            val = int(var.get())
            if min_val <= val <= max_val:
                entry.config(bg="#2a2a2a", highlightbackground="#00ff9c")
            else:
                entry.config(bg=self.cores["escuro"]["err"], highlightbackground="red")
        except:
            entry.config(bg=self.cores["escuro"]["err"], highlightbackground="red")

    def guardar_historico_audit(self, num, seed, duracao):
        try:
            path = os.path.join(os.path.expanduser("~"), "Desktop", "esp_audit_logs.txt")
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = (
                f"--- ESP SESSION / SESSÂO ESP ---\n"
                f"Timestamp / Data e Hora: {timestamp}\n"
                f"Result / Resultado: {num}\n"
                f"Seed Used / Seed Utilizada: {seed}\n"
                f"Prep Time / Tempo de Preparação: {duracao}s\n"
                f"Config: {self.digitos} digits/algarismos / {self.segundos} seconds/segundos\n"
                f"OS / Sistema: {platform.system()}\n"
                f"------------------\n\n"
            )
            with open(path, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except: pass

    def sair_fullscreen_esc(self, event=None):
        self.toggle_fullscreen()

    def impedir_descanso_ecra(self):
        try:
            pyautogui.moveRel(1, 0, duration=0)
            pyautogui.moveRel(-1, 0, duration=0)
        except: pass
        self.root.after(45000, self.impedir_descanso_ecra)

    def centrar_janela_fix(self, janela, largura, altura, sem_barra=True):
        janela.withdraw() 
        if sem_barra:
            janela.overrideredirect(True)
        janela.update_idletasks()
        x = (self.sw // 2) - (largura // 2)
        y = (self.sh // 2) - (altura // 2)
        janela.geometry(f"{largura}x{altura}+{x}+{y}")
        janela.config(highlightbackground="#4d4d4d", highlightthickness=1)
        janela.deiconify() 
        janela.attributes('-topmost', True)
        janela.focus_force()

    def criar_barra_titulo(self, master, text, fechar_alvo=None):
        if self.is_fullscreen and master == self.root: return None, None
        tema = "escuro" if self.modo_escuro else "claro"
        c = self.cores[tema]
        frame_t = tk.Frame(master, bg=c["title_bg"], bd=0)
        frame_t.pack(fill="x", side="top")
        lbl_t = tk.Label(frame_t, text=text, font=("Segoe UI", 10, "bold"), bg=c["title_bg"], fg="#888888")
        lbl_t.pack(pady=5, padx=10, side="left")
        if fechar_alvo:
            btn_s = tk.Label(frame_t, text="✕", font=("Segoe UI", 12), bg=c["title_bg"], fg="#888888", cursor="hand2")
            btn_s.pack(pady=5, padx=10, side="right")
            btn_s.bind("<Button-1>", lambda e: fechar_alvo.destroy())

        def iniciar_mov(event):
            master._drag_x = event.x
            master._drag_y = event.y
        def mover_janela(event):
            deltax = event.x - master._drag_x
            deltay = event.y - master._drag_y
            master.geometry(f"+{master.winfo_x() + deltax}+{master.winfo_y() + deltay}")
            
        frame_t.bind("<Button-1>", iniciar_mov)
        frame_t.bind("<B1-Motion>", mover_janela)
        sep = tk.Frame(master, height=1, bg=c["border"])
        sep.pack(fill="x")
        return frame_t, sep

    def mostrar_janela_idioma(self):
        self.win_idioma = tk.Toplevel(self.root)
        self.win_idioma.configure(bg="#1e1e1e")
        self.criar_barra_titulo_simples(self.win_idioma, "Idioma / Language")
        tk.Label(self.win_idioma, text="Idioma/Language", font=("Segoe UI", 14), bg="#1e1e1e", fg="white").pack(pady=(20, 30))
        btn_frame = tk.Frame(self.win_idioma, bg="#1e1e1e")
        btn_frame.pack()
        tk.Button(btn_frame, text="Português", font=("Segoe UI", 12), width=15, command=lambda: self.proximo_step(self.win_idioma, "PT")).pack(side="left", padx=10)
        tk.Button(btn_frame, text="English", font=("Segoe UI", 12), width=15, command=lambda: self.proximo_step(self.win_idioma, "EN")).pack(side="left", padx=10)
        self.centrar_janela_fix(self.win_idioma, 450, 230)

    def criar_barra_titulo_simples(self, win, txt):
        f = tk.Frame(win, bg="#252525")
        f.pack(fill="x")
        tk.Label(f, text=txt, bg="#252525", fg="gray").pack(pady=5)

    def proximo_step(self, janela, lang):
        self.idioma = lang
        janela.destroy()
        self.mostrar_janela_timer()

    def mostrar_janela_timer(self):
        win = tk.Toplevel(self.root)
        win.configure(bg="#1e1e1e")
        self.criar_barra_titulo_simples(win, self.t[self.idioma]["title"])
        tk.Label(win, text=self.t[self.idioma]["timer_q"], font=("Segoe UI", 14), bg="#1e1e1e", fg="white").pack(pady=(25, 20))
        timer_var = tk.StringVar(value="30")
        self.entry_timer = tk.Entry(win, textvariable=timer_var, font=("Segoe UI", 14), justify="center", width=10, bg="#2a2a2a", fg="white", insertbackground="white", relief="flat", highlightthickness=2)
        self.entry_timer.pack()
        timer_var.trace_add("write", lambda *args: self.validar_estilo_entrada(timer_var, self.entry_timer, 1, 36000))
        tk.Button(win, text=self.t[self.idioma]["btn_conf"], font=("Segoe UI", 12), command=lambda: self.validar_timer(win)).pack(pady=25)
        self.centrar_janela_fix(win, 450, 250)

    def validar_timer(self, win):
        try:
            val = int(self.entry_timer.get())
            if 1 <= val <= 36000:
                self.segundos = val
                self.tempo_restante = val
                win.destroy()
                self.mostrar_janela_digitos()
        except: pass

    def mostrar_janela_digitos(self):
        win = tk.Toplevel(self.root)
        win.configure(bg="#1e1e1e")
        self.criar_barra_titulo_simples(win, self.t[self.idioma]["title"])
        tk.Label(win, text=self.t[self.idioma]["digitos_q"], font=("Segoe UI", 14), bg="#1e1e1e", fg="white").pack(pady=(25, 20))
        digitos_var = tk.StringVar(value="6")
        self.entry_digitos = tk.Entry(win, textvariable=digitos_var, font=("Segoe UI", 14), justify="center", width=10, bg="#2a2a2a", fg="white", insertbackground="white", relief="flat", highlightthickness=2)
        self.entry_digitos.pack()
        digitos_var.trace_add("write", lambda *args: self.validar_estilo_entrada(digitos_var, self.entry_digitos, 1, 9))
        tk.Button(win, text=self.t[self.idioma]["btn_conf"], font=("Segoe UI", 12), command=lambda: self.validar_digitos(win)).pack(pady=25)
        self.centrar_janela_fix(win, 450, 250)

    def validar_digitos(self, win):
        try:
            val = int(self.entry_digitos.get())
            if 1 <= val <= 9:
                self.digitos = val
                win.destroy()
                self.construir_janela_principal()
        except: pass

    def construir_janela_principal(self):
        self.root.deiconify()
        self.root.overrideredirect(True)
        self.centrar_janela_fix(self.root, self.base_w, self.base_h, sem_barra=True)
        tema = "escuro" if self.modo_escuro else "claro"
        c = self.cores[tema]
        self.root.configure(bg=c["bg"])
        self.root.focus_force()
        self.frame_titulo_custom, self.sep_titulo = self.criar_barra_titulo(self.root, self.t[self.idioma]["title"], fechar_alvo=self.root)
        self.root.bind("<Motion>", self.detectar_rato)
        self.root.bind("<Configure>", self.atualizar_elementos_dinamicos)
        self.main_frame = tk.Frame(self.root, bg=c["bg"])
        self.main_frame.pack(expand=True, fill="both")
        self.ui_superior = tk.Frame(self.main_frame, bg=c["bg"])
        self.ui_superior.pack(fill="x")
        self.lbl_timer_text = tk.Label(self.ui_superior, text="", font=("Segoe UI", 18), bg=c["bg"], fg=c["text"])
        self.lbl_timer_text.pack(pady=(0, 15))
        self.estilo = ttk.Style()
        self.estilo.theme_use('clam')
        self.estilo.configure("Custom.Horizontal.TProgressbar", background=c["text"], troughcolor=c["trough"], bordercolor=c["bg"], thickness=8)
        self.progress = ttk.Progressbar(self.ui_superior, style="Custom.Horizontal.TProgressbar", orient="horizontal", mode="determinate")
        self.progress["maximum"] = self.segundos
        self.progress.pack(fill="x")
        placeholder = " ".join(["__"] * self.digitos)
        self.lbl_numero = tk.Label(self.main_frame, text=placeholder, font=("Segoe UI", 80, "bold"), bg=c["bg"], fg=c["num"])
        self.lbl_numero.pack(expand=True, fill="both")
        self.ui_inferior = tk.Frame(self.main_frame, bg=c["bg"])
        self.ui_inferior.pack(fill="x", side="bottom")
        self.lbl_inicio = tk.Label(self.ui_inferior, text=self.t[self.idioma]["prog_start"].format(self.inicio_programa.strftime("%H:%M:%S")), font=("Segoe UI", 11), bg=c["bg"], fg=c["text"])
        self.lbl_inicio.pack()
        self.lbl_sorteio = tk.Label(self.ui_inferior, text="", font=("Segoe UI", 11), bg=c["bg"], fg=c["text"])
        self.lbl_sorteio.pack(pady=(0, 20))
        self.frame_botoes = tk.Frame(self.ui_inferior, bg=c["bg"])
        self.frame_botoes.pack()
        btn_opts = {"font": ("Segoe UI", 11), "bg": c["bg"], "fg": c["text"], "activebackground": c["text"], "activeforeground": c["bg"], "relief": "groove", "bd": 2}
        self.btn_hist = tk.Button(self.frame_botoes, text=self.t[self.idioma]["history"], width=18, command=self.mostrar_historico, **btn_opts)
        self.btn_hist.pack(side="left", padx=10)
        self.btn_cores = tk.Button(self.frame_botoes, text=self.t[self.idioma]["invert"], width=14, command=self.inverter_cores, **btn_opts)
        self.btn_cores.pack(side="left", padx=10)
        self.btn_full = tk.Button(self.frame_botoes, text=self.t[self.idioma]["fullscreen"], width=18, command=self.toggle_fullscreen, **btn_opts)
        self.btn_full.pack(side="left", padx=10)
        self.efeito_blink() 
        self.atualizar_timer()
        self.atualizar_elementos_dinamicos()

    def atualizar_elementos_dinamicos(self, event=None):
        if event and event.widget != self.root: return
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        pad_x, pad_y = int(w * 0.10), int(h * 0.10)
        self.main_frame.pack_configure(padx=pad_x, pady=pad_y)
        disp_w = w - (pad_x * 2)
        ui_offset = 220 if self.ui_superior.winfo_ismapped() else 60
        disp_h = h - (pad_y * 2) - ui_offset
        largura_proporcao = 1.6 if not self.numero_gerado else 0.85
        t_largura = int(disp_w / (self.digitos * largura_proporcao))
        t_altura = int(disp_h * 0.8)
        novo_tamanho = min(t_largura, t_altura)
        novo_tamanho = max(30, min(novo_tamanho, 450)) 
        self.lbl_numero.config(font=("Segoe UI", novo_tamanho, "bold"))

    def detectar_rato(self, event):
        if not self.is_fullscreen or not self.numero_gerado: return
        if not self.ui_superior.winfo_ismapped(): self.mostrar_ui()
        if self.timer_hide: self.root.after_cancel(self.timer_hide)
        self.timer_hide = self.root.after(3000, self.ocultar_ui)

    def mostrar_ui(self):
        if not self.is_fullscreen and self.frame_titulo_custom:
            self.frame_titulo_custom.pack(fill="x", side="top", before=self.main_frame)
            self.sep_titulo.pack(fill="x", after=self.frame_titulo_custom)
        self.ui_superior.pack(fill="x", before=self.lbl_numero)
        self.ui_inferior.pack(fill="x", side="bottom")
        self.root.config(cursor="")
        self.root.after(20, self.atualizar_elementos_dinamicos)

    def ocultar_ui(self):
        if self.is_fullscreen and self.numero_gerado:
            if self.frame_titulo_custom:
                self.frame_titulo_custom.pack_forget()
                self.sep_titulo.pack_forget()
            self.ui_superior.pack_forget()
            self.ui_inferior.pack_forget()
            self.root.config(cursor="none")
            self.root.after(20, self.atualizar_elementos_dinamicos)

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.frame_titulo_custom:
            self.frame_titulo_custom.destroy()
            self.sep_titulo.destroy()
            self.frame_titulo_custom = self.sep_titulo = None
        if self.is_fullscreen:
            self.root.geometry(f"{self.sw}x{self.sh}+0+0")
            if self.numero_gerado: self.ocultar_ui()
        else:
            self.frame_titulo_custom, self.sep_titulo = self.criar_barra_titulo(self.root, self.t[self.idioma]["title"], fechar_alvo=self.root)
            self.mostrar_ui()
            self.centrar_janela_fix(self.root, self.base_w, self.base_h)
        self.root.after(50, self.atualizar_elementos_dinamicos)

    def efeito_blink(self):
        if self.piscando:
            tema = "escuro" if self.modo_escuro else "claro"
            nova_cor = self.cores[tema]["num"] if self.visivel else self.cores[tema]["bg"]
            self.lbl_numero.configure(fg=nova_cor)
            self.visivel = not self.visivel
            self.root.after(1200, self.efeito_blink)

    def atualizar_timer(self):
        if self.tempo_restante > 0:
            self.lbl_timer_text.config(text=self.t[self.idioma]["gen_in"].format(self.tempo_restante))
            self.progress["value"] = self.segundos - self.tempo_restante
            self.tempo_restante -= 1
            self.root.after(1000, self.atualizar_timer)
        else:
            self.piscando = False 
            self.progress["value"] = self.segundos
            self.gerar_numero()

    def gerar_numero(self):
        self.numero_gerado = True
        seed_audit = time.time_ns()
        random.seed(seed_audit)
        duracao_sessao = round(time.time() - self.inicio_sessao, 2)
        limite_inf = 0 if self.digitos == 1 else 10 ** (self.digitos - 1)
        limite_sup = (10 ** self.digitos) - 1
        num = random.randint(limite_inf, limite_sup)
        tema = "escuro" if self.modo_escuro else "claro"
        self.lbl_numero.config(text=str(num), fg=self.cores[tema]["num"])
        self.lbl_timer_text.config(text=self.t[self.idioma]["gen_done"])
        self.lbl_sorteio.config(text=self.t[self.idioma]["gen_time"].format(datetime.datetime.now().strftime("%H:%M:%S")))
        self.guardar_historico_audit(num, seed_audit, duracao_sessao)
        self.atualizar_elementos_dinamicos()
        if self.is_fullscreen: self.root.after(3000, self.ocultar_ui)

    def mostrar_historico(self):
        tema = "escuro" if self.modo_escuro else "claro"
        c = self.cores[tema]
        win = tk.Toplevel(self.root)
        win.configure(bg=c["bg"])
        # Aplica a barra de título customizada e remove a nativa
        self.centrar_janela_fix(win, 600, 500, sem_barra=True)
        self.criar_barra_titulo(win, self.t[self.idioma]["history"], fechar_alvo=win)
        
        txt = scrolledtext.ScrolledText(win, font=("Consolas", 10), bg=c["bg"], fg=c["text"], relief="flat", insertbackground=c["text"])
        txt.pack(padx=20, pady=20, expand=True, fill="both")
        path = os.path.join(os.path.expanduser("~"), "Desktop", "esp_audit_logs.txt")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f: txt.insert(tk.INSERT, f.read())
        txt.configure(state='disabled')

    def inverter_cores(self):
        self.modo_escuro = not self.modo_escuro
        tema = "escuro" if self.modo_escuro else "claro"; c = self.cores[tema]
        self.root.configure(bg=c["bg"]); self.main_frame.configure(bg=c["bg"])
        if self.frame_titulo_custom: self.frame_titulo_custom.destroy(); self.sep_titulo.destroy()
        if not self.is_fullscreen:
            self.frame_titulo_custom, self.sep_titulo = self.criar_barra_titulo(self.root, self.t[self.idioma]["title"], fechar_alvo=self.root)
            self.frame_titulo_custom.pack(fill="x", side="top", before=self.main_frame)
            self.sep_titulo.pack(fill="x", side="top", after=self.frame_titulo_custom)
        else: self.frame_titulo_custom = self.sep_titulo = None
        self.ui_superior.configure(bg=c["bg"]); self.ui_inferior.configure(bg=c["bg"]); self.frame_botoes.configure(bg=c["bg"])
        self.lbl_timer_text.configure(bg=c["bg"], fg=c["text"]); self.lbl_numero.configure(bg=c["bg"])
        if not self.piscando: self.lbl_numero.configure(fg=c["num"])
        self.lbl_inicio.configure(bg=c["bg"], fg=c["text"]); self.lbl_sorteio.configure(bg=c["bg"], fg=c["text"])
        self.estilo.configure("Custom.Horizontal.TProgressbar", background=c["text"], troughcolor=c["trough"], bordercolor=c["bg"])
        for b in [self.btn_hist, self.btn_cores, self.btn_full]: b.configure(bg=c["bg"], fg=c["text"], activeforeground=c["bg"], activebackground=c["text"])

if __name__ == "__main__":
    root = tk.Tk(); app = AppGeradorNumeros(root); root.mainloop()