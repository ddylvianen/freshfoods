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

    $("#oder-btn").on('click', function(){
        el = $(".shopping-item-total-cont, #product-item-count, #shopping-cont");
        message = $("<h5>Order was placed!</h5>").css({'text-align': 'center', 'grid-column': 'span 2'});
        $.ajax({
            url: `create/order`,
            success: () =>{
                el.html('');
                $("#oder-btn").hide();
                $(".shopping-item-total-cont").html(message).css('margin-top', '15rem');
            },});
    });
});