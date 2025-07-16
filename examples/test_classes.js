// Teste básico de classe JavaScript
class Pessoa {
  constructor(nome, idade) {
    console.log("Criando pessoa...");
  }

  falar() {
    console.log("Olá!");
  }

  andar(passos) {
    console.log("Andando...");
  }
}

// Classe vazia para teste
class Vazia {}

// Classe só com constructor
class SoConstructor {
  constructor() {
    console.log("Só constructor");
  }
}

// Classe só com métodos
class SoMetodos {
  metodo1() {
    return "teste";
  }

  metodo2(x, y) {
    return x + y;
  }
}
