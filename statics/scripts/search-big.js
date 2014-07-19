jQuery(function(){
	options = { serviceUrl:'/auto-complete-big/' };
	a = $('#q').autocomplete(options);
});

    /*function GoSearch(){

        if($("#q").val()!="") {


          document.getElementById("search-form").action  = "/search/?q=" + $("#q").val() + "";
          $("#search-form").submit();
        };

}*/