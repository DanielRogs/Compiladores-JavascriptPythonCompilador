console.log("This is an example JavaScript code snippet.");

// Isto é um exemplo de comentário em JavaScript

var x = [1, 2, 3];

for (var i in x) {
  console.log("Index: " + i + ", Value: " + x[i]);
}

var y = 20 + 15;
if (x > y) {
  console.log("x is greater than y");
} else {
  console.log("x is not greater than y");
}

while (x != y) {
  console.log("x is still less than y");
  x++;
}

function add(a, b) {
  return a + b;
}

var dobroLambda = (n) => n * 2;

var dobro = (n) => {
    console.log("Calculando o dobro...");
    return n * 2;
};