window.onscroll=function(){
    scrollFunction();
};


function scrollFunction(){
    if(document.body.scrollTop > 160 || document.documentElement.scrollTop > 160){
        document.getElementById("btnScroll").style.display = "block";
        document.getElementById("btnScroll-1").style.display = "block";
        document.getElementById("btnScroll-2").style.display = "block";
        document.getElementById("btnScroll-3").style.display = "block";
    }else{
        document.getElementById("btnScroll").style.display = "none";
        document.getElementById("btnScroll-1").style.display = "none";
        document.getElementById("btnScroll-2").style.display = "none";
        document.getElementById("btnScroll-3").style.display = "none";
    }
};


function toUp(){
    timer=setInterval(function(){   
        var scrollTop=document.documentElement.scrollTop||document.body.scrollTop;
        var ispeed=Math.floor(-scrollTop/6);
        // console.log(ispeed);
        if(scrollTop==0){
            clearInterval(timer);
        }
        document.documentElement.scrollTop=document.body.scrollTop=scrollTop+ispeed;
    },13)
    // document.body.scrollTop = 0;
    // document.documentElement.scrollTop = 0;
};