import unittest
from aluno import AlunoClass
from turma import TurmaClass
from conexao import ConexaoClass
import mongomock  # Projeto: https://github.com/mongomock/mongomock

class alunoTest(unittest.TestCase):
  @mongomock.patch(servers=(('localhost.com', 27017),))
  def setUp(self):
    print('Teste', self._testMethodName, 'sendo executado...')
    self.aluno = AlunoClass('Fabio', 'Teixeira', 10)
    self.turma = TurmaClass()
    self.turma.cadastrarAlunos([self.aluno])
    self.conexao = ConexaoClass.conexaoMongoDB(self, url='localhost.com', banco='faculdade')

  def test_salvarAluno(self):
    resp = self.aluno.salvar(conexao=self.conexao, colecao='aluno')
    self.assertEqual(True, resp, 'Aluno cadastrado incorretamente!')

    # verificação extra
    doc = self.conexao['aluno'].find_one({"nome": "Fabio", "sobrenome": "Teixeira"})
    self.assertIsNotNone(doc, 'Documento do aluno não encontrado no banco (stub).')
    self.assertEqual(10, doc['nota'])

  def test_salvarTurma(self):
    resp = self.turma.salvar(conexao=self.conexao, colecao='turma')
    self.assertEqual(True, resp, 'Turma cadastrada incorretamente!')

if __name__ == "__main__":
  unittest.main()
