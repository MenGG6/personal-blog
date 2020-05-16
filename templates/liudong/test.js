window.onload=function(){
    lunBo("lbimg","lbbtn");
}
    //轮播图函数
function lunBo(lbimg,lbbtn){
    var lbimgs=document.getElementsByClassName(lbimg);
    var lbbtns=document.getElementsByClassName(lbbtn);
    //图片及标识键设置函数（轮播到当前页面设置透明度为1，标识按钮设置为红色，其他页面隐藏）
    function initSet(index){
        for(var i=0;i<lbimgs.length;i++){
            lbimgs[i].style.opacity='0';
            lbbtns[i].style.backgroundColor='gray';
        }
        lbimgs[index].style.opacity='1';
        lbbtns[index].style.backgroundColor='blue';
    }
    //第一张图片初始化。（最开始时轮播到第一张图）
    initSet(0);
    //自动轮播函数
    var count=1;    //从第二张图开始轮播
    function autoMove(){
        if(count==lbimgs.length){
            count=0;
        }
        initSet(count);
        count++;
    }
    //设置自动轮播时间
    var scollMove=setInterval(autoMove,2000);
    //监听按钮控制跳转当前图片函数
    lbbtns[0].onclick=function(){
        clearInterval(scollMove);
        count=0;
        initSet(count);
        scollMove=setInterval(autoMove,2000);
    }
    lbbtns[1].onclick=function(){
        clearInterval(scollMove);
        count=1;
        initSet(count);
        scollMove=setInterval(autoMove,2000);
    }
    lbbtns[2].onclick=function(){
        clearInterval(scollMove);
        count=2;
        initSet(count);
        scollMove=setInterval(autoMove,2000);
    }
    lbbtns[3].onclick=function(){
        clearInterval(scollMove);
        count=3;
        initSet(count);
        scollMove=setInterval(autoMove,2000);
    }
    //监听左右控件实现前后跳转图片
    var rightbtn=document.getElementById("rightbtn");
    var lefttbtn=document.getElementById("leftbtn");
    rightbtn.onclick=function(){
        clearInterval(scollMove);
        autoMove();
        scollMove=setInterval(autoMove,2000);
    }
    leftbtn.onclick=function(){
        clearInterval(scollMove);
        if(count==0){
            count=lbimgs.length;
        }
        count--;
        initSet(count);
        scollMove=setInterval(autoMove,2000);
    };
}
