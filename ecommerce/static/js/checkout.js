if(shipping=='False'){
    document.getElementById('shipping-info').innerHTML = ''
}
if (user != 'AnonymousUser'){
         document.getElementById('user-info').innerHTML = ''
}

if (shipping == 'False' && user != 'AnonymousUser'){
    //Hide entire form if user is logged in and shipping is false
        document.getElementById('form-wrapper').classList.add("hidden");
        //Show payment if logged in user wants to buy an item that does not require shipping
        document.getElementById('payment-info').classList.remove("hidden");
}

var form = document.getElementById('form')

form.addEventListener('submit', function(e){
    e.preventDefault()
    document.getElementById('form-button').classList.add('hidden')
    document.getElementById('payment-info').classList.remove('hidden')
})


