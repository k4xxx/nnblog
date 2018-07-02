//带密码的博客链接验证
function showArticleDetail(self) {
            $('#article-pwd').val('');
            $('.modal-cover').fadeIn(1000);
            $('.lock-modal').fadeIn(1000);

            var bottom_url = $(self).attr('bottom_url');
            var article_id = $(self).attr('article_id');

            $('body').data('bottom_url',bottom_url);
            $('body').data('article_id',article_id);

        }


$('#closed-btn').click(function () {
    $('.modal-cover').fadeOut(1000)
    $('.comment-modal').fadeOut(1000)
});


$('#comment-icon').on('click',function () {
    $('#comment-area').focus()
});


//点击’回复‘链接的事件
function replyComment(self){
    var $sonCommentDiv = $(self).parent().parent().find('.son-comment');
    $sonCommentDiv.fadeIn(1000);
    $sonCommentDiv.find('textarea').focus();
}


//发表评论框提交按钮
$('#comment-btn').on('click',function () {
    var article_id = $('#article_id').val();
    var comment_content = $('#comment-area').val();
    var username = $('#user').attr('username');
    var avatar = $('#user').attr('avatar');
    var floor = $('.comment').length + 1;

    $.ajax({
        url:'/post_comment/',
        type:'post',
        data:{
            'article_id':article_id,
            'comment_content':comment_content
        },
        success:function (arg) {
            if (arg.state){
                // alert('xxx')
                // swal('恭喜您，发表成功','我现在就去叫博主过来看你的评论哈！','success');
                $('#comment-area').val('');
                //页面ajax显示刚刚评论的内容
                newCommentEle = document.createElement('div');
                $(newCommentEle).attr('class','ui container segment');
                $(newCommentEle).html('<div class="comment"><a class="avatar1"><img src="/media/'+avatar+'"></a>'
                +'<div class="content">'
                    +'<i class="fa fa-flag" aria-hidden="true"></i>&nbsp;'+floor+'楼&nbsp;'
                    +'<i class="fa fa-user-circle-o" aria-hidden="true"></i>'
                    +'<a class="author">&nbsp;'+username+'</a>'
                    +'<div class="metadata"><i class="fa fa-clock-o" aria-hidden="true"></i>'
                    +'<span class="date">&nbsp;刚刚</span></div>'
                    +'<div class="text">'+comment_content+'</div>'
                    // +'<div class="actions"><a class="reply onclick="replyComment(this)">回复</a></div>
                +'</div></div>');
                $('#comments').append(newCommentEle)

            // 页面评论数+1
                var old_comment_count = parseInt($('#comment_count').text())
                $('#comment_count').text(old_comment_count+1)

            }else{
                swal('发表失败','请重新尝试！','error');
            }
        }
    })
});

$('.up-icon').on('click',function () {
    var $cur_icon = $(this);
    $.ajax({
        url:'/article/poll',
        type:'post',
        data:{
            'article_id':$(this).parent().find('input').val(),
            'is_up':'True'
        },
        success:function (arg) {
            if (arg.state == 0){
                //还未登陆
                swal({
                    title:'您还没有登录哦！',
                    text:'要现在去登陆然后狠狠地给博主一赞吗？',
                    type:'warning',
                    showCancelButton:true,
                    confirmButtonColor:'#DD6B55',
                    confirmButtonText:'立即登陆！',
                    cancelButtonText:'我不赞了！',
                    closeOnConfirm:false,
                    closeOnCancel:true,
                    showLoaderOnConfirm:true,
                },
                function(isConfirm){
                    if(isConfirm){
                       location.href = '/login'
                    }
                })
            }else if (arg.state == 1){
                //点赞成功
                $cur_icon.find('.plus1').fadeIn(1000);
                $cur_icon.find('.plus1').fadeOut(1000);
                $cur_icon.find('i').css('color','red');
                var old_up_count = parseInt($($cur_icon).find('.up_count').text());
                new_up_count = old_up_count+1;
                $cur_icon.find('.up_count').text(new_up_count)
            }else if (arg.state == 8){
                 //    说明是博主自己在操作
                swal('不要脸！','自己赞自己！','error');
            }else if(arg.state == 2){
            //    说明已经操作过
                if (arg.is_up){
                 swal('您已经点赞过！','别再拍博主马屁了好吗！','error');
                }else{
                 swal('你到底要干嘛？','之前点踩现在又点赞！','error');
                }
            }
        }
    })
});

$('.down-icon').on('click',function () {
    var $cur_icon = $(this);
    $.ajax({
        url:'/article/poll',
        type:'post',
        data:{
            'article_id':$(this).parent().find('input').val(),
            'is_up':'False'
        },
        success:function (arg) {
            // alert(arg.state == 2);
            if (arg.state == 0){
                //还未登陆
                swal({
                    title:'您还没有登录哦！',
                    text:'要现在去登陆然后狠狠地给博主一赞吗？',
                    type:'warning',
                    showCancelButton:true,
                    confirmButtonColor:'#DD6B55',
                    confirmButtonText:'立即登陆！',
                    cancelButtonText:'我不赞了！',
                    closeOnConfirm:false,
                    closeOnCancel:true,
                    showLoaderOnConfirm:true,
                },
                function(isConfirm){
                    if(isConfirm){
                       location.href = '/login'
                    }
                })
            }else if (arg.state == 8){
            //    说明是博主自己在操作
                swal('丧心病狂啊！','连自己都要踩！','error');
            }else if (arg.state == 1){
                //点赞成功
                $cur_icon.find('.sub1').fadeIn(1000);
                $cur_icon.find('.sub1').fadeOut(1000);
                $cur_icon.find('i').css('color','grey');
                var old_down_count = parseInt($($cur_icon).find('.down_count').text());
                new_down_count = old_down_count+1;
                $cur_icon.find('.down_count').text(new_down_count)
            }else if(arg.state == 2){
            //    说明已经操作过
                if (arg.is_up){
                     swal('你到底要干嘛？','之前点赞现在又点踩！','error');

                }else{
                    swal('您已经点踩过！','给博主留个面子，别再踩啦！','error');
                }
            }
        }
    })
});


//回复子评论
$('body').on('click','.son-reply-icon i',function () {
    var $sonSonCommentDiv = $(this).parent().parent().find('.son-son-comment');
    $sonSonCommentDiv.fadeIn(1000);
    $sonSonCommentDiv.find('textarea').focus();
});


//子子回复框鼠标移除事件
$('body').on('blur','.son-son-comment-area',function () {
    var $sonSonCommentDiv = $(this).parent().parent().find('.son-son-comment');
    $sonSonCommentDiv.fadeOut(1000);
});


//子回复框鼠标移除事件
$('body').on('blur','.son-comment-area',function () {
    var $sonCommentDiv = $(this).parent().parent().find('.son-comment');
    $sonCommentDiv.fadeOut(1000);
});

//点击子回复的提交按钮事件
$('body').on('click','.son-comment-btn',function () {
    var $sonCommentDiv = $(this).parent();
    var pid = $(this).parent().parent().parent().find('.comment_id').val();
    var son_comment_id = $sonCommentDiv.parent().find('.son-comment_id').val();
    var content = $(this).prev().val();
    var article_id = $('#article_id').val();
    var parent_name = $sonCommentDiv.parent().find('.author').text();

    var username = $('#user').attr('username');
    var avatar = $('#user').attr('avatar');
    $.ajax({
        url:'/post_comment/'+pid,
        data:{'comment_content':content,'article_id':article_id},
        type:'post',
        success:function (arg) {
            if (arg.state){
                $sonCommentDiv.find('textarea').val('');
                // alert('success')
                $sonCommentDiv.fadeOut(100);
                // ajax添加元素
                $sonCommentDiv.parent().find('.text').append(`<div class="son-comment-box">
                                        <input type="hidden" class="son-comment_id" value="${son_comment_id}">
                                        <img src="/media/${avatar}">
                                        <span class="author">${username}</span><i class="fa fa-chevron-circle-right" aria-hidden="true"></i>
                                        ${parent_name} ：${content}
                                        <div class="son-reply-icon"><i class="fa fa-commenting-o" aria-hidden="true"></i></div>
                                    </div> `)
            }else{
                alert('error')
            }
        }
    })
    
});



//点击子子回复的提交按钮事件
$('body').on('click','.son-son-comment-btn',function () {
    var $sonSonCommentDiv = $(this).parent();
    var pid = $(this).parent().parent().parent().parent().find('.comment_id').val();
    // var son_comment_id = $sonCommentDiv.parent().find('.son-comment_id').val();
    var content = $(this).prev().val();
    var article_id = $('#article_id').val();
    var parent_name = $sonSonCommentDiv.parent().find('.author').text();

    var username = $('#user').attr('username');
    var avatar = $('#user').attr('avatar');
    $.ajax({
        url:'/post_comment/'+pid,
        data:{'comment_content':content,'article_id':article_id},
        type:'post',
        success:function (arg) {
            if (arg.state){
                $sonSonCommentDiv.find('textarea').val('');
                // alert('success')
                $sonSonCommentDiv.fadeOut(100);
                // ajax添加元素
                $sonSonCommentDiv.parent().parent().append(`<div class="son-comment-box">
                                        <img src="/media/${avatar}">
                                        ${username}<i class="fa fa-chevron-circle-right" aria-hidden="true"></i>
                                        ${parent_name} ：${content}
                                        <div class="son-reply-icon"><i class="fa fa-commenting-o" aria-hidden="true"></i></div>
                                    </div> `)
            }else{
                alert('error')
            }
        }
    })

});