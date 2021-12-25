$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
    var actions = $("table td:last-child").html();
    // Append table with add row form on add new button click
    $(".add-new").click(function(){
        $(this).attr("disabled", "disabled");
        var index = $("table tbody tr:last-child").index();
        var row = '<tr>' +
            '<td><input type="text" class="form-control" name="image" id="txtimage"></td>' +
            '<td><input type="text" class="form-control" name="name" id="txtname"></td>' +
            '<td><input type="text" class="form-control" name="email" id="txtemail"></td>' +
            '<td><input type="text" class="form-control" name="phone" id="txtphone"></td>' +
            '<td><input type="text" class="form-control" name="password" id="txtpassword"></td>' +
            '<td><input type="text" class="form-control" name="type" id="txttype"></td>' +
            '<td>' + actions + '</td>' +
        '</tr>';
        $("table").append(row); 
        
        $("table tbody tr").eq(index + 1).find(".add, .edit, .delete").toggle();
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
        var txtimage = $("#txtimage").val();
        var txtname = $("#txtname").val();
        var txtemail = $("#txtemail").val();
        var txtphone = $("#txtphone").val();
        var txtpassword = $("#txtpassword").val();
        var txttype = $("#txttype").val();
        $.post("/ajax_add", { txtimage: txtimage, txtname: txtname, txtemail: txtemail, txtphone: txtphone, txtpassword: txtpassword, txttype: txttype}, function(data) {
            $("#displaymessage").html(data);
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
        $(this).parents("tr").remove();
        $(".add-new").removeAttr("disabled");
        var id = $(this).attr("id");
        var string = id;
        $.post("/ajax_delete", { string: string}, function(data) {
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
      
        var txtimage = $('#txtimage').val();
        var txtname = $('#txtname').val();
        var txtemail = $('#txtemail').val();
        var txtphone = $('#txtphone').val();
        var txtpassword = $('#txtpassword').val();
        var txttype =$('#txttype').val();
        var txtuid = $('#txtuid').val();
        var txtkey= $('#txtkey').val();

        $.post("/ajax_update", {  txtimage: txtimage, txtname: txtname, txtemail: txtemail, txtphone: txtphone, txtpassword: txtpassword, txttype: txttype, txtuid: txtuid, txtkey: txtkey}, function(data) {
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
                var idname = 'txtuid';
            }else if (i=='7'){
                var idname = 'txtkey';
            }
            else{} 
            $(this).html('<input type="text" name="updaterec" id="' + idname + '" class="form-control" value="' + $(this).text() + '">');
        });  
        $(this).parents("tr").find(".add, .edit").toggle();
        $(".add-new").attr("disabled", "disabled");
        $(this).parents("tr").find(".add").removeClass("add").addClass("update"); 
    });

    
});