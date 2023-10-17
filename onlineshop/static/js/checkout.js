$(function() {
    // var IMP = window.IMP;
    IMP.init('imp43546585');

    $(".order-form").on("submit", function(e){
        var amount = parseFloat($(".order-form input[name='amount']").val().replace(',', ''));
        var type = $(".order-form input[name='type']:checked").val();

        // 폼 데이터를 기준으로 주문 생성
        var order_id = AjaxCreateOrder(e);
        if (order_id == false){
            alert("AjaxCreateOrder: 주문 생성 실패\n다시 시도해주세요.");
            return false;
        }

        // 결제 정보 생성
        var merchant_id = AjaxStoreTransaction(e, order_id, amount, type);

        // 생성된 결제 정보로 iamport 결제시도
        if (merchant_id !== ''){
            IMP.request_pay({
                "pg": "html5_inicis.INIBillTst",
                "pay_method": "card",
                "merchant_uid": merchant_id,
                "name": "E-shop product",
                "buyer_name": $('input["first_name"]').val() + ' ' + $('input["last_name"]').val(),
                "buyer_email": $("input['email']").val(),
                "amount": amount
            }, function(rsp) {
                if (rsp.success){
                    var msg = "결제가 완료되었습니다.";
                    msg += "고유 ID" + rsp.imp_uid;
                    msg += "상점 거래 ID" + rsp.merchant_uid;
                    msg += "결제 금액" + rsp.paid_amount;
                    msg += "카드 승인번호" + rsp.apply_num;
                    
                    // DB에 반영
                    IMPTransaction(e, order_id, rsp.merchant_uid, rsp.imp_uid, rsp.paid_amount);
                }
                else{
                    var msg = "결제에 실패하였습니다.";
                    msg += "에러 내용" + rsp.error_msg;
                    console.log(msg);
                }
            });
        }
        return false;
    });
});

function AjaxCreateOrder(e){
    e.preventDefault();

    var order_id = "";

    var request = $.ajax({
        method: "POST",
        url: order_create_url,
        async: false,
        data: $('.order-form').serialize()
    });

    request.done(function(data){
        if (data.order_id){
            order_id = data.order_id;
        }
    });

    request.fail(function(jqXHR, textStatus){
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        }
        else if (jqXHR.status == 403){
            alert("로그인 해주세요");
        }
        else{
            alert("AjaxCreateOrder: 문제가 발생했습니다. 다시 시도해주세요.");
        }
    });

    return order_id;
}

function AjaxStoreTransaction(e, order_id, amount, type){
    e.preventDefault();

    var merchant_id = '';

    var request = $.ajax({
        method: "POST",
        url: order_checkout_url,
        async: false,
        data: {
            order_id: order_id,
            amount: amount,
            type: type,
            csrfmiddlewaretoken: csrf_token,
        },
    });

    request.done(function(data){
        if (data.works){
            merchant_id = data.merchant_id;
        }
    });

    request.fail(function(jqXHR, textStatus){
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        }
        else if (jqXHR.status == 403){
            alert("로그인 해주세요");
        }
        else{
            alert("AjaxStoreTransaction: 문제가 발생했습니다. 다시 시도해주세요.");
        }
    });

    return merchant_id;
}

function IMPTransaction(e, order_id, merchant_id, imp_id, amount){
    e.preventDefault();
    var request = $.ajax({
        method: "POST",
        url: order_validation_url,
        async: false,
        data: {
            order_id: order_id,
            merchant_id: merchant_id,
            imp_id: imp_id,
            amount: amount,
            csrfmiddlewaretoken: csrf_token,
        }
    });

    request.done(function(data){
        if (data.works){
            $(location).attr("href", location.origin+order_complete_url+"?order_id"+order_id)
        }
    });

    request.fail(function(jqXHR, textStatus){
        if (jqXHR.status == 404) {
            alert("페이지가 존재하지 않습니다.");
        }
        else if (jqXHR.status == 403){
            alert("로그인 해주세요");
        }
        else{
            alert("IMPTransaction: 문제가 발생했습니다. 다시 시도해주세요.");
        }
    });
}