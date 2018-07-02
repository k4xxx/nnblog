//提示框 toastr设置
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
        hideMethod: "fadeOut"
    };


/////////////////////////////////表单验证////////////////////////////////////
//发表博客表单验证
//博客标题 输入框失去焦点的事件
//判断标题是否已存在

//发表博客时存入草稿按钮点击事件
$('#post_drafts_blog').on('click',function () {
        if ($('.blog-title-inp').val() == '') {
            // 如果博客标题为空，则给提示，不提交
            toastr.error('博客标题不能为空!', 'Error');
        }
        else {
            // 否则，提交
            document.forms.writeBlogForm.action="/manage/article/drafts/";
            swal('已存入草稿','请去博客草稿箱查看','success');
            $('.blog-form').submit();
        }
});

//发表博客立即发布按钮点击事件
$('#post_blog').on('click',function () {
        if ($('.blog-title-inp').val() == '') {
            // 如果博客标题为空，则给提示，不提交
            toastr.error('博客标题不能为空!', 'Error');
        }
        else {
            //判断标题是否已存在
            // 否则，提交
            document.forms.writeBlogForm.action="/manage/article/add/";
            $('.blog-form').submit();
            swal('发布成功','请去博客管理页面查看','success')
        }
});

//编辑博客发布按钮点击事件
$('#update-article').on('click',function () {
        if ($('.blog-title-inp').val() == '') {
            // 如果博客标题为空，则给提示，不提交
            toastr.error('博客标题不能为空!', 'Error');
        }
        else {
            var article_id =  $('#article_id').val();
            //判断标题是否已存在
            // 否则，提交
            document.forms.updateArticleForm.action="/manage/article/update/" + article_id;
            document.forms.updateArticleForm.submit();
            swal('发布成功','请去博客管理页面查看','success')
        }
});


//编辑博客存入草稿箱按钮点击事件
$('#update-drafts-article').on('click',function () {
        if ($('.blog-title-inp').val() == '') {
            // 如果博客标题为空，则给提示，不提交
            toastr.error('博客标题不能为空!', 'Error');
        }
        else {
            var article_id =  $('#article_id').val();
            //判断标题是否已存在
            // 否则，提交
            document.forms.updateArticleForm.action="/manage/article/drafts/" + article_id;
            document.forms.updateArticleForm.submit();
            swal('发布成功','请去博客草稿箱查看','success')
        }
});


///////////////////////////////博客管理///////////////////////////////////////

//删除博客（包括已发布和草稿箱里的）
$('.delete-blog-icon').on('click',function (){
    // alert('xxxxxxx');
    var $delete_tr = $(this).parent().parent();
    var $blog_id = $delete_tr.find('input').val();
   swal({
            title:'确定要抛弃本博吗？',
            text:'一旦删除，将无法恢复！',
            type:'warning',
            showCancelButton:true,
            confirmButtonColor:'#DD6B55',
            confirmButtonText:'狠心删除！',
            cancelButtonText:'饶你一命！',
            closeOnConfirm:false,
            closeOnCancel:false,
           showLoaderOnConfirm:true,
        },
        function(isConfirm){
            if(isConfirm){
                // 发送ajax请求
                $.ajax({
                    url:'/manage/article/delete/'+$blog_id,
                    type:'get',
                    success:function (arg) {
                        if (arg.state){
                            swal("已删除！","太狠了，再见主人！",'success');
                        //    从页面删除当前行
                            $delete_tr.remove()
                        }else {
                            swal('错误！',"删除失败，请重新尝试！",'error');
                        }
                    }

                });


            }else{
                swal('取消！',"谢谢主人不杀之恩！",'error');
            }
        }
        )
});

// 发布草稿箱博客
$('.fabu-blog-icon').on('click',function () {
    var $post_tr = $(this).parent();
    var $blog_id = $post_tr.parent().find('input').val();
    
    swal({
            title:'确定要发布本篇博客吗？',
            text:'发布后博客将对外公开',
            type:'warning',
            showCancelButton:true,
            confirmButtonColor:'#DD6B55',
            confirmButtonText:'现在发布！',
            cancelButtonText:'以后再说！',
            closeOnConfirm:false,
            closeOnCancel:false
        },
        function(isConfirm){
            if(isConfirm){
                //    ajax发请求，将blog的is_post状态改为True
                $.ajax({
                    url :'/post_drafts_blog',
                    type:'get',
                    data:{'blog_id':$blog_id},
                    success:function (arg) {
                        if (arg.state){
                            swal("已发布！","请去博客管理页面查看！",'success');
                            $post_tr.remove();
                        }else{
                            swal("发布失败！","请重新尝试！",'error');
                        }
                    }
                })

            }else{
                swal('取消！',"博客未发布！",'error');
            }
        }
        )
    
});

//置顶博客按钮
$('.zhiding-icon').on('click',function () {
    var $post_tr = $(this).parent().parent();
    var $blog_id = $post_tr.find('input').val();

    swal({
            title:'确定要将本篇博客置顶吗？',
            text:'置顶后将在首页优先展示！',
            type:'warning',
            showCancelButton:true,
            confirmButtonColor:'#DD6B55',
            confirmButtonText:'立即置顶！',
            cancelButtonText:'以后再说！',
            closeOnConfirm:false,
            closeOnCancel:false,
            showLoaderOnConfirm:true,
        },
        function(isConfirm){
            if(isConfirm){
                //    ajax发请求，将blog的is_sticky状态改为True
                $.ajax({
                    url :'/manage/article/stick/'+$blog_id,
                    type:'get',
                    success:function (arg) {
                        alert(arg.state)
                        if (arg.state===1){
                        //    说明已经置顶
                            swal("别瞎点了老铁","博客已经是置顶状态",'error');
                        }
                        else if (arg.state){
                            swal("已置顶！","博客将在首页优先展示！",'success');
                        }else{
                            swal("置顶失败！","请重新尝试！",'error');
                        }
                    }
                })

            }else{
                swal('取消！',"博客未置顶！",'error');
            }
        }
        )
    
});

// 设置密码按钮
$('body').on('click','.suo-btn',function () {
    $('.cover').fadeIn(1000);
    $('.suo-modal').fadeIn(1000);
    //获取点击当前行的博客id
    var blog_id = $(this).parent().parent().find('input').val();
//    设置属性  记录点击的当前行博客id,以便知道要修改的是哪个博客的密码
    $('body').data('blog_id',blog_id);
//    设置属性  记录点击的当前图标,以便根据是否有密码来切换图标
    $('body').data('suo_icon_td',$(this).parent());


});

// 设置密码模态框取消按钮
$('body').on('click','.suo-close-btn',function () {
        $('.suo-modal').fadeOut(1000);
        $('.cover').fadeOut(1000);
});

//修改密码或者取消密码的 提交按钮
$('body').on('click','.set-pwd-btn',function () {
    //从data里获取需要修改的博客id（弹出模态框的时候设置的data）
    var blog_id = $('body').data('blog_id');
    // alert(blog_id);
    //从data里获取需要修改的那一行的锁图标的td（弹出模态框的时候设置的data）
    var suo_icon_td = $('body').data('suo_icon_td');
    // alert(suo_icon_td);
    // 获取输入框里的值
    var pwd = $('#password').val();
    // 关闭模态框
    $('.suo-modal').fadeOut(1000);
    $('.cover').fadeOut(1000);
    // 发送ajax请求
    $.ajax({
        url:'/manage/article/password/'+blog_id,
        type:'post',
        data:{'pwd':pwd},
        success:function (arg) {
            // alert(arg.state);
            if (arg.state){
            //    如果arg.pwd为空，说明是解锁，将锁图标换成解锁的图标
            //     alert(arg.pwd == '');
                if (pwd == ''){
                    suo_icon_td.html('<i class="fa fa-unlock suo-btn suo-icon" aria-hidden="true"></i>')
                    swal("恭喜您！","密码已解除！",'success');
                }else{
                    suo_icon_td.html('<i class="fa fa-lock suo-btn suo-icon" aria-hidden="true"></i>')
                    swal("恭喜您！","博客已上锁！",'success');
                }
            //    否则，换成上锁的图标
            }else{
                swal("修改失败","请重新尝试！",'error');
            }
        }
    })
});


///////////////////////////分类管理//////////////////////////////////////

//编辑分类按钮单击显示模态框
$('body').on('click','.edite-category-inco',function () {
    $('.cover').fadeIn(1000);
    $('.category-modal').fadeIn(1000);
    //点击的当前tr行
    var $curTrEle = $(this).parent().parent().parent();
    //当前行的分类的id
    var $curCateId = $curTrEle.find('.cate_id_inp').val();
    var cate_title =$curTrEle.find('.cate-title').text();
    var cate_info = $curTrEle.find('.cate-info').text();
    $('.category-modal input').val(cate_title);
    $('.category-modal textarea').val(cate_info);

    $('body').data('$curCateId',$curCateId);
    $('body').data('$curTrEle',$curTrEle);

});

//编辑分类模态框取消按钮
$('#category-modal-close-btn').on('click',function () {
   $('.cover').fadeOut(1000);
    $('.category-modal').fadeOut(1000);
});

//添加新分类按钮
$('#add-category-btn').on('click',function () {

    $('.category-modal input').val('');
    $('.category-modal textarea').val('');
    $('.cover').fadeIn(1000);
    $('.category-modal').fadeIn(1000);
});


//编辑分类模态框取消按钮
$('#friend-modal-close-btn').on('click',function () {
   $('.cover').fadeOut(1000);
    $('.friendlink-modal').fadeOut(1000);
});


// 添加/编辑  博客分类提交按钮绑定事件

$('#handle-category-btn').on('click',function () {
    // alert('添加成功')
    var cate_name = $('.category-modal input').val();
    var cate_info = $('.category-modal textarea').val();

    //如果 $('body').data('$curCateId')有数据，书名是点编辑进来的
    var cate_id = $('body').data('$curCateId');
    var $curTrEle = $('body').data('$curTrEle');

    if (cate_id == undefined){

        // 说明是添加新的分类
        //如果分类标题为空，给与提示
        if (cate_name == ''){
            swal("分类标题不能为空!","请重新输入！","error");
            return
        }
        $.ajax({
            url:'/manage/category/add/',
            type:'post',
            data:{'cate_name':cate_name,'cate_info':cate_info},
            success:function (arg) {
            $('.cover').fadeOut(1000);
            $('.category-modal').fadeOut(1000);
            // alert(arg.state);
            if (arg.state){
                swal("添加成功！","又多了一条新分类！",'success');
                 //    添加一行tr
                var newTr = document.createElement('tr');
                $(newTr).html(
                    '<input class="cate_id_inp" type="hidden" name="cate_id" value='+arg.cate_id+'>\
                    <td class="cate-title">'+cate_name+'</td>\
                    <td class="cate-info">'+cate_info+'</td>\
                    <td class="edit-td"><a><i class="fa fa-pencil edite-category-inco" aria-hidden="true"></i></a></td>\
                    <td class="delete-td"><i class="fa fa-trash-o fa-lg delete-cate-icon"></i></td>'
                );
                $('tbody').append(newTr)
            }else {
                swal("添加失败！","请重试！",'error');
            }

        }
    })
    }
    else {
        $.ajax({
            url: '/manage/category/update/' + cate_id,
            type: 'post',
            data: {'cate_id': cate_id, 'cate_name': cate_name, 'cate_info': cate_info},
            success: function (arg) {
                $('.cover').fadeOut(1000);
                $('.category-modal').fadeOut(1000);
                alert(arg.state);
                if (arg.state) {
                    swal("编辑成功！", "恭喜！", 'success');
                    //    修改当前行的td
                    $curTrEle.find('.cate-title').text(cate_name);
                    $curTrEle.find('.cate-info').text(cate_info);
                } else {
                    swal("编辑失败！", "请重试！", 'error');
                }
            }
        });
        //    将$('body').data重新设置为空
        $('body').data('$curCateId', null)
    }


});


// 删除分类按钮点击事件

$('body').on('click','.delete-cate-icon',function () {
    var $delete_tr = $(this).parent().parent();
    var $cate_id = $delete_tr.find('input').val();
   swal({
            title:'确定删除分类吗？',
            text:'一旦删除，将无法恢复！',
            type:'warning',
            showCancelButton:true,
            confirmButtonColor:'#DD6B55',
            confirmButtonText:'狠心删除！',
            cancelButtonText:'饶你一命！',
            closeOnConfirm:false,
            closeOnCancel:false,
           showLoaderOnConfirm:true,
        },
        function(isConfirm){
            if(isConfirm){
                // 发送ajax请求
                $.ajax({
                    url:'/manage/category/delete/'+$cate_id,
                    type:'get',
                    success:function (arg) {
                        if (arg.state){
                            swal("已删除！","太狠了，再见主人！",'success');
                        //    从页面删除当前行
                            $delete_tr.remove()
                        }else {
                            swal('错误！',"删除失败，请重新尝试！",'error');
                        }
                    }

                });
                
            }else{
                swal('取消！',"谢谢主人不杀之恩！",'error');
            }
        }
        )
});



///////////////////////////友情链接管理//////////////////////////////////////

// 删除友情链接按钮点击事件

$('body').on('click','.delete-link-icon',function () {
    var $delete_tr = $(this).parent().parent();
    var link_id = $delete_tr.find('input').val();
    alert(link_id)
   swal({
            title:'确定删除此条链接吗？',
            text:'一旦删除，将无法恢复！',
            type:'warning',
            showCancelButton:true,
            confirmButtonColor:'#DD6B55',
            confirmButtonText:'狠心删除！',
            cancelButtonText:'饶你一命！',
            closeOnConfirm:false,
            closeOnCancel:false,
           showLoaderOnConfirm:true
        },
        function(isConfirm){
            if(isConfirm){
                // 发送ajax请求
                $.ajax({
                    url:'/manage/friendlylink/delete/'+link_id,
                    type:'get',
                    success:function (arg) {
                        if (arg.state){
                            swal("已删除！","太狠了，再见主人！",'success');
                        //    从页面删除当前行
                            $delete_tr.remove()
                        }else {
                            swal('错误！',"删除失败，请重新尝试！",'error');
                        }
                    }

                });
                
            }else{
                swal('取消！',"谢谢主人不杀之恩！",'error');
            }
        }
        )
});

//添加新链接图标点击时间
$('#add-frindlink-btn').on('click',function () {
     $('.friendlink-modal input').val('');
    $('.friendlink-modal textarea').val('');
   $('.cover').fadeIn(1000);
    $('.friendlink-modal').fadeIn(1000);
});

//编辑友情链接按钮 单击显示模态框
$('body').on('click','.edit-link-inco',function () {
   $('.cover').fadeIn(1000);
    $('.friendlink-modal').fadeIn(1000);
    var link_title = $(this).parent().parent().parent().find('.link-title').text();
    var link_url = $(this).parent().parent().parent().find('.link-url').text();
    $('.friendlink-modal input').val(link_title);
    $('.friendlink-modal textarea').val(link_url);

    var $curTrEle = $(this).parent().parent().parent();
    //当前行的分类的id
    var $curlinkId = $curTrEle.find('.link_id_inp').val();
    // alert($curlinkId)

    $('body').data('$curLinkId',$curlinkId);
    $('body').data('$curTrEle',$curTrEle);

});

// 添加/编辑  友情链接提交按钮绑定事件

$('#handle-link-btn').on('click',function () {
    // alert('添加成功');
    var link_name = $('.friendlink-modal input').val();
    var link_info = $('.friendlink-modal textarea').val();

    //如果 $('body').data('$curCateId')有数据，书名是点编辑进来的
    var link_id = $('body').data('$curLinkId');
    var $curTrEle = $('body').data('$curTrEle');
    // alert($curTrEle);
    if (link_id != undefined){
        // alert('有id啊');
        $.ajax({
        url:'/manage/friendlylink/update/'+link_id,
        type:'post',
        data:{'link_title':link_name,'link_url':link_info},
        success:function (arg) {
            $('.cover').fadeOut(1000);
            $('.friendlink-modal').fadeOut(1000);
            // alert(arg.state);
            if (arg.state){
                swal("编辑成功！","恭喜！",'success');
            //    修改当前行的td
                $curTrEle.find('.link-title').text(link_name);
                $curTrEle.find('.link-url').text(link_info);
            }else {
                swal("编辑失败！","请重试！",'error');
            }
        }
    });
    //    将$('body').data重新设置为空
        $('body').data('$curLinkId',null)
    }else{
        // 说明是添加新的分类
        //如果分类标题为空，给与提示
        if (link_name == ''){
            swal("友情链接标题不能为空!","请重新输入！","error");
            return
        }
        alert(link_name);
        alert(link_info);
        $.ajax({
        url:'/manage/friendlylink/add/',
        type:'post',
        data:{'link_title':link_name,'link_url':link_info},
        success:function (arg) {
            alert('请求已响应');
            $('.cover').fadeOut(1000);
            $('.friendlink-modal').fadeOut(1000);
            alert(arg.state);
            if (arg.state){
                alert(arg.link_id)
                swal("添加成功！","又多了一条新链接！",'success');
                 //    添加一行tr
                var newTr = document.createElement('tr');
                $(newTr).html(
                    '<input type="hidden" class="link_id_inp" value='+arg.link_id+ '>\
                    <td class="link-title">'+link_name+'</td>\
                    <td class="link-url">'+link_info+'</td>\
                    <td class="edit-td"><a><i class="fa fa-pencil edit-link-inco" aria-hidden="true"></i></a></td>\
                    <td class="delete-td"><i class="fa fa-trash-o fa-lg delete-link-icon"></i></td>'
                );
                $('tbody').append(newTr)
            }else {
                swal("添加失败！","请重试！",'error');
            }

        }
    })
    }
});

// 修改头像时文件inpu改变事件
$('#avatar-file-inp').on('change',(function () {
    // 1、本地预览
        // 获取用户最后一次选择的图片
        var choose_file=$(this)[0].files[0];
        // 创建一个新的FileReader对象，用来读取文件信息
        var reader=new FileReader();
        // 读取用户上传的图片的路径
        reader.readAsDataURL(choose_file);
        // 读取完毕之后，将图片的src属性修改成用户上传的图片的本地路径
        reader.onload=function () {
             $("#avatar-img").attr("src",reader.result)
        };
    // 2、上传服务器
    formdata = new FormData();

    formdata.append("avatar",$("#avatar-file-inp")[0].files[0]);

    var post_url = '/userinfo/update/avatar';

    $.ajax({
        url:post_url,
        type:'post',
        processData:false,
        contentType:false,
        data:formdata,
        success:function (arg) {
            if (arg.state){
                swal("恭喜您！","头像修改成功！",'success');
            }else {
                swal("头像修改失败！","请重试！",'error');
            }
        }
    })
}));


// 修改微信二维码时文件inpu改变事件
$('#wechat-file-inp').on('change',(function () {
    // 1、本地预览
        // 获取用户最后一次选择的图片
        var choose_file=$(this)[0].files[0];
        // 创建一个新的FileReader对象，用来读取文件信息
        var reader=new FileReader();
        // 读取用户上传的图片的路径
        reader.readAsDataURL(choose_file);
        // 读取完毕之后，将图片的src属性修改成用户上传的图片的本地路径
        reader.onload=function () {
             $("#wechat-img").attr("src",reader.result)
        };
    // 2、上传服务器
    formdata = new FormData();

    formdata.append("wechat",$("#wechat-file-inp")[0].files[0]);

    var post_url = '/userinfo/update/wechat';

    $.ajax({
        url:post_url,
        type:'post',
        processData:false,
        contentType:false,
        data:formdata,
        success:function (arg) {
            if (arg.state){
                swal("恭喜您！","微信二维码修改成功！",'success');
            }else {
                swal("二维码修改失败！","请重试！",'error');
            }
        }
    })
}));

// 修改密码提交按钮
$('#update-pwd-submit-btn').on('click',function () {
    old_pwd = $('#pwd-inp').val();
    new_pwd1 = $('#pwd-inp1').val();
    new_pwd2 = $('#pwd-inp2').val();
    var post_url = '/userinfo/update/password';
    $.ajax({
        url:post_url,
        type:'post',
        data:{'old_pwd':old_pwd,'new_pwd1':new_pwd1,'new_pwd2':new_pwd2},
        success:function (arg) {

            if (arg.state){
                swal("恭喜您！","密码修改成功！",'success');
            }else {
                swal("修改失败！", arg.msg, 'error');
            }
        }
    })
});

// 修改用户信息提交按钮
$('#update-info-submit-btn').on('click',function () {
    nickname = $('#nickname-inp').val();
    telephone = $('#telephone-inp').val();
    email = $('#email-inp').val();
    qq = $('#qq-inp').val();
    site = $('#site-inp').val();
    site_title = $('#site-title-inp').val();
    signature = $('#signature').val();

    var post_url = '/userinfo/update/info_detail';
    $.ajax({
        url:post_url,
        type:'post',
        data:{
            'nickname':nickname,
            'telephone':telephone,
            'email':email,
            'qq':qq,
            'site':site,
            'site_title':site_title,
            'signature':signature,
        },
        success:function (arg) {

            if (arg.state){
                swal("恭喜您！","信息修改成功！",'success');
            }else {
                swal("修改失败！", arg.msg, 'error');
            }
        }
    })
});
