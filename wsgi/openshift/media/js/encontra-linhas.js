// Resolve conflito com prototype
jQuery.noConflict();

var pontosJSON;
var linhasJSON;
// regx filtro para linhas val
var linhas_option_num_regex=/([0-9]{1,4}[a-z]{0,2})/gi;
var $id_ponto=jQuery('#id_ponto');
var $id_info=jQuery('#info');
var $id_linha=jQuery('#id_linha');
var $id_linha_opt=jQuery("#id_linha option");
var ponto_info_style='<p class="ponto_erro_info" ' +
    'id="info"style="display:none;' +
    'color:#404040;font-size: 13px;padding-top: 4px;margin-bottom: 0px;">';
var ponto_n_encontrado='&ensp;&uarr; Ponto vazio ou não encontrado. ' +
    'Tente novamente (^-^\')';
/*
    Obtem lista JSON de pontos - pontosJSON
*/

jQuery.getJSON('/pontos/json', function(data){
    pontosJSON = data;
    //  jQuery.each(data.data, function(i,v) { pts[pts.length]=v.ponto; });
    //  lista de pontos disponiveis
}).complete(function() {
    if (jQuery('#id_ponto').val()){
        get_linhas();
    }
});

/*
    Ponto erro informacao
*/
function ponto_erro_info(erro_texto) {
    jQuery('.ponto_erro_info').remove();
    $id_ponto.after(ponto_info_style+erro_texto+'</p>');
    jQuery('#info').show('fast');
}
/*
    Encontra Linhas
*/
function setSelectLinhas(ponto){
    $id_linha_opt.remove();
    jQuery.getJSON('/'+ponto+'/linhas/', function(data){
        linhasJSON=data;
     }).error(function() { ponto_erro_info(ponto_n_encontrado); })
       .complete(function() { 
            jQuery.each(linhasJSON.data, function(n,linha) {
                $id_linha.append(jQuery("<option />").val(linha.linha.match(
                    linhas_option_num_regex)).text(linha.linha));
        });
     });
}
/*
    Completa lista de linhas e informacao sobre os pontos
*/
function get_linhas(){
    var ponto_value=$id_ponto.val();
    var ponto_encontrado=false;
    jQuery.each(pontosJSON.data, function(i,ponto) {
        if(ponto.ponto==ponto_value){
            plocal = ponto.logradouro + ', ' +
                    ponto.bairro + ', ' +
                    ponto.referencia
            ponto_erro_info(plocal.toTitleCase());
            setSelectLinhas(ponto_value);
            ponto_encontrado=true;
            return false;// break
        }
    });
    return ponto_encontrado;
}

jQuery(function() {
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
        if(parseInt(jQuery(this).val().length) == 4){
            // Se somente um resultado fecha auto-complete
            if(parseInt(jQuery(this).autocomplete("widget").length)==1){
                jQuery(this).autocomplete("close");
            }
            if(!get_linhas()){
                ponto_erro_info(ponto_n_encontrado);
            }
        }
        else{
            jQuery("#id_linha option").remove();
            jQuery('.ponto_erro_info').remove();
        }
    });
    
    $id_linha.mousedown(function(){
        if(!jQuery(this).val()){
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
    jQuery('#id_twitter').change(function(){
        if(jQuery(this).val().match(/@/g)){
            jQuery(this).val(jQuery(this).val().replace(/@/g, ""));
            jQuery(this).after('<p id="info-twitter" ' +
                'style="display:none;color:#404040;' +
                'font-size: 13px;padding-top: 4px;margin-bottom: 0px;' +
                '">&ensp;&uarr; olha o @ já está aqui (^-^)</p>');
            jQuery('#info-twitter').show('fast');
            jQuery('#info-twitter').delay(8000).hide('slow');
        }
        //alert(jQuery(this).val().replace(/@/g, ""));
    });
});
