# /*****************************************************************************
#  * Pesquisar pontos
#  *
#  * 2012 Twitnerario
#  *****************************************************************************/
jQuery.noConflict()(($) ->
    $('form#searchform').submit (e) ->
        e.preventDefault()
        s = $(@).find("input[name='s']").val()
        if s.length
            window.location.replace("?s=#{ encodeURIComponent(s) }")
)