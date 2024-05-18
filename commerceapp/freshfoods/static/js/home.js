let item = null;
let int = null;

$(document).ready(function () {
    $("#shopping-cont").on('click', 'a', function () {
        item = $(this).find('.item-add-cont');
        const id = parseInt(this.id.replace('product-', ''));
        const num = item.find('.item-add-remove-number').find('p');

        if ($(item).is(':hidden')) {
            // add the current count to the pop up
            $.ajax({
                url: `get/cart/item/${id}`,
                success: (res) => { num.text(res); },
            });


            $.ajax({
                url: `add/item/${id}`,
                success: () => {

                    if (int != null) {
                        clearTimeout(int);
                    }
                    num.text((parseInt(num.text()) + 1));

                    $('.item-add-cont').hide();
                    item.toggle();
                    int = setTimeout(() => { item.toggle() }, 5_000);
                    check_running(num.text(), 'add');
                }
            });
        }
    });

    $("#shopping-cont").on('click', '.fa-circle-minus', function () {
        const par = $(this).parent();
        const num = par.find('.item-add-remove-number');
        const parofpar = par.parent().parent().parent();
        const id = parofpar[0].id.replace('product-', '');
        $.ajax({
            url: `remove/item/${id}`,
            success: () => {
                if (int != null) {
                    clearTimeout(int);
                }

                if (parseInt(num.text()) !== 1) {
                    num.text((parseInt(num.text()) - 1));
                    int = setTimeout(() => { item.toggle() }, 5_000);
                }
                else{item.hide();}
                check_running(num.text(), 'remove');
            }
        });
    });

    $("#shopping-cont").on('click', '.fa-circle-plus', function () {
        const par = $(this).parent();
        const num = par.find('.item-add-remove-number');
        const parofpar = par.parent().parent().parent();
        const id = parofpar[0].id.replace('product-', '');

        $.ajax({
            url: `add/item/${id}`,
            success: () => {
                num.text((parseInt(num.text()) + 1));

                if (int != null) {
                    clearTimeout(int);
                }
                int = setTimeout(() => { item.toggle() }, 5_000);
                check_running(num.text(), 'add');
            }
        });
    });

    $('#shopping-cont').on('click', '.item-add-remove', function () {
        const par = $(this).parent();
        const num = par.find('.item-add-remove-number');
        const parofpar = par.parent();
        const id = parofpar[0].id.replace('product-', '');
        $.ajax({
            url: `remove/all/item/${id}`,
            success: () => {
                if (int != null) {
                    clearTimeout(int);
                }
                item.toggle();
                check_running(num.text(), 'remove-all');
                num.text(1);

            }
        });

    });
});

function check_running(name, res) {
    const shopping_num = $("#shopping-number");
    if (res === 'add') {
        if (shopping_num.text().trim() === '') {
            shopping_num.text('+1');
        }
        else {
            const num = parseInt(shopping_num.text().replace("+", '')) + 1;
            shopping_num.text(`+${num}`);
        }
    } else if (res === "remove-all") {
        const num = parseInt(shopping_num.text().replace("+", '')) - parseInt(name);
        if(num === 0){shopping_num.text("")}
        else{shopping_num.text(`+${num}`)}
    }
    else {
        if (shopping_num.text() === '+1') {
            shopping_num.text('');
        }
        else {
            const num = parseInt(shopping_num.text().replace("+", '')) - 1;
            shopping_num.text(`+${num}`);
        }
    }
}


function isInt(str) {
    return !isNaN(Number(str)) && str.trim() !== '';
}