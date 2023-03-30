
function Init(E,n1,n2){
    for (e=0;e<n1;e=e+1){
        E[e][0]=e;
        console.log(e,0)
        }
    for (f=0;f<n2;f=f+1){
        E[0][f]=f;
        }
    

}

function distanceEdition(S1,S2){
    m=S1.length;
    n=S2.length;
    E=[];
    for (e=0;e<m;e=e+1){
        E.push([]);
        for (f=0;f<n;f=f+1){
            E[e].push(0);
            
        }
    }
    
    Init(E,m,n);
    //print(m,n)
    
    for (i=0;i<m;i=i+1){
        for (j=0; j<n;j=j+1){
            
            if(i==0){
                E[i][j]=j;}
            else if(j==0){
                E[i][j]=i;}
            else{
                if(S1[i]==S2[j]){
                    e=0;}
                else{
                    e=1;
                
                }
                E[i][j]=Math.min(E[i-1][j]+1,E[i][j-1]+1,E[i-1][j-1]+e);
                }}}
    //print(E[m-1][n-1])
    return E[m-1][n-1]

}







