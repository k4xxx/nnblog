/**
 * Created by fuyong on 2018/4/13.
 */

toastr.options = {
        closeButton: false,
        debug: false,
        progressBar: false,
        positionClass: "toast-top-center",
        onclick: null,
        showDuration: "300",
        hideDuration: "1000",
        timeOut: "5000",
        extendedTimeOut: "1000",
        showEasing: "swing",
        hideEasing: "linear",
        showMethod: "fadeIn",
        hideMethod: "fadeOut",

    };


// 注册表单验证
// 输入框失去光标时验证
$('input').blur(function () {
    var $cur_input = $(this);
    var $errorMsgSpan = $(this).parent().prev().find('span');
    var $errorIconSpan = $(this).parent().find('.checke-icon');
    if ($(this)[0].name == 'telephone' || $(this)[0].name == 'email'){
        //如果是电话和邮箱  则不要求必填
    }
    else if($(this).val() == ''){
       $errorIconSpan.html('<i class="fa fa-remove fa-fw" aria-hidden="true"></i>');
        if ($errorMsgSpan.hasClass('my-hidden')){
            $errorMsgSpan.removeClass('my-hidden');
            $(this).parent().addClass('has-error')
        }
        // $(this).addClass('active')
    }
    // console($('input').val())
    if ($(this).val() != ''){
        // alert('不为空')
        //如果不为空，则发ajax验证
        // console.log($(this)[0].name);
        $.ajax({
            url:'/reg_valid',
            type:'post',
            data:{'inp_name':$(this)[0].name,'inp_value':$(this).val()},
            success:function (arg) {
                // alert(arg.state=='True');
                if (arg.state){
                    // alert('对了');
                    // 提示对勾
                    $errorIconSpan.html('<i class="fa fa-check fa-fw" aria-hidden="true"></i>');
                    $errorMsgSpan.text('必填项，您还没有输入内容'); // 占位
                }else{
                    // alert('展示错误信息')
                    // console.log( $errorIconSpan);
                    $($cur_input).parent().addClass('has-error');
                    $errorIconSpan.html('<i class="fa fa-remove fa-fw" aria-hidden="true"></i>');
                    $errorMsgSpan.text(arg.msg);
                    if ($errorMsgSpan.hasClass('my-hidden')){
                        $errorMsgSpan.removeClass('my-hidden');

                    }
                }
            }
        })

    }

});

$('input').focus(function () {
    var $errorMsgSpan = $(this).parent().prev().find('span');
    if (!$errorMsgSpan.hasClass('my-hidden')){
        $errorMsgSpan.addClass('my-hidden');
        $(this).parent().removeClass('has-error')
    }
});



// 提交按钮时验证
$('#register-submit-btn').on('click',function () {
        var username = $('#usr-inp').val();
        var password = $('#pwd-inp').val();
        var password2 = $('#pwd-inp2').val();
        var telephone = $('#telephone-inp').val();
        var nickname = $('#nickname-inp').val();
        var email = $('#email-inp').val();
        var agreement = $('[name=agreement]').is(':checked');
        if (username == '') {
            // 如果用户名或者密码为空，则给提示，不提交
            toastr.error('用户名不能为空', 'Error');
        }else if(password == ''){
            toastr.error('密码不能为空', 'Error');
        }else if(password2 == ''){
            toastr.error('重复密码不能为空', 'Error');
        }else if(nickname == ''){
             toastr.error('昵称不能为空', 'Error');
        }else if(password !== password2){
            toastr.error('两次密码输入不一致', 'Error');
        }else if(agreement == ''){
            toastr.error('请仔细阅读并且同意用户协议', 'Error');
        }
        else {
            // 否则，用ajax提交
            $.ajax({
                url:'/register',
                type:'post',
                data:{
                    'username':username,
                    'password':password,
                    'password2':password2,
                    'nickname':nickname,
                    'telephone':telephone,
                    'email':email,
                    'agreement':agreement
                },
                success:function (arg) {
                    if (arg.state){
                        sweetAlert('恭喜您！','注册成功，请开始您的表演！','success');
                        setTimeout(function(){
                            window.location.href='/login'
                        },1500);

                    }else{
                        swal('注册信息填写有误!',arg.msg,'error')
                    }
                }
            })
        }
});

//重置按钮
$('#reg-reset-btn').on('click',function () {
    $('input').val('');
});
