$(document).ready(function () {
    $("#shopping-cont").on('click', '#trashcan', function (){
        const item = $(this);
        const totalprice = $('.shopping-item-total-price');
        const totalitem = $('.shopping-heading-small');
        const id = item.data("id");
        console.log(id);
        $.ajax({
            url: `/remove/all/item/${id}`,
            success: function(res){
                toti = parseInt(totalitem.text().replace(" items", '')) - 
                parseInt(item.parent().find('.shopping-item-child-count').text().replace('x', ''));
                totp = parseFloat(totalprice.text().replace("$ ", '')) - 
                parseFloat(item.parent().find('.shopping-item-child-price').text().replace("$ ", ''));
                totalitem.text(`${toti} items`);
                if (totp === 0){
                    $(".shopping-item-total-cont").remove();
                    $('.shopping-order-btn').remove();
                }
                else{
                    totp = totp.toFixed(2);
                    totalprice.text(`$ ${totp}`);
                } 
                item.parent().remove();
            }
        });
    });
});