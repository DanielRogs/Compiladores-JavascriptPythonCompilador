// Teste avançado de classes JavaScript
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

  aniversario() {
    this.idade = this.idade + 1;
    console.log("Agora tenho " + this.idade + " anos");
  }

  cumprimentar(outraPessoa) {
    console.log("Olá " + outraPessoa);
    this.falar();
  }
}

// Testando instanciação e uso
var pessoa1 = new Pessoa("João", 25);
var pessoa2 = new Pessoa("Maria", 30);

// Chamando métodos
pessoa1.falar();
pessoa2.aniversario();
pessoa1.cumprimentar("Pedro");

// Acessando propriedades
console.log(pessoa1.nome);
console.log(pessoa2.idade);
