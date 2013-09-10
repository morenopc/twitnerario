###########################################################################
###
    Serialize Anything - MasterGED
    (c) 2013 Moreno Cunha, Domob / MasterVig
###########################################################################
jQuery::values = (data) ->
    inps = jQuery(@).find(":input").get()
    if typeof data isnt "object"
        # return all data
        data = {}
        jQuery.each inps, () ->
            if @.name and (
                @.checked or /select|textarea/i.test(@.nodeName)\
                or /text|hidden|password/i.test(@.type))
                data[@.name] = jQuery(@).val()
        return data
    else
        jQuery.each inps, () ->
            if @.name and data[@.name]
                if @.type is "checkbox" or @.type is "radio"
                    jQuery(@).prop("checked", (data[@.name] is jQuery(@).val()))
                else
                    jQuery(@).val(data[@.name])
            else if @.type is "checkbox"
                jQuery(@).prop("checked", false)
        return jQuery(@)
