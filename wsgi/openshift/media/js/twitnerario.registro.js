/*****************************************************************************
 * jQuery for registro.html file
 *
 * 2012 Twitnerario
 *****************************************************************************/
 (function( jQuery ) {
  jQuery.widget( "ui.combobox", {
    _create: function() {
      var input,
        self = this,
        select = this.element.hide(),
        selected = select.children( ":selected" ),
        value = selected.val() ? selected.text() : "",
        wrapper = this.wrapper = jQuery( "<span>" )
          .addClass( "ui-combobox" )
          .insertAfter( select );

      input = jQuery( "<input>" )
        .appendTo( wrapper )
        .val( value )
        .addClass( "ui-state-default ui-combobox-input" )
        .autocomplete({
          delay: 0,
          minLength: 0,
          source: function( request, response ) {
            var matcher = new RegExp( jQuery.ui.autocomplete.escapeRegex(request.term), "i" );
            response( select.children( "option" ).map(function() {
              var text = jQuery( this ).text();
              if ( this.value && ( !request.term || matcher.test(text) ) )
                return {
                  label: text.replace(
                    new RegExp(
                      "(?![^&;]+;)(?!<[^<>]*)(" +
                      jQuery.ui.autocomplete.escapeRegex(request.term) +
                      ")(?![^<>]*>)(?![^&;]+;)", "gi"
                    ), "<strong>$1</strong>" ),
                  value: text,
                  option: this
                };
            }) );
          },
          select: function( event, ui ) {
            ui.item.option.selected = true;
            self._trigger( "selected", event, {
              item: ui.item.option
            });
          },
          change: function( event, ui ) {
            if ( !ui.item ) {
              var matcher = new RegExp( "^" + jQuery.ui.autocomplete.escapeRegex( jQuery(this).val() ) + "$", "i" ),
                valid = false;
              select.children( "option" ).each(function() {
                if ( jQuery( this ).text().match( matcher ) ) {
                  this.selected = valid = true;
                  return false;
                }
              });
              if ( !valid ) {
                // remove invalid value, as it didn't match anything
                jQuery( this ).val( "" );
                select.val( "" );
                input.data( "autocomplete" ).term = "";
                return false;
              }
            }
          }
        })
        .addClass( "ui-widget ui-widget-content ui-corner-left" );

      input.data( "autocomplete" )._renderItem = function( ul, item ) {
        return jQuery( "<li></li>" )
          .data( "item.autocomplete", item )
          .append( "<a>" + item.label + "</a>" )
          .appendTo( ul );
      };

      jQuery( "<a>" )
        .attr( "tabIndex", -1 )
        .attr( "title", "Show All Items" )
        .appendTo( wrapper )
        .button({
          icons: {
            primary: "ui-icon-triangle-1-s"
          },
          text: false
        })
        .removeClass( "ui-corner-all" )
        .addClass( "ui-corner-right ui-combobox-toggle" )
        .click(function() {
          // close if already visible
          if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
            input.autocomplete( "close" );
            return;
          }

          // work around a bug (likely same cause as #5265)
          jQuery( this ).blur();

          // pass empty string as value to search for, displaying all results
          input.autocomplete( "search", "" );
          input.focus();
        });
    },

    destroy: function() {
      this.wrapper.remove();
      this.element.show();
      jQuery.Widget.prototype.destroy.call( this );
    }
  });
})( jQuery );