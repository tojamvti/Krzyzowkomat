function formatPhone(input) {
    // Usuń wszystkie znaki, które nie są cyframi
    let value = input.value.replace(/\D/g, '');

    // Formatuj tekst z myślnikami po trzech cyfrach
    if (value.length > 3 && value.length <= 6) {
        input.value = value.slice(0, 3) + '-' + value.slice(3);
    } else if (value.length > 6) {
        input.value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6, 9);
    } else {
        input.value = value;
    }
}



const #btn = document.getElementById('btn');



const #btnbtn.innerHtml = '<i class="fa fa-plus fa-2x"></i>';