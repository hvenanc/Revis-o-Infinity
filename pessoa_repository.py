from pessoa import Pessoa

class PessoaRepository:
    def __init__(self, db):
        self.conn = db.get_connection()

    def inserir(self, pessoa):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO pessoa (nome, idade, email) VALUES (?, ?, ?)", (pessoa.nome, pessoa.idade, pessoa.email))
        self.conn.commit()

    def listar(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pessoa")
        rows = cursor.fetchall()
        return [Pessoa(id=row[0], nome=row[1], idade=row[2], email=row[3]) for row in rows]
    
    def listar_por_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pessoa WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return Pessoa(id=row[0], nome=row[1], idade=row[2], email=row[3])
        else:
            return None

    def atualizar(self, pessoa):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE pessoa SET nome = ?, idade = ?, email = ? WHERE id = ?", (pessoa.nome, pessoa.idade, pessoa.email, pessoa.id))
        self.conn.commit()

    def deletar(self, pessoa_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM pessoa WHERE id = ?", (pessoa_id,))
        self.conn.commit()
