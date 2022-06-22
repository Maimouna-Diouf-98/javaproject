
document.getElementById('soumis').addEventListener('click', (e)=>{
   e.preventDefault();
    let m = Number(document.getElementById('ligne').value);
    let n = Number(document.getElementById('col').value);

  
    
    if(Number.isInteger(m,n)){
      let tab = document.getElementById('para');
      let addlign =  '';
      for (let i = 1; i <=m; i++) {
        addlign+= '<tr>';
        for (let j = 1; j <=n; j++) {
            addlign+= '<td>' + i*j ;
        }
        addlign+= '<tr>';
      }
      tab.innerHTML = addlign;
      console.log(m,n, tab);
    }
    else{
        alert('entrez un nombre entier')
    }
})

document.getElementById('recommencer').addEventListener('click', (e)=>{
    e.preventDefault();
   location.reload();
 })
 


