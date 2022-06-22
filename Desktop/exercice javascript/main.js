let quantite =document.getElementById('quantite');

let prix_ht = document.getElementById('prix_ht');

let montant_ht = document.getElementById('montant') ;
let total_ttc = document.getElementById('total_ttc') ;
let tva = null;



let radio =  document.querySelectorAll('input[type ="radio"]');

for (let i = 0; i < radio.length; i++) { 
       let rd = radio[i];
       
       console.log(rd.value);  
       
       rd.addEventListener('click', ()=>{
              
              total_ttc.value = montant_ht.value + (montant_ht.value * (rd.value/100))
              console.log(total_ttc.value);
              
       });
       
}


document.getElementById('calculer').addEventListener('click', ()=>{
       montant_ht.value = quantite.value * prix_ht.value; 
       
       
       
});


document.getElementById('effacer').addEventListener('click',supprimer);
function supprimer(){
       document.querySelectorAll('input').forEach(input => input.value = "");
}





