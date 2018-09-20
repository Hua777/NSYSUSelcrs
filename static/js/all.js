var Wait = () => {
    $('#waiting').show();
}
var Okay = () => {
    $('#waiting').hide();
}
var addclass = (number) => {
    swal({
        title: '請輸入您的志願序或是點數',
        input: 'text',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: '送出',
        cancelButtonText: '取消',
        showLoaderOnConfirm: true,
        preConfirm: (point) => {
            if (point == "" || isNaN(point)) {
                swal({
                    title: '錯誤',
                    text: "並不是數字",
                    button: "關閉",
                    icon: 'error'
                });
            } else {
                return fetch('/api/select', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    contentType: 'application/json; charset=UTF-8',
                    dataType: 'json',
                    body: JSON.stringify({
                        "type": '+',
                        "number": number,
                        "point": point
                    })
                }).then((result) => {
                    return result.json()
                });
            }
        },
        allowOutsideClick: () => !swal.isLoading()
    }).then((result) => {
        if (result.value.check) {
            swal({
                title: '成功',
                text: "成功加選",
                type: 'success'
            });
            refresh();
        } else if (!result.value.check) {
            swal({
                title: '失敗',
                text: "非選課時間",
                type: 'error'
            });
            refresh();
        }
    });
}
var removeclass = (number) => {
    swal({
        title: '您確定要退選嗎？',
        text: '你將無法恢復他！',
        showCancelButton: true,
        confirmButtonText: '送出',
        cancelButtonText: '取消',
        showLoaderOnConfirm: true,
        preConfirm: () => {
            return fetch('/api/select', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                contentType: 'application/json; charset=UTF-8',
                dataType: 'json',
                body: JSON.stringify({
                    "type": '-',
                    "number": number,
                    "point": 0
                })
            }).then((result) => {
                return result.json()
            });
        },
        allowOutsideClick: () => !swal.isLoading()
    }).then((result) => {
        if (result.value.check) {
            swal({
                title: '成功',
                text: "成功退選",
                type: 'success'
            });
            refresh();
        } else if (!result.value.check) {
            swal({
                title: '失敗',
                text: "非選課時間",
                type: 'error'
            });
            refresh();
        }
    });
}
var refresh = () => {
    Wait();
    $.ajax({
        type: 'POST',
        url: '/api/schedule',
        data: JSON.stringify({}),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        error: (err) => {
            Okay();
        },
        success: (res) => {
            Okay();
            if (res.check) {
                $('#schedule').html(res.html);
            }
        }
    });
}
var classclick = (number) => {
    Wait();
    $.ajax({
        type: 'POST',
        url: '/api/classinfo',
        data: JSON.stringify({
            "number": number
        }),
        contentType: 'application/json; charset=UTF-8',
        dataType: 'json',
        error: (err) => {
        },
        success: (res) => {
            var p = (res.Select > 0 ? Math.floor((res.Remaining / res.Select) * 10000) / 100 : 100);
            if (p > 100) p = 100;
            swal({
                title: res.Number + ' - ' + res.Name,
                html:
                    "教室：" + res.Room +
                    "<br/><br/>開放名額：" + res.Restrict +
                    "<br/>選上人數：" + res.Selected +
                    "<br/>剩餘人數：" + res.Remaining +
                    "<br/>點選人數：" + res.Select +
                    "<br/><br/>選上機率：" + p + "%（僅供參考）" +
                    "<br/><br/>\
                    <a class='btn btn-success btn-sm' href=\"javascript:addclass('" + res.Number + "');\">加選</a>\
                    <a class='btn btn-danger btn-sm' href=\"javascript:removeclass('" + res.Number + "');\">退選</a>\
                    <a class='btn btn-primary btn-sm' href=\"" + res.Url + "\" target='blank'>課綱</a>",
                button: "關閉",
            });
            Okay();
        }
    });
}
$(document).ready(() => {
    $('#loginBTN').click(() => {
        Wait();
        $('#loginBTN').prop('disabled', true);
        $.ajax({
            type: 'POST',
            url: '/api/login',
            data: JSON.stringify({
                "username": $('#usernameTXT').val(),
                "password": $('#passwordTXT').val(),
                "validcode": $('#validcodeTXT').val(),
                "validcodeSrc": $('#validcodeTXT').attr('data-src')
            }),
            contentType: 'application/json; charset=UTF-8',
            dataType: 'json',
            error: (err) => {
                Okay();
                alert('未知預期錯誤！');
                window.location.href = '/';
            },
            success: (res) => {
                Okay();
                if (res.check) {
                    window.location.href = '/main';
                } else {
                    alert(res.msg);
                    window.location.href = '/';
                }
            }
        });
    });
    Okay();
});