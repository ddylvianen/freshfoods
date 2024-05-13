let item = null;
let int = null;

$(document).ready(function () {
    $("#shopping-cont").on('click', 'a', function (){
        item = $(this).find('.item-add-cont');
        const id = parseInt(this.id.replace('product-', ''));
        const num = item.find('.item-add-remove-number').find('p')

        

        if ($(item).is(':hidden')){
            $.ajax({
                url: `get/cart/item/${id}`,
                success: (res)=>{num.text(res)},
            });
            $.ajax({
                url: `add/item/${id}`,
                success: () =>{

                    if (int != null){
                        clearTimeout(int);
                    }
                    num.text((parseInt(num.text()) + 1))
                    $('.item-add-cont').hide();
                    item.toggle()
                    int = setTimeout(()=>{item.toggle()}, 5_000);
                }
            });
        }
    });

    $("#shopping-cont").on('click', '.fa-circle-minus', function(){
        const par = $(this).parent();
        const num = par.find('.item-add-remove-number');
        const parofpar = par.parent().parent().parent();
        const id = parofpar[0].id.replace('product-', '');
        $.ajax({
            url: `remove/item/${id}`,
            success: () =>{
                if (int != null){
                    clearTimeout(int);
                }

                if ( parseInt(num.text()) !== 1){
                    num.text((parseInt(num.text()) - 1));
                    int = setTimeout(()=>{item.toggle()}, 5_000);
                }     
            }
        });
    });

    $("#shopping-cont").on('click', '.fa-circle-plus', function(){
        const par = $(this).parent();
        const num = par.find('.item-add-remove-number');
        const parofpar = par.parent().parent().parent();
        const id = parofpar[0].id.replace('product-', '');
        
        $.ajax({
            url: `add/item/${id}`,
            success: () =>{
                num.text((parseInt(num.text()) + 1));

                if (int != null){
                    clearTimeout(int);
                }
                int = setTimeout(()=>{item.toggle()}, 5_000);
            }
        });
    });

    $('#shopping-cont').on('click', '.item-add-remove', function(){
        const par = $(this).parent();
        const num = par.find('.item-add-remove-number');
        const parofpar = par.parent();
        const id = parofpar[0].id.replace('product-', '');
        $.ajax({
            url: `remove/all/item/${id}`,
            success: () =>{
                if (int != null){
                    clearTimeout(int);
                }
                item.toggle()
                num.text(0); 
            }
        });
        
    });      
});


