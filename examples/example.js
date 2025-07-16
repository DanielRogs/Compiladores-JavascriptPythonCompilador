console.log("This is an example JavaScript code snippet.");

// Isto é um exemplo de comentário em JavaScript

var obj = { a: 1, b: 2 };
for (var key in obj) {
  console.log(key);
}

var arr = [10, 20, 30];
for (var item of arr) {
  console.log(item);
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

function eqStrict(a, b) {
  return a === b;
}

function neqStrict(a, b) {
  return a !== b;
}

var x = true && false;
var y = true || false;
console.log(x);
console.log(y);

let a = 10;
const PI = 3.14;
var b = a + PI;
console.log(b);
