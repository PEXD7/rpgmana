import tkinter as tk
import sqlite3

class Jogador:
    def __init__(self, nome, vida_maxima, mana_maxima, row):
        self.nome = nome
        self.vida_maxima = vida_maxima
        self.mana_maxima = mana_maxima
        self.vida_atual = self.vida_maxima
        self.mana_atual = self.mana_maxima
        self.pontos = 0

        # Carrega os valores do banco de dados
        self.carregar_valores()

        self.frame = tk.Frame(window, width=650, height=450, bd=0, relief=tk.RAISED, bg=('LightSlateGray'))
        self.frame.grid(row=row, column=0, padx=1, pady=10)

        self.nome_label = tk.Label(self.frame, text=f"Jogador: {self.nome}", bg=('LightSlateGray'))
        self.nome_label.grid(row=0, column=0, sticky="w")
        self.nome_label.config(width=20,bd=15)

        self.vida_label = tk.Label(self.frame, text=f"Vida: {self.vida_atual}/{self.vida_maxima}", bg=('SlateGray'))
        self.vida_label.grid(row=1, column=0, sticky="w")
        

        self.mana_label = tk.Label(self.frame, text=f"Mana: {self.mana_atual}/{self.mana_maxima}", bg=('SlateGray'))
        self.mana_label.grid(row=2, column=0, sticky="w")

        self.pontos_label = tk.Label(self.frame, text=f"Pontos: {self.pontos}")
        self.pontos_label.grid(row=3, column=0, sticky="w")

        self.add_vida_button = tk.Button(self.frame, text="+1",
                                         command=self.adicionar_vida, bg=('Lime'))
        self.add_vida_button.grid(row=1, column=1)
        

        self.sub_vida_button = tk.Button(self.frame, text="-1",
                                         command=self.subtrair_vida, bg=('RED'))
        self.sub_vida_button.grid(row=1, column=2)

        self.add_mana_button = tk.Button(self.frame, text="+1",
                                         command=self.adicionar_mana, bg=('Lime'))
        self.add_mana_button.grid(row=2, column=1)

        self.sub_mana_button = tk.Button(self.frame, text="-1",
                                         command=self.subtrair_mana, bg=('RED'))
        self.sub_mana_button.grid(row=2, column=2)

        self.add_pontos_button = tk.Button(self.frame, text="+1",
                                           command=self.adicionar_pontos, bg=('Lime'))
        self.add_pontos_button.grid(row=3, column=1)

        self.sub_pontos_button = tk.Button(self.frame, text="-1",
                                           command=self.subtrair_pontos, bg=('RED'))
        self.sub_pontos_button.grid(row=3, column=2)

        self.atualizar_status()

    def carregar_valores(self):
        conn = sqlite3.connect("pontuacoes.db")
        cursor = conn.cursor()

        cursor.execute("SELECT vida_atual, mana_atual, pontos FROM jogadores WHERE nome = ?", (self.nome,))
        resultado = cursor.fetchone()
        if resultado:
            self.vida_atual, self.mana_atual, self.pontos = resultado
        else:
            self.vida_atual = self.vida_maxima
            self.mana_atual = self.mana_maxima

        conn.close()

    def adicionar_vida(self):
        if self.vida_atual < self.vida_maxima:
            self.vida_atual += 1
            if self.vida_atual > self.vida_maxima:
                self.vida_atual = self.vida_maxima
            self.atualizar_status()

    def subtrair_vida(self):
        if self.vida_atual > 0:
            self.vida_atual -= 1
            if self.vida_atual < 0:
                self.vida_atual = 0
            self.atualizar_status()

    def adicionar_mana(self):
        if self.mana_atual < self.mana_maxima:
            self.mana_atual += 1
            if self.mana_atual > self.mana_maxima:
                self.mana_atual = self.mana_maxima
            self.atualizar_status()

    def subtrair_mana(self):
        if self.mana_atual > 0:
            self.mana_atual -= 1
            if self.mana_atual < 0:
                self.mana_atual = 0
            self.atualizar_status()

    def adicionar_pontos(self):
        self.pontos += 1
        self.atualizar_status()

    def subtrair_pontos(self):
        if self.pontos > 0:
            self.pontos -= 1
            self.atualizar_status()

    def atualizar_status(self):
        self.vida_label.config(text=f"Vida: {self.vida_atual}/{self.vida_maxima}")
        self.mana_label.config(text=f"Mana: {self.mana_atual}/{self.mana_maxima}")
        self.pontos_label.config(text=f"Pontos: {self.pontos}")


def atualizar_banco_dados():
    conn = sqlite3.connect("pontuacoes.db")
    cursor = conn.cursor()

    for jogador in jogadores:
        cursor.execute("UPDATE jogadores SET vida_atual = ?, mana_atual = ?, pontos = ? WHERE nome = ?",
                       (jogador.vida_atual, jogador.mana_atual, jogador.pontos, jogador.nome))

    conn.commit()
    conn.close()


# Criação da janela
window = tk.Tk()
window.title("GENRENCIADO V.1")
window.config(bg=('LightSlateGray'))
# Criação dos jogadores
jogadores = []
jogadores.append(Jogador("XXXXXXX", 12, 12, 0))
jogadores.append(Jogador("XXXXXXX", 12, 12, 1))
jogadores.append(Jogador("XXXXXXX", 12, 12, 2))
jogadores.append(Jogador("XXXXXXX", 12, 12, 3))
jogadores.append(Jogador("XXXXXXX", 12, 12, 4))

# Criação da tabela de jogadores no banco de dados
conn = sqlite3.connect("pontuacoes.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS jogadores (nome TEXT, vida_atual INTEGER, mana_atual INTEGER, pontos INTEGER)")

# Inserindo os jogadores na tabela
for jogador in jogadores:
    cursor.execute("INSERT INTO jogadores (nome, vida_atual, mana_atual, pontos) VALUES (?, ?, ?, ?)",
                   (jogador.nome, jogador.vida_atual, jogador.mana_atual, jogador.pontos))

conn.commit()
conn.close()

# Botão para atualizar o banco de dados
atualizar_button = tk.Button(window, text="Atualizar Banco de Dados", command=atualizar_banco_dados, bg=('Lime'))
atualizar_button.grid(row=5, column=0, pady=10)

# Loop principal da interface
window.mainloop()
