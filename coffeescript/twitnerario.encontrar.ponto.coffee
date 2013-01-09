# /*****************************************************************************
#  * jQuery for pesquisar.ponto.html file
#  *
#  * 2012 Twitnerario
#  *****************************************************************************/
jQuery ->
    make_search = ->
        key_search = $('#pesq_ponto').val()
        source = $('#pesq_resultado').html()
        $.getJSON '/localizar/'+key_search+'/', (pontos) =>
            results = pontos.data.length
            if results > 50
                results = 50
            for i in [0..results - 1] by 1
                obj = pontos.data[i]
                template = Handlebars.compile(source)
                context = {ponto: obj.ponto, lograd: obj.logradouro, bairro: obj.bairro, p_refer: obj.referencia}
                $('.lista_resultados').append(template(context))

    $('#pesq_button').bind 'click', (e) =>
        make_search()

    $("#pesq_ponto").bind 'keypress', (e) =>
        if e.which == 13
            e.preventDefault()
            make_search()

    $(".resultado").live 'click', (e) ->
        url = '/registro/' + $(this).attr('id')
        $(location).attr('href', url)

    return