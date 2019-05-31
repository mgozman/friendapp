$(document).ready(function(){
    const csrf_input = document.querySelector('input[name=csrfmiddlewaretoken]');
    const csrf = csrf_input.name + '=' + csrf_input.value;

    const status = $('#user_status');
    const city = $('#user_city');
    const marrige = $('#user_marrige');
    const phone = $('#user_phone');
    const school = $('#user_school');
    const skype = $('#user_skype');


    function updateProfile() {
        let data = csrf;
        data += '&status=' + status[0].value;
        data += '&city=' + city[0].value;
        data += '&marrige=' + marrige[0].value;
        data += '&phone=' + phone[0].value;
        data += '&school=' + school[0].value;
        data += '&skype=' + skype[0].value;
        $.ajax({
            url: "update_profile",
            method: "post",
            data: data,
            dataType: 'json',
            success: function(response) {
            }
        });
    };

    function setupProfileInput(input) {
        $('.edit_value').focusout(updateProfile);
        $('.edit_value').keypress(function(e){
            if (e.which == 13){
                e.preventDefault();
                updateProfile();
                $(this).blur();
            };
        });
    };

    setupProfileInput(status);
    setupProfileInput(city);
    setupProfileInput(marrige);
    setupProfileInput(school);
    setupProfileInput(phone);
    setupProfileInput(skype);

    $('#user_phone').keypress(function(e){
        if (e.key >= 0 && e.key <= 9 && e.key != ' '){
        } else {
            return false;
        }
    });

    $('#post').submit(function(){
        url_str = $(this).find('.users_where_to_post').val();
        $.ajax({
            url: url_str + "/post_process",
            method:"post",
            data:$(this).serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
        $(this).trigger('reset');
        return false;
    });

    $('.new_comment_form').submit(function(){
        url_str = $(this).find('.post_id').val();
        $.ajax({
            url: url_str + "/comment_process",
            method:"post",
            data:$(this).serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
        $(this).trigger('reset');
        return false;
    });

    
    $('.new_comment').keypress(function(){
        if (e.which == 13){
            url_str = $(this).closest('.post_id').val();
            $.ajax({
                url: url_str + "/comment_process",
                method:"post",
                data:$(this).parent().serialize(),
                success:function(response){
                    $('#all_posts').html(response);
                },
                error: console.error
            });
            $(this).parent().trigger('reset');
        }
    });

    
    $('.delete_post_form').submit(function(){
        url_str = $(this).find('.post_id').val();
        $.ajax({
            url: url_str + "/post_delete",
            method:"post",
            data:$(this).serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
        return false;
    });
    
    $('.delete_friend_form').submit(function(){
        url_str = $(this).find('.friend_id').val();
        $.ajax({
            url: '/' + url_str + "/friend/delete",
            method:"post",
            data:$(this).serialize(),
            success:function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        return false;
    });
    
    $('.delete_online_friend_form').submit(function(){
        url_str = $(this).find('.friend_id').val();
        $.ajax({
            url: '/' + url_str + "/friend_online/delete",
            method:"post",
            data:$(this).serialize(),
            success:function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        return false;
    });

    $('.delete_comment').click(function(){
        $.ajax({
            url:"delete_comment",
            method:"post",
            data:$(this).parent().serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
    });

    $('#display_all_posts').click(function(){
        url_str = $(this).next().val();
        $.ajax({
            url: url_str + "/display_all_posts",
            method:"post",
            data:$('#post').serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
        $('#display_my_posts').css('opacity', '0.5');
        $('#display_all_posts').css("opacity", "1");
        $('.line_all_posts').css('width', '100%')
        $('.line_my_posts').css('width', '30%')
    });

    $('#display_my_posts').click(function(){
        url_str = $(this).next().val();
        $.ajax({
            url: url_str + "/display_my_posts",
            method:"post",
            data:$('#post').serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
        $('#display_my_posts').css('opacity','1');
        $('#display_all_posts').css('opacity',  "0.5");
        $('.line_all_posts').css('width', '30%')
        $('.line_my_posts').css('width', '100%')
    });

    $('#display_friends').click(function(){
        url_str = $(this).next().val();
        $.ajax({
            url: '/' + url_str + "/friends_process",
            method:"get",
            success:function(response){
                $('#friends_container').html(response);
            },
            error: console.error
            
        });
        $('#display_online_friends').css('opacity', '0.5');
        $('#display_friends').css("opacity", "1");
        $('#display_not_friends').css("opacity", "0.5");
        $('.line_friends').css('width', '100%')
        $('.line_online_friends').css('width', '30%')
        $('.line_all_users').css('width', '30%')
    });

    $('#display_online_friends').click(function(){
        url_str = $(this).next().val();
        $.ajax({
            url: '/'+ url_str + "/friends_online",
            method:"get",
            success:function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        $('#display_online_friends').css('opacity', '1');
        $('#display_friends').css("opacity", "0.5");
        $('#display_not_friends').css("opacity", "0.5");
        $('.line_friends').css('width', '30%')
        $('.line_online_friends').css('width', '100%')
        $('.line_all_users').css('width', '30%')
    });

    $('#display_not_friends').click(function(){
        url_str = $(this).next().val();
        $.ajax({
            url: '/' + url_str + "/friends_others",
            method:"get",
            success:function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        $('#display_online_friends').css('opacity', '0.5');
        $('#display_friends').css("opacity", "0.5");
        $('#display_not_friends').css("opacity", "1");
        $('.line_friends').css('width', '30%')
        $('.line_online_friends').css('width', '30%')
        $('.line_all_users').css('width', '100%')
    });

    $('.add_friend_form').submit(function(){
        url_str = $(this).find('.friend_id').val();
        $.ajax({
            url: '/add_to_friend/' + url_str,
            method:"get",
            data:$(this).serialize(),
            success:function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        return false;
    });

    $('.like_post').click(function(){
        $.ajax({
            url:"like_post",
            method:"post",
            data:$(this).parent().serialize(),
            success:function(response){
                $('#all_posts').html(response);
            },
            error: console.error
        });
        $(this).toggleClass("opacity_1");
    });
    
    $('#upload_new_group_pic').click(function(){
        const input_group = document.getElementById('fileToUploadGroup');
        function onChange() {
            input_group.removeEventListener('change', onChange);
            $.ajax({
                url: 'group_pic',
                type: 'POST',
                data: new FormData($('#group_pic_form')[0]),
                cache: false,
                contentType: false,
                processData: false,
                success: function(response){
                    $('#group_photo').css("backgroundImage" , "url(" + response['url'] + ")");
                },
                error: console.error
              });
        }
        input_group.addEventListener('change', onChange);
        input_group.click();
    });

    $('#upload_new_profile_pic').click(function(){
        const input = document.getElementById('fileToUpload');
        function onChange() {
            input.removeEventListener('change', onChange);
            $.ajax({
                url: '/profile_pic',
                type: 'POST',
                data: new FormData($('#profile_pic_form')[0]),
                cache: false,
                contentType: false,
                processData: false,
                success: function(response){
                    $('#main_photo_img').css("backgroundImage" , "url(" + response['url'] + ")");
                },
                error: console.error
              });
        }
        input.addEventListener('change', onChange);
        input.click();
    });

    

    $('#online_friends').click(function(){
        url_str = $(this).next('.user_id').val();
        document.getElementById('display_all_friends').click(function(){
            document.getElementById('display_online_friends').click();
        });
     
    });

    $('.edit_ico').click(function(){
        $(this).next().focus();
    });

    $('.message_to_friend').click(function(){
        $.ajax({
            url: 'send_messages',
            method: "POST",
            data:$(this).serialize(),
            success: function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        return false;
    });

    $('.send_mess').click(function(){
        $.ajax({
            url: 'new_message',
            method: "POST",
            data:$(this).parent().serialize(),
            success: function(response){
                $('#friends_container').html(response);
            },
            error: console.error
        });
        return false;
    });

    function checkNewMessages (){
        $.ajax({
            url: '/check_new_message',
            method: "GET",
            data:{},
            success: function(response){
                if (response['new_mess'] > 0 ){
                    $('#my_mess').html('My Messages (' + response['new_mess'] + ')')
                }
            },
            error: console.error
        });
        setTimeout(checkNewMessages, 5000);
    };
    checkNewMessages();

    $('.group_title').keypress(function(e){
        if (e.which == 13){
            e.preventDefault();
            $.ajax({
                url: 'update_title',
                method: "POST",
                data:$('#create_group_form').serialize(),
                success: function(response){
                    
                },
                error: console.error
            });
            $(this).blur();
        }
    });

    $('.group_title').focusout(function(){
        $.ajax({
            url: 'update_title',
            method: "POST",
            data:$('#create_group_form').serialize(),
            success: function(response){
                
            },
            error: console.error
        });
        $(this).blur();
    });

    $('.group_desc').keypress(function(e){
        if (e.which == 13){
            e.preventDefault();
            $.ajax({
                url: 'update_desc',
                method: "POST",
                data:$('#create_group_form').serialize(),
                success: function(response){
                    
                },
                error: console.error
            });
            $(this).blur();
        }
    });

    $('.group_desc').focusout(function(){ 
        $.ajax({
            url: 'update_desc',
            method: "POST",
            data:$('#create_group_form').serialize(),
            success: function(response){
                
            },
            error: console.error
        });
        $(this).blur();
    });

    $('#display_my_groups').click(function(){
        $.ajax({
            url: "my_groups",
            method:"get",
            success:function(response){
                $('#group_container').html(response);
            },
            error: console.error
        });
        $('#display_my_groups').css("opacity", "1");
        $('#display_admin_groups').css('opacity', '0.5');
        $('#display_all_groups').css("opacity", "0.5");
        $('.line_groups').css('width', '100%')
        $('.line_admin_groups').css('width', '30%')
        $('.line_all_groups').css('width', '30%')
    });

    $('#display_admin_groups').click(function(){
        $.ajax({
            url: "admin_groups",
            method:"get",
            success:function(response){
                $('#group_container').html(response);
            },
            error: console.error
        });
        $('#display_my_groups').css("opacity", "0.5");
        $('#display_admin_groups').css('opacity', '1');
        $('#display_all_groups').css("opacity", "0.5");
        $('.line_groups').css('width', '30%')
        $('.line_admin_groups').css('width', '100%')
        $('.line_all_groups').css('width', '30%')
    });

    $('#display_all_groups').click(function(){
        $.ajax({
            url: "other_groups",
            method:"get",
            success:function(response){
                $('#group_container').html(response);
            },
            error: console.error
        });
        $('#display_my_groups').css("opacity", "0.5");
        $('#display_admin_groups').css('opacity', '0.5');
        $('#display_all_groups').css("opacity", "1");
        $('.line_groups').css('width', '30%')
        $('.line_admin_groups').css('width', '30%')
        $('.line_all_groups').css('width', '100%')
    });

    $('.delete_group').click(function(){
        url_str = $(this).prev().val();
        $.ajax({
            url: "/" + url_str + "/delete_group",
            method:"get",
            success:function(response){
                $('#group_container').html(response);
            },
            error: console.error
        });
    });

    $('.follow_button').click(function(){
        group_id = $(this).prev().prev().val();
        user_id = $(this).prev().val();
        $.ajax({
            url: "/" + user_id + "/follow_group/" + group_id,
            method:"get",
            success:function(response){
                $('#group_container').html(response);
            },
            error: console.error
        });
    });

    $('.unfollow_button').click(function(){
        group_id = $(this).prev().prev().val();
        user_id = $(this).prev().val();
        $.ajax({
            url: "/" + user_id + "/unfollow_group/" + group_id,
            method:"get",
            success:function(response){
                $('#group_container').html(response);
            },
            error: console.error
        });
    });

    $('#my_pic_div').click(function(e){
        const input_group = document.getElementById('myFileToUpload');
        function onChange() {
            input_group.removeEventListener('change', onChange);
            $.ajax({
                url: 'my_pic',
                type: 'POST',
                data: new FormData($('#my_pic_form')[0]),
                cache: false,
                contentType: false,
                processData: false,
                success: function(response){
                    $('#all_pics').html(response);
                },
                error: console.error
              });
        }
        input_group.addEventListener('change', onChange);
        input_group.click();
    });

    $('#upload_more_pic').click(function(e){
        const input_group = document.getElementById('moreFileToUpload');
        function onChange() {
            input_group.removeEventListener('change', onChange);
            $.ajax({
                url: 'more_pic_upload',
                type: 'POST',
                data: new FormData($('#more_pic_form')[0]),
                cache: false,
                contentType: false,
                processData: false,
                success: function(response){
                    $('#display_pics').html(response);
                },
                error: console.error
              });
        }
        input_group.addEventListener('change', onChange);
        input_group.click();
    });

    $('.delete_pic').click(function(){
        pic_id = $(this).next().val();
        $.ajax({
            url: "delete_pic/" + pic_id,
            method:"get",
            success:function(response){
                $('#display_pics').html(response);
            },
            error: console.error
        });
    });
});