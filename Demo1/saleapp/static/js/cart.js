function addToCart(id, name, price) {
    fetch('/api/cart', {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity
    }) // js promise
}
function updateCart(medicineId, obj) {
    fetch(`/api/cart/${medicineId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.info(data)
        let d = document.getElementsByClassName("cart-counter")
        for (let i = 0; i < d.length; i++)
            d[i].innerText = data.total_quantity

        let d2 = document.getElementsByClassName("cart-amount")
        for (let i = 0; i < d2.length; i++)
            d2[i].innerText = data.total_amount.toLocaleString("en-US")
    }) // js promise
}

function deleteCart(medicineId) {
    if (confirm("Bạn chắc chắn xóa không?") == true) {
        fetch(`/api/cart/${medicineId}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            console.info(data)
            let d = document.getElementsByClassName("cart-counter")
            for (let i = 0; i < d.length; i++)
                d[i].innerText = data.total_quantity

            let d2 = document.getElementsByClassName("cart-amount")
            for (let i = 0; i < d2.length; i++)
                d2[i].innerText = data.total_amount.toLocaleString("en-US")

            let c = document.getElementById(`cart${medicineId}`)
            c.style.display = "none"
        }).catch(err => console.info(err)) // js promise
    }

}

function pay(medicineId) {
    if (confirm("Bạn chắc chắn thanh toán?") == true) {
        fetch('/api/pay', {
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        if (data.status === 200)
                location.reload();
            else
                alert("Có lỗi xày ra!")
    }) // js promise
    }
}

 $(function() {
  // Sidebar toggle behavior
  $('#sidebarCollapse').on('click', function() {
    $('#sidebar, #content').toggleClass('active');
  });
});