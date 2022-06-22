const inputNumber = document.getElementById('number');
const msg = document.getElementById('msg');
const checkBtn = document.getElementById('check');
const restartBtn = document.getElementById('restart');

let randomNumber = Math.floor(Math.random() * 20) + 1;
let count = 0;

restartBtn.addEventListener('click', restart);

function restart() {
    location.reload();
}

checkBtn.addEventListener('click', () => {

    if(inputNumber.value !== ''){
        msg.innerHTML = '';

        count++;

        let number = Number(inputNumber.value);

        if(number === randomNumber){
            msg.innerHTML = `Vous avez reussi au bout de ${count} coups. BRAVO !!!`;
            msg.style.color = 'green';
            checkBtn.disabled = true;
        }
        else{
            let error = number > randomNumber ? 
            'Le nombre a trouver est plus petit !' : 
            'Le nombre a trouver est plus grand !';
            msg.innerHTML = error;
            msg.style.color = 'red';
        }

    }
    else{
        msg.innerHTML = 'Le champ ne doit pas etre vide !';
        msg.style.color = 'red'
    }
})

// EXO 2 RESOLUTION
// REST parameter
function sommeIndeterminer(...args){
    // const args = [a, b, c, d, e, f];
    let somme = 0;
    
    for(let i = 0; i < args.length; i++){
      somme+= args[i]
    }
    
    return somme;
  }
  
// console.log(sommeIndeterminer(5, 5));
  