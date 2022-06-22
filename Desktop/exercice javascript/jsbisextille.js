     
     let date = prompt('Entrez une année sous forme YYYY:');
     let annee = null;
     if(date.length == 4){
          if(Number(date)){
                annee = Number(date);
               if(annee % 4 === 0){
                    document.getElementById('demo').innerHTML =  'annee bisextille';
                    document.getElementById('demo').style.color = 'green';
                    
               }
               else{
                    document.getElementById('demo').innerHTML =  'annee non bisextille';
                    document.getElementById('demo').style.color = 'red';
                    
               }
          }else{
               alert('entrer un nombre')
          }
     }else{
          alert('entrez une annee de 4 chiffre:')
     }
    
     
     
     


