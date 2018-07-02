/**
 * Created by fuyong on 2018/4/17.
 */



$('#closed-btn').on('click',function () {
    $('.modal-cover').fadeOut(1000);
    $('.lock-modal').fadeOut(1000);
});


$('#pwd-submit-btn').on('click',function () {
    var bottom_url = $('body').data('bottom_url');
    var article_id = $('body').data('article_id');
    var pwd = $('#article-pwd').val();

    $.ajax({
        url:'/article_pwd_valid',
        type:'post',
        data:{'article_id':article_id, 'pwd':pwd},
        success:function(arg) {
            if(arg.state==1){
                swal('验证成功','马上为您跳转！','success');
                location.href=bottom_url+'/article/'+article_id+'.html'
            }else{
                swal("密码错误！","请重新输入！",'error');
            }
        }
    });

});


// 博客搜索提交按钮
$('#article_search_btn').on('click',function () {
    var search_keyword = $('#article_search_input').val();
    var bottom_url = $('#bottom_url').val();
    location.href = '/'+bottom_url+'/articles/search/'+search_keyword
});


//登录状态笑脸 鼠标滑动
$('#loginInfo-icon i').mouseover(function () {
    $('#loginInfo').fadeIn(1000);
    $('#loginInfo').fadeOut(5000)
});

// $('#loginInfo-icon i').mouseout(function () {
//     $('#loginInfo').fadeOut(1000)
// });