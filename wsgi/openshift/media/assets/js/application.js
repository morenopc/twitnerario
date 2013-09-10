/***************************************************
      Responsive Menu
***************************************************/

jQuery.noConflict()(function($){
      "use strict";
      // Create the dropdown base
      $("<select />").appendTo("#nav-main");
      
      // Create default option "Go to..."
      $("<option />", {
         "selected": "selected",
         "value"   : "",
         "text"    : "Escolha a página"
      }).appendTo("#nav-main select");
      
      // Populate dropdown with menu items
      $("#nav-main a").each(function() {
       var el = $(this);
       $("<option />", {
           "value"   : el.attr("href"),
           "text"    : el.text()
       }).appendTo("#nav-main select");
      });
      
     // To make dropdown actually work
     // To make more unobtrusive: http://css-tricks.com/4064-unobtrusive-page-changer/
      $("#nav-main select").change(function() {
        window.location = $(this).find("option:selected").val();
      });
   
});

/***************************************************
      As the page loads, cal these scripts
***************************************************/

jQuery(document).ready(function ($) {
  "use strict";
  $('.accordion-group .accordion-toggle').click(function() {
      var parent = $(this).parents('.accordion-group');
      parent.siblings().removeClass('active').find('.accordion-body').stop(true,true).hide(300);
      if(!parent.hasClass('active')) {
        parent.addClass('active').find('.accordion-body').stop(true,true).fadeIn(400);
      } else { 
        parent.removeClass('active').find('.accordion-body').stop(true,true).hide(200);
      }
    });

  // responsive videos with fitvids
  $('.fitvids').fitVids();
  
}); /* end of as page load scripts */

  
/***************************************************
      Autocomplete Search
***************************************************/

// Load countries then initialize plugin:
jQuery.ajax({
    url: '/media/content/countries.txt',
    dataType: 'json'
}).done(function (source) {

    var countriesArray = jQuery.map(source, function (value, key) { return { value: value, data: key }; }),
        countries = jQuery.map(source, function (value) { return value; });

    // Initialize autocomplete with custom appendTo:
    jQuery('#autocomplete-dynamic').autocomplete({
        lookup: countriesArray
    });
    
});

