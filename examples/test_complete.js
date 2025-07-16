// Teste completo passo a passo
class Pessoa {
  constructor(nome, idade) {
    this.nome = nome;
    this.idade = idade;
    console.log("Pessoa criada!");
  }

  falar() {
    console.log("Olá, eu sou " + this.nome);
    return this.nome;
  }
}

var pessoa1 = new Pessoa("João", 25);
pessoa1.falar();
