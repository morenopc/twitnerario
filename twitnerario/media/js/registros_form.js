/*
    Replace black-space and @
*/
jQuery(function(){
    var $id_twitter=jQuery('input#id_twitter');
    var regex=/(\@|\s)/gi;
    $id_twitter.keypress(function() {
        if ($id_twitter.val().match(regex)){
            //alert($id_twitter.val());
            jQuery(this).val(function(i,val) {
                return val.replace(regex,'');
            });
        }    
    });
});
