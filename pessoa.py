class Pessoa:
    def __init__(self, nome, idade, email, id=None):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.email = email

    def __repr__(self):
        return (
            f"\n"
            f"{'-'*30}\n"
            f"{'ID':<10} | {self.id}\n"
            f"{'NOME':<10} | {self.nome}\n"
            f"{'EMAIL':<10} | {self.email}\n"
            f"{'IDADE':<10} | {self.idade} anos"
        )

