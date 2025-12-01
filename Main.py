#!/usr/bin/env python3
# alert_formatter.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import datetime
import re
from typing import Tuple, List

def suggest_team(description: str, link: str) -> Tuple[str, List[str]]:
    desc = (description or "").lower()
    link_low = (link or "").lower()
    matches = []

    if "platcom" in desc:
        matches.append("Banco de Dados ou Produção (contém 'Platcom') - Verificar manualmente")

    if "cgmp25" in desc:
        matches.append("Banco de Dados (contém 'CGMP25')")

    if "cgmp6" in desc and "platcom" not in desc:
        matches.append("Produção (contém 'CGMP6' e não contém 'Platcom')")

    if "query" in desc and "webhook" in link_low:
        matches.append("Gestão de Crises (tem 'Query' + link com webhook)")

    if "webhook" in link_low:
        matches.append("Gestão de Crises (tem link com webhook)")

    if "osb" in desc:
        matches.append("V8 Whatsapp (contém 'OSB')")

    if "weblogic" in desc:
        matches.append("V8 Whatsapp (contém 'WebLogic')")

    if "gto" in desc:
        matches.append("V8 Whatsapp (contém 'GTO')")

    if "GoldenGate" in desc:
        matches.append('Time de BI (tem "GoldenGate")')

    if "VINDT" in desc:
        matches.append("Time de Telecom (tem 'VINDT')")

    if "Protheus" in desc:
        matches.append("Time de produção (tem 'Protheus')")

    if re.search(r"\.prd\b", desc) or re.search(r"\.prd\b", link_low):
        matches.append("Produção (contém '.prd')")

    if not matches:
        return ("Sem sugestão automática — verificar manualmente", [])

    return (matches[0].split(" (")[0], matches)


STEP_LABELS = [
    "Colar o NÚMERO do alerta",
    "Colar a DESCRIÇÃO (uma única linha)",
    "Colar o LINK do Dynatrace (opcional; use PULAR se não houver)"
]


class AlertFormatterApp:
    def __init__(self, root):
        self.root = root
        root.title("Montador de Alertas")
        root.geometry("420x220")
        root.resizable(False, False)

        self.values = ["", "", ""]
        self.step = 0

        self.header = ttk.Label(root, text=STEP_LABELS[self.step], font=("Segoe UI", 12))
        self.header.pack(padx=12, pady=(12, 4), anchor="w")

        self.field_frame = ttk.Frame(root)
        self.field_frame.pack(fill="both", expand=False, padx=12)

        self.single_entry = None

        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", side="bottom", padx=12, pady=12)

        self.skip_btn = ttk.Button(btn_frame, text="Pular", command=self.skip_step)
        self.skip_btn.pack(side="left")

        self.prev_btn = ttk.Button(btn_frame, text="Voltar", command=self.prev_step, state="disabled")
        self.prev_btn.pack(side="left", padx=(8, 0))

        self.next_btn = ttk.Button(btn_frame, text="Próximo", command=self.next_step)
        self.next_btn.pack(side="right")

        self.status_label = ttk.Label(root, text="Passo 1 de 3", font=("Segoe UI", 9))
        self.status_label.pack(side="bottom", anchor="w", padx=12, pady=(0, 8))

        self.update_ui()

    def clear_field_frame(self):
        for child in self.field_frame.winfo_children():
            child.destroy()
        self.single_entry = None

    def update_ui(self):
        self.clear_field_frame()
        self.header.config(text=STEP_LABELS[self.step])
        self.status_label.config(text=f"Passo {self.step + 1} de {len(STEP_LABELS)}")
        self.prev_btn.config(state="normal" if self.step > 0 else "disabled")
        self.next_btn.config(text="Concluir" if self.step == len(STEP_LABELS) - 1 else "Próximo")

        self.single_entry = ttk.Entry(self.field_frame, width=50, font=("Segoe UI", 10))
        if self.values[self.step]:
            self.single_entry.insert(0, self.values[self.step])
        self.single_entry.pack(pady=(6, 0))
        self.single_entry.focus_set()
        self.single_entry.bind("<Return>", lambda e: self.next_step())

    def get_current_input(self):
        return self.single_entry.get().strip()

    def next_step(self):
        value = self.get_current_input()

        if self.step in (0, 1) and not value:
            messagebox.showwarning("Campo vazio", "Preencha o campo antes de prosseguir.")
            return

        self.values[self.step] = value

        if self.step < len(STEP_LABELS) - 1:
            self.step += 1
            self.update_ui()
        else:
            self.show_result()

    def skip_step(self):
        self.values[self.step] = ""

        if self.step < len(STEP_LABELS) - 1:
            self.step += 1
            self.update_ui()
        else:
            self.show_result()

    def prev_step(self):
        self.values[self.step] = self.get_current_input()
        if self.step > 0:
            self.step -= 1
            self.update_ui()

    def format_message(self):
        lines = [l for l in self.values if l.strip()]
        return "\n".join(lines)

    def show_result(self):
        formatted = self.format_message()
        suggested_team, reasons = suggest_team(self.values[1], self.values[2])

        res = tk.Toplevel(self.root)
        res.title("Alerta formatado")

        ### ALTERAÇÃO — janela menor
        res.geometry("380x260")
        res.resizable(False, False)

        ### ALTERAÇÃO — manter janela on top
        res.attributes("-topmost", True)

        ttk.Label(res, text="Mensagem pronta:", font=("Segoe UI", 11)).pack(anchor="w", padx=12, pady=(12, 4))

        txt = scrolledtext.ScrolledText(res, width=46, height=5, wrap="word", font=("Segoe UI", 10))
        txt.insert("1.0", formatted)
        txt.config(state="disabled")
        txt.pack(padx=12, pady=(0, 8))

        ttk.Label(res, text=f"Sugestão de time: {suggested_team}", foreground="blue",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=12)

        if reasons:
            ttk.Label(res, text="Regras ativadas:", font=("Segoe UI", 9)).pack(anchor="w", padx=12, pady=(4, 0))
            for rule in reasons:
                ttk.Label(res, text=f"- {rule}", font=("Segoe UI", 8)).pack(anchor="w", padx=20)

        btn_frame = ttk.Frame(res)
        btn_frame.pack(fill="x", padx=12, pady=8)

        def copy_clipboard():
            self.root.clipboard_clear()
            self.root.clipboard_append(formatted)

            ### ALTERAÇÃO — mensagem "copiado" sem pop-up
            temp_label = ttk.Label(res, text="Copiado com sucesso!", foreground="green")
            temp_label.pack(anchor="w", padx=12, pady=(4, 0))
            res.after(1500, temp_label.destroy)

        def save_file():
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            fname = f"alerta_{ts}.txt"
            with open(fname, "w", encoding="utf-8") as f:
                f.write(formatted)
            messagebox.showinfo("Salvo", f"Arquivo salvo como {fname}")

        def new_alert():
            res.destroy()
            self.values = ["", "", ""]
            self.step = 0
            self.update_ui()

        ttk.Button(btn_frame, text="Copiar", command=copy_clipboard).pack(side="left")
        ttk.Button(btn_frame, text="Salvar", command=save_file).pack(side="left", padx=(8, 0))
        ttk.Button(btn_frame, text="Novo alerta", command=new_alert).pack(side="right")
        ttk.Button(btn_frame, text="Fechar", command=res.destroy).pack(side="right", padx=(0, 8))

        ### ALTERAÇÃO — copiar automaticamente ao exibir janela
        self.root.clipboard_clear()
        self.root.clipboard_append(formatted)


def main():
    root = tk.Tk()
    app = AlertFormatterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
