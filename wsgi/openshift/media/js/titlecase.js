// TitleCase
String.prototype.toTitleCase = function() {
    var i, str, lowers, uppers;
    str = this.replace(/\w\S*/g, function(txt) {
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });

    // Pt-Br
    lowers = ['', 'No', 'Na','Nos', 'Nas','Em', 'O', 'Os', 'A', 'As', 'Ao','Aos', 
    'Um', 'Uma', 'Uns', 'Umas','Do','De','Da','Dos','Des','Das','Defronte','Av',
    'Avn','Frente'];
    for (i = 0; i < lowers.length; i++)
        str = str.replace(new RegExp('\\s' + lowers[i] + '\\s', 'g'), 
            function(txt) {
                return txt.toLowerCase();
            });

    // Certain words such as initialisms or acronyms should be left uppercase
    uppers = ['Id'];
    for (i = 0; i < uppers.length; i++)
        str = str.replace(new RegExp('\\b' + uppers[i] + '\\b', 'g'), 
            uppers[i].toUpperCase());

    return str;
}
