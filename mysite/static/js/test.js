/*
出现闪烁问题  原因 href机制
没想到直接html, body{
  scroll-behavior:smooth;
}治好了
$(function(){
    $(".class-for-click-scroll").click(function(){
        //根据a标签的href转换为id选择器，获取id元素所处的位置，并高度减50px（这里根据需要自由设置）
        $('html,body').stop().animate({scrollTop: ($($(this).attr('href')).offset().top-150)}, 700);
    });
    return false;
});
*/