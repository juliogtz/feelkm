$(function() {
 var STATUS_MENU_TOP_USER=0;

    /* Search forms submits */

    $('form').each(function() {

        $(this).find('input').keypress(function(e) {
            // Enter pressed?
            if(e.which == 10 || e.which == 13) {

                if(this.form.id=="search-form-top"){

                  this.form.action="/search/?q="+$("#inputSearchHi").val()+"";
                }

                if(this.form.id=="search-form"){

                  this.form.action="/search/?q="+$("#q").val()+"";
                }

                this.form.submit();


            }
        });


    });


    /* Click links header Register - Login  */

     $( "#link-register" ).click(function() {

        $( "#box-access" ).fadeIn( "slow" );

        $( "#box-register" ).fadeIn( "slow" );
    });

      $( "#link-login" ).click(function() {

        $( "#box-access" ).fadeIn( "slow" );

        $( "#box-login-form" ).fadeIn( "slow" );
    });


    /* Click on login box- btn Facebook */


    $('#btn-register-facebook-3').hover(function() {

        $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-login-hover-facebook.png');

    }, function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-login-facebook.png');
    });


    /* Click login btn normal */



      $('#btn-login-normal-img').hover(function() {

        $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-login-hover.png');

    }, function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-login.png');

    });



    /* Click on register box - btn Facebook  */

    $('#btn-register-facebook').hover(function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook-hover.png');

    }, function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook.png');
    });


    $('#btn-register-facebook-2').hover(function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook-hover.png');

    }, function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook.png');

    });



    $( "#btn-register-facebook" ).click(function() {

         $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook-on.png');




    });


    /* Click on register box - btn link register with email  */

   $( "#sub-title-register-link" ).click(function() {

         $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook-on.png');

         $( "#box-register" ).fadeOut( "fast", function(){

             $( "#box-register-form" ).fadeIn( "slow" );

         document.getElementById("btn-register-facebook-form-r").style.display="";
         document.getElementById("line-form-register-aux").style.display="";
         document.getElementById("box-register-form").style.height="620px";

         } );

    });

    /* Click on register box - btn link register with normal  */

      $('#btn-register-normal-img').hover(function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-hover.png');

    }, function() {

      $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register.png');
    });


    /* Click login with email and password */

    $("#link-open-login-from-register").click(function(){

        $( "#box-register" ).fadeOut( "fast", function(){

             $( "#box-register-form" ).fadeOut( "fast",function(){

                 $( "#box-login-form" ).fadeIn("slow");

             });

         } );


    });




    $("#form-register-footer-link").click(function(){

        $("#box-register-form" ).fadeOut( "fast", function(){

             $( "#box-register" ).fadeOut( "fast",function(){

                 $( "#box-login-form" ).fadeIn("slow");

             });

         });


    });

    $("#txt-send-reovery-link").click(function() {


        $("#box-recovery-form-wait-su" ).fadeOut( "fast", function(){


                 $( "#box-login-form" ).fadeIn("slow");

         });

    });


    $("#footer-txt-login-link").click(function(){

        $("#box-login-form" ).fadeOut( "fast", function(){

             $( "#box-register" ).fadeOut( "fast",function(){

                 $( "#box-register-form" ).fadeIn("slow");

             });

         });


    });


   $("#recovery-password-link").click(function(){

        $("#box-login-form" ).fadeOut( "fast");
        $("#box-register" ).fadeOut( "fast");
        $("#box-register-form" ).fadeOut( "fast");
        $("#box-recovery-password" ).fadeIn( "slow");


    });


    /* Keyboard esc and close all forms login-register */
     $(document).keyup(function(event){
        if(event.which==27)
        {

            $("#box-login-form" ).fadeOut( "fast");
            $("#box-register" ).fadeOut( "fast");
            $("#box-register-form" ).fadeOut( "fast");
            $("#box-recovery-password" ).fadeOut( "fast");
            $("#box-access" ).fadeOut( "slow");

            document.getElementById("name_user").value="";
            document.getElementById("last_user").value="";
            document.getElementById("email_user").value="";
            document.getElementById("id_facebook").value="";
            document.getElementById("email_facebook").value="";

            document.getElementById("email_user_recovery").value="";
            document.getElementById("user_user_login").value="";
            document.getElementById("password_user_login").value="";

            //Close Menu

            if(STATUS_MENU_TOP_USER==1){

                MenuTopUser();
            }




        }});


function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }


 function csrfSafeMethod(method) {
                            // these HTTP methods do not require CSRF protection
                            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                        }



 $( "#btn-register-normal-img" ).click(function() {

      $("#box-register-form").fadeOut("fast");
      $("#box-register-form-wait").fadeIn( "fast");



         //$(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-on.png');

        /* Remove Class validation */

        $("#user_user").removeClass("input-text-color-alert" );
        $("#name_user").removeClass("input-text-color-alert" );
        $("#last_user").removeClass("input-text-color-alert" );
        $("#email_user").removeClass("input-text-color-alert" );
        $("#password_user").removeClass("input-text-color-alert" );

            var csrftoken = getCookie('csrftoken');
            var csrftoken2 = getCookie('csrftoken');



                        $.ajaxSetup({
                             beforeSend: function(xhr, settings) {

                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }

                        });

         $.ajax({
             type: "POST", url: "/register-new-user/",
             success:function(){




      $("#box-register-form-wait").fadeOut("fast");
      $("#box-register-form").fadeIn( "fast");

             },

             error:function(){


                  $("#txt-alert-box" ).html("¿Esta usted seguro que esta conectado a internet?");
                  $("#box-register-form-wait").fadeOut("fast");
                   $("#box-register-form").fadeIn( "fast");

             },

             statusCode: {
                        404: function() {
                  $("#txt-alert-box" ).html("¿Esta usted seguro que esta conectado a internet?");
                  $("#box-register-form-wait").fadeOut("fast");
                   $("#box-register-form").fadeIn( "fast");


              }
             },


             data: {
                    user_user: $("#user_user").val(),
                     name_user: $("#name_user").val(),
                     last_user: $("#last_user").val(),
                     email_user: $("#email_user").val(),
                     password_user:$("#password_user").val(),
                     id_facebook:$("#id_facebook").val(),
                     email_facebook:$("#email_facebook").val(),
                     firtsFacebookPic:$("#firtsFacebookPic").val()

                    }

         }) .done(function( msg ) {




            // alert(msg);

            if(msg=="1"){

                 $("#txt-alert-box" ).html("");
                 window.location.href = document.URL;
             }

             if(msg=="0"){
                 //alert("Someone is using the user.")

                 $("#txt-alert-box" ).html("El nombre usuario ya esta en uso, intente otro.");
                 $("#user_user").addClass("input-text-color-alert");

             }

              if(msg=="-1"){
                 //alert("Problems with creating new user")

                 $("#txt-alert-box" ).html("Error de conexión, vuelva a intentar.");
                 $("#user_user").addClass("input-text-color-alert");
             }

              if(msg=="-2"){


                 $("#txt-alert-box" ).html("El usuario fue creado, reinicie la página.");
                 $("#user_user").addClass("input-text-color-alert");
             }

               if(msg=="-3"){

                 $("#txt-alert-box" ).html("No se permiten campos vacios.");

                   if(document.getElementById("user_user").value==""){

                    $("#user_user").addClass("input-text-color-alert");

                    }


                   if(document.getElementById("name_user").value==""){

                    $("#name_user").addClass("input-text-color-alert");

                    }


                   if(document.getElementById("last_user").value==""){

                    $("#last_user").addClass("input-text-color-alert");

                    }

                   if(document.getElementById("email_user").value==""){

                    $("#email_user").addClass("input-text-color-alert");

                    }


                   if(document.getElementById("password_user").value==""){

                    $("#password_user").addClass("input-text-color-alert");

                    }


             }



             if(msg=="-5"){
                 $("#txt-alert-box" ).html("El mail ya esta en uso, intente con otro.");
                 $("#email_user").addClass("input-text-color-alert");
             }

         });



    });



     $( "#btn-login-normal-img" ).click(function() {

         //$(this).attr('src', '/{{ STATIC_URL }}imgs/btn-login-on.png');

          $("#box-login-form").fadeOut("fast");
          $("#box-login-form-wait").fadeIn( "fast");


         $("#user_user_login").removeClass("input-text-color-alert");
         $("#password_user_login").removeClass("input-text-color-alert");


         function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

            var csrftoken = getCookie('csrftoken');
            var csrftoken2 = getCookie('csrftoken');

                        function csrfSafeMethod(method) {
                            // these HTTP methods do not require CSRF protection
                            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
                        }

                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
});


         $.ajax({
             type: "POST", url: "/login/",
             data: {
                     user_user: $("#user_user_login").val(),
                     password_user:$("#password_user_login").val()

                    }

         }) .done(function( msg ) {


            if(msg=="1"){

                 window.location.href = document.URL;
             }

             if(msg=="0"){
                 //alert("Error login")

                  $("#txt-alert-box-login" ).html("Error, intente otra vez.");t
                  $("#box-login-form-wait").fadeOut("fast");
                  $("#box-login-form").fadeIn( "fast");
             }


              if(msg=="-4"){

                 $("#txt-alert-box-login" ).html("El usuario no existe.");
                 $("#box-login-form-wait").fadeOut("fast");
                 $("#box-login-form").fadeIn( "fast");

                 $("#user_user_login").addClass("input-text-color-alert");

             }

               if(msg=="-3"){
                // alert("Empty fields")



                  $("#txt-alert-box-login" ).html("No se permiten campos vacios.");
                  $("#box-login-form-wait").fadeOut("fast");
                  $("#box-login-form").fadeIn( "fast");





                   if(document.getElementById("user_user_login").value==""){

                       $("#user_user_login").addClass("input-text-color-alert");


                   }

                     if(document.getElementById("password_user_login").value==""){

                       $("#password_user_login").addClass("input-text-color-alert");

                   }






             }



         });

    });


    $( "#btn-recovery-password" ).click(function() {

         //$(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-on.png');

          $("#box-recovery-password").fadeOut("fast");
          $("#box-recovery-form-wait").fadeIn( "fast");


         $("#email_user_recovery").removeClass("input-text-color-alert");


         function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

            var csrftoken = getCookie('csrftoken');
            var csrftoken2 = getCookie('csrftoken');



                        $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
});


         $.ajax({
             type: "POST", url: "/recovery/",
             data: {
                     email_user: $("#email_user_recovery").val()


                    }

         }) .done(function( msg ) {


            if(msg=="1")
            {

                 //alert("mensaje enviado");
                  $("#box-recovery-form-wait").fadeOut("fast");
                  $("#box-recovery-form-wait-su").fadeIn( "fast");
                  $("#email_user_recovery").removeClass("input-text-color-alert");

            }


             if(msg=="0")
             {
                 //alert("Correo electronico no existe.")

                 $("#txt-alert-box-recovery").html("El correo electrónico no existe.");

                 $("#box-recovery-form-wait").fadeOut("fast");
                 $("#box-recovery-password").fadeIn("fast");

                 $("#email_user_recovery").addClass("input-text-color-alert");

             }





         });

    });

     function testAPI() {
    console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      console.log('Successful login for: ' + response.name);
      alert("gracias por logearte");
    });
  }


    /* ------------------------------------ Facebook Operations JS -------------------------------------- */

    $("#btn-register-facebook").click(function(){

            Register_Facebook();
    });





    $("#btn-register-facebook-2").click(function(){



       $("#box-register").fadeOut("fast");
       $("#box-register-form").fadeOut("fast");


       Register_Facebook();

    });

     $("#btn-register-facebook-3").click(function(){

       $(this).attr('src', '/{{ STATIC_URL }}imgs/btn-register-facebook-on.png');

       $("#box-register").fadeOut("fast");
       $("#box-register-form").fadeOut("fast");
       $("#box-login-form").fadeOut("fast");


       Register_Facebook();

    });


    function Register_Facebook(){

            var dataRest="";

          FB.login(function(response){
            // Handle the response object, like in statusChangeCallback() in our demo
            // code.

            if (response.status === 'connected') {
              // Logged into your app and Facebook.
              // 1.- Validate if the user - if user( login -> ) no open form register.

                FB.api('/me', function(response) {
                  console.log('Successful login for: ' + response.name);

                    console.log(response);

                    //alert(response.id + " - "+ response.name + " - "+ response.email +" - "+ response.gender+" - "+response.userid+ " - "+
                    // response.last_name+ " - "+ response.first_name+ response.locale);

                    var csrftoken = getCookie('csrftoken');
                    $.ajaxSetup({
                            beforeSend: function(xhr, settings) {
                                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                                }
                            }
                                });

                     $.ajax({
                         type: "POST", url: "/facebook-register/",
                         data: {
                                 id_facebook: response.id,
                                 name_full: response.name,
                                 email: response.email,
                                 gender: response.gender,
                                 last_name: response.last_name,
                                 first_name: response.first_name,
                                 locale: response.locale

                               }}) .done(function( msg ) {





                                if(msg=="0") {

                                    $("#box-register").fadeOut("fast", function () {

                                        $("#box-register-form").fadeIn("slow", function () {

                                            /* Poner los valores en en el formulario */

                                            document.getElementById("btn-register-facebook-form-r").style.display="none";
                                            document.getElementById("line-form-register-aux").style.display="none";

                                            document.getElementById("box-register-form").style.height="580px";

                                            document.getElementById("name_user").value = response.first_name;
                                            document.getElementById("last_user").value = response.last_name;
                                            document.getElementById("email_user").value = response.email;
                                            document.getElementById("id_facebook").value = response.id;
                                            document.getElementById("email_facebook").value = response.email;
                                            document.getElementById("firtsFacebookPic").value = "https://graph.facebook.com/" + response.id + "/picture?width=200&height=200";

                                        });


                                    });

                                }

                                if(msg=="1")
                                {
                                         window.location.href = document.URL;

                                }

                                if(msg=="-1")
                                {
                                    alert("Hubo un problema, intentelo más tarde");
                                }



                             });
                        });


            } else if (response.status === 'not_authorized') {

                alert("Disculpa, pero no tienes autorización");

            } else {
              // The person is not logged into Facebook, so we're not sure if
              // they are logged into this app or not.

                alert("Necesitas iniciar sesión en Facebook para continuar.");
            }


        },{scope: 'public_profile,email,publish_stream,read_stream,user_about_me,user_photos'});

    }


    // Click on menu top user - just with login

    function MenuTopUser(){

        if(STATUS_MENU_TOP_USER==0){
           $("#menu-top-header-options").fadeIn("slow");
            STATUS_MENU_TOP_USER=1;
        }else{

             $("#menu-top-header-options").fadeOut("slow");
             STATUS_MENU_TOP_USER=0;

        }

    }

    $("#txt-header-name-user").click(function(){

        MenuTopUser();

    });


     $("#img-profile-header-yes-d").click(function(){

        MenuTopUser();
    });

    $("#img-profile-header-no-div").click(function(){

        MenuTopUser();
    });




    /*$(document).click(function(){

         if(STATUS_MENU_TOP_USER==1){

                MenuTopUser();
            }

    });*/







});