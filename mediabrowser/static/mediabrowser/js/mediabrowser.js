MEDIABROWSER = {
    getURLParams: function(url) {
        var chunks, i, chunk;
        var m = url.match(/\?([^#]+)/);
        var params = {};
        
        if(!m || !m[1]) {
            return {};
        }
        chunks = m[1].split("&");
        for(i=0; i<chunks.length; i++) {
            chunk = chunks[i].split('=');
            if (chunk.length>1) {
                params[chunk[0]] = decodeURI(chunk[1]);
            } else if (chunk[0]) {
                params[chunk[0]] = "";
            }
        }
        return params;
    },
    
    insertFile: function(file_url) {
        var params = MEDIABROWSER.getURLParams(window.location.href);
        window.opener.CKEDITOR.tools.callFunction( params["CKEditorFuncNum"], file_url);
    }
};


$(function(){
    
    var reset_controls = function() {
        $("#InsertFile, #DeleteFile").removeClass("active").addClass("inactive");
    };
    
    // clicking on asset:
    $("#MediaBrowserContent").on("click", ".mb-selectable", function(){
        $("#MediaBrowserContent .active").removeClass("active");
        $(this).addClass("active");
        $("#InsertFile").removeClass("inactive").addClass("active");
        $("#DeleteFile").removeClass("inactive").addClass("active");
    });
    
    // clicking on insert file
    $("#InsertFile").click(function(event){
        event.preventDefault();
        event.bubbles = false;
        var url = $(".mb-selectable.active").attr("data-url");
        if (url) {
            MEDIABROWSER.insertFile(url);
            window.close();
        }
        
    });
    
    // TODO: click away
    $(document).bind('click', function(e) {
        if(!$(e.target).closest('.mb-selectable').length) {
            reset_controls();
            $(".mb-selectable.active").removeClass("active");
        }
    });
    
    // file upload
    $("#id_file").change(function(){
        if(this.value) {
            $(this).closest("form").submit();
        }
    });
    
    $("#UploadFile").click(function(event){
        event.preventDefault(); 
        $("#id_file").click();
    });
    
    
    // file deletion dialog
    $("#ConfirmDeleteDialog").dialog({
        modal: true,
        autoOpen: false
    });
    // clicking on delete file button
    $("#DeleteFile").click(function(event){
        event.preventDefault();
        var selected_file = $("div.mb-selectable.active");
        if(selected_file) {
            $("#FileIdToBeDeleted").val(selected_file.attr("data-id"));
            $("#FileToBeDeletedContent").text(selected_file.text());
            $("#ConfirmDeleteDialog").dialog("open");
        }
    });
    // clicking on ok to delete button
    $("#AssetDeletionForm").submit(function(event){
        event.preventDefault();
        var form = $(this);
        $.ajax(
            form.attr("action"),
            {
                data: form.serialize(),
                method: "POST",
                success: function(data) {
                    if(data.status == "ok") {
                        $("#File"+data.id).remove();
                        reset_controls();
                    } else {
                        alert(data.message);
                    }
                    $("#ConfirmDeleteDialog").dialog("close");
                }
            }
        );
    });
    
    $('.ui-dialog-cancel').click(function(){
        $(this).closest('.ui-dialog-content').dialog("close");
    });
    
    
    // search fields
    // FIXME: there can be may results; eventually this will be an ajax call
    $("#Search").keyup(function(event){
        var val = this.value.toLowerCase();
        $(".mb-selectable").each(function(){
            
        });
    });
    
    // set active link on top nav
    $("#MediaBrowserNavigation a").each(function(){
        if(this.pathname == location.pathname) {
            $(this).addClass("active");
        }
    });
    
    // activate tooltip
    $(function() {
        $( document ).tooltip();
    });

});