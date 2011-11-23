/*
    Replace black-space and @
*/
$(function(){
    var $id_twitter=$('input#id_twitter');
    var regex=/(\@|\s)/gi;
    $id_twitter.keypress(function() {
        if ($id_twitter.val().match(regex)){
            //alert($id_twitter.val());
            $(this).val(function(i,val) {
                return val.replace(regex,'');
            });
        }    
    });
});
$(function() {
   $('input#id_twitter').marcoPolo({
     data: {
       apikey: 'api_test-W1cipwpcdu9Cbd9pmm8D4Cjc469',
     },
     formatData: function (data) {
       return data.results.slice(0, 20);
     },
     formatItem: function (data, $item) {
       return data.screen_name;
     },
     onSelect: function (data, $item) {
     this.val(data.screen_name);
     }
   });
});

/*
    Check if twitter exists
*/
$(function(){
    var $id_twitter=$('input#id_twitter');
    $id_twitter.focusout(function() {
        $.ajax({
            url:'http://twitter.com/'+$id_twitter.val()+'/',
            type:'HEAD',
            error: function(){
                $id_twitter.css({'border-style':'solid','border-width':'1px','border-color':'#FF6666'});
            },
        });
    });
});
