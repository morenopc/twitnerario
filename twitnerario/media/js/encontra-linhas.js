var pontosJSON;
var linhas_option_num_regex=/([0-9]{1,4}[a-z]{0,2})/gi;// regx filtro para linhas val
var $id_ponto=$('#id_ponto');
var $id_info=$('#info');
var $id_linha=$('#id_linha');
var $id_linha_opt=$("#id_linha option");
var ponto_info_tyle='<p class="ponto_erro_info" id="info"style="display:none;color:#404040;font-size: 13px;padding-top: 4px;margin-bottom: 0px;">';
var ponto_n_encontrado='&ensp;&uarr; Ponto vazio ou não encontrado. Tente novamente (^-^\')';
/*
    Obtem lista JSON de pontos - pontosJSON
*/
$.getJSON('/media/json/listaPontos.json', function(data){
    pontosJSON=data;
    //$.each(data.data, function(i,v) { pts[pts.length]=v.ponto; }); lista de pontos disponiveis
});
/*
    Ponto erro informacao
*/
function ponto_erro_info(erro_texto) {
    $('.ponto_erro_info').remove();
    $id_ponto.after(ponto_info_tyle+erro_texto+'</p>');
    $('#info').show('fast');
}
/*
    Encontra Linhas
*/
function setSelectLinhas(ponto){
    $id_linha_opt.remove();
    $.getJSON('/'+ponto+'/linhas/', function(data){
        $.each(data.data, function(i,v) {
            $id_linha.append($("<option />").val(v.linha.match(linhas_option_num_regex)).text(v.linha));
        });
     }).error(function() { ponto_erro_info(ponto_n_encontrado); });
}
/*
    Completa lista de linhas e informacao sobre os pontos
*/
function get_linhas(){
    var ponto_value=$id_ponto.val();
    var ponto_encontrado=false;
    $.each(pontosJSON.data, function(i,ponto) {
        if(ponto.ponto==ponto_value){
            plocal=ponto.logradouro+', '+ponto.bairro+', '+ponto.referencia
            ponto_erro_info(plocal.toTitleCase());
            setSelectLinhas(ponto_value);
            ponto_encontrado=true;
            return false;// break
        }
    });
    return ponto_encontrado;
}

$(function() {
    /*
        Auto completar Pontos 
    */    
    $id_ponto.autocomplete({
	    source: pts,// from /js/pontos-array.js
	    minLength: 2,
	    autoFocus: true,
	    delay: 0,
    });
    
    /*
        Events
    */
    $id_ponto.keyup(function(){
        if(parseInt($(this).val().length) == 4){
            // Se somente um resultado fecha auto-complete
            if(parseInt($(this).autocomplete("widget").length)==1){
                $(this).autocomplete("close");
            }
            if(!get_linhas()){
                ponto_erro_info(ponto_n_encontrado);
            }
        }
        else{
            $("#id_linha option").remove();
            $('.ponto_erro_info').remove();
        }
    });
    
    $id_linha.mousedown(function(){
        if(!$(this).val()){
            event.preventDefault();// nao abre o dropdown
            if(!get_linhas()){
                ponto_erro_info(ponto_n_encontrado);
                $id_linha_opt.remove();
            }
        }
    });
    /*
        Excecoes
    */
    $('#id_twitter').change(function(){
        if($(this).val().match(/@/g)){
            $(this).val($(this).val().replace(/@/g, ""));
            $(this).after('<p id="info-twitter" style="display:none;color:#404040;font-size: 13px;padding-top: 4px;margin-bottom: 0px;">&ensp;&uarr; olha o @ já está aqui (^-^)</p>');
            $('#info-twitter').show('fast');
            $('#info-twitter').delay(8000).hide('slow');
        }
        //alert($(this).val().replace(/@/g, ""));
    });
});
