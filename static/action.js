
$(document).ready(function(){

    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tbody tr").filter(function() {
            if( typeof value != "string"){
                value = value.toString();
            }
          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });


    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    // Append table with add row form on add new button click
    $(".add-new").click(function(){
        $(this).attr("disabled", "disabled");
        var index = $("table tbody tr:first-child").index();
        var row = '<tr>' +
            '<td><img height="60" src="../static/image/anonymous.png" alt="Costumer image"></td> ' +
            '<td><input type="text" class="form-control" name="name" id="txtname"></td>' +
            '<td><input type="text" class="form-control" name="email" id="txtemail"></td>' +
            '<td><input type="text" class="form-control" name="phone" id="txtphone"></td>' +
            '<td class="hidetext"><input type="text" class="form-control" name="password" id="txtpassword"></td>' +
            '<td><input type="text" class="form-control" name="type" id="txttype"></td>' +
            '<td></td>' +
            '<td>' + actions + '</td>' +
        '</tr>';
        $("table").prepend(row); 
        
        $("table tbody tr").eq(index).find(".add, .edit, .delete").toggle();
        $('[data-toggle="tooltip"]').tooltip();
 
    });
   


    // Add row on add button click
    $(document).on("click", ".add", function(){
        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');

        input.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                empty = true;
            } else{
                $(this).removeClass("error");
            }
        });

        var txtname = $("#txtname").val();
        var txtemail = $("#txtemail").val();
        var txtphone = $("#txtphone").val();
        var txtpassword = $("#txtpassword").val();
        var txttype = $("#txttype").val();
        $.post("/ajax_add", {txtname: txtname, txtemail: txtemail, txtphone: txtphone, txtpassword: txtpassword, txttype: txttype}, function(data) {
            
            var message = data.split(",");
            $("table tbody tr:first-child").attr('id', message[1]);
            $("#displaymessage").html(message[0]);
            $("#displaymessage").show();
        });

        $(this).parents("tr").find(".error").first().focus();
        if(!empty){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });   
            $(this).parents("tr").find(".add, .edit, .delete").toggle();
            $(".add-new").removeAttr("disabled");
        } 
    }); 
    // Delete row on delete button click
    $(document).on("click", ".delete", function(){
       

        var currentRow=$(this).parents("tr").attr("id");
        $(this).parents("tr").remove();

        $.post("/ajax_delete", {userKey: currentRow}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
        
    });
    // update rec row on edit button click
    $(document).on("click", ".update", function(){

        var empty = false;
        var input = $(this).parents("tr").find('input[type="text"]');

        input.each(function(){
            if(!$(this).val()){
                $(this).addClass("error");
                empty = true;
            } else{
                $(this).removeClass("error");
            }
        });

        var currentRow=$(this).closest("tr"); 
        
        var txtname = $('#txtname').val();
        var txtemail = $('#txtemail').val();
        var txtphone = $('#txtphone').val();
        var txtpassword = $('#txtpassword').val();
        var txttype = $('#txttype').val();
        var currentRow=$(this).parents("tr").attr("id");

      

        $.post("/ajax_update", {txtname: txtname, txtemail: txtemail, txtphone: txtphone, txtpassword: txtpassword, txttype: txttype, txtkey: currentRow}, function(data) {
            $("#displaymessage").html(data);
            $("#displaymessage").show();
        });
        $(this).parents("tr").find(".update").removeClass("update").addClass("add");
        $(this).parents("tr").find(".error").first().focus();

        if(!empty){
            input.each(function(){
                $(this).parent("td").html($(this).val());
            });   
          
            $(this).parents("tr").find(".add, .edit").toggle();
            $(".add-new").removeAttr("disabled");
        }
      
    });
 
    // Edit row on edit button click
    $(document).on("click", ".edit", function(){  
        $(this).parents("tr").find("td:not(:last-child)").each(function(i){
            if (i=='0'){
                var idname = 'txtimage';
            }else if (i=='1'){
                var idname = 'txtname';
            }else if (i=='2'){
                var idname = 'txtemail';
            }else if (i=='3'){
                var idname = 'txtphone';
            }else if (i=='4'){
                var idname = 'txtpassword';
            }else if (i=='5'){
                var idname = 'txttype';
            }else if (i=='6'){
                var idname = 'txtwallet';
            }else if (i=='7'){
                var idname = 'txtkey';
            }
            else{}

            if(i == '0' || i == '6' || i == '7'){


            }else if(i == '5'){
                $(this).html('<input type="text" name="updaterec" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
            }
            else{
             $(this).html('<input type="text" name="updaterec" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
            }

        });  
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
        $(this).parents("tr").find(".add").removeClass("add").addClass("update"); 
    });

    $(document).on("click", ".imageUpload", function(){
       
        $(this).css( "display", "none" );
        $(this).siblings().css( "display", "" );
        $(this).siblings().children("div").children("div").children("input").attr('id', 'files');
        $(this).siblings().children("div").children("div").children("label").attr('for', 'files');
        $(this).siblings().children("div").children("div").children("div").children(".cancelUpload").siblings().attr('id', 'send');
        $(this).siblings().children("div").children("div").siblings().children("p").attr('id', 'uploading');
        $(this).siblings().children("div").children("div").siblings().children("progress").attr('id', 'progress');

    });
    $(document).on("click", ".cancelUpload", function(){
       
        $(this).parent().parent().parent().parent(".imageInput").siblings().css( "display", "" );
        $(this).parent().parent().parent().parent(".imageInput").css( "display", "none" );
        $(this).parent().siblings("input").attr('id', 'filetemp');
        $(this).parent().siblings("label").attr('for', 'filetemp');
        $(this).siblings().attr('id', '');
        $(this).parent().parent().siblings().children("p").attr('id', '');
        $(this).parent().parent().siblings().children("progress").attr('id', '');


    });
  
   

    
});



